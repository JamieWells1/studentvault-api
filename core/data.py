# Used for controlling the db_cache files in real-time
import json
import requests
from json.decoder import JSONDecodeError
from typing import Dict, List, Any
import threading
import time

from utils import logger

from rapidfuzz import process, fuzz


class Data:
    def __init__(self):
        with open("db_cache/module.json", "r") as module_data:
            try:
                modules = json.load(module_data)
            except (FileNotFoundError, JSONDecodeError):
                modules = {}

        with open("db_cache/lesson.json", "r") as lesson_data:
            try:
                lessons = json.load(lesson_data)
            except (FileNotFoundError, JSONDecodeError):
                lessons = {}

        with open("db_cache/ai_quiz.json", "r") as quiz_data:
            try:
                quizzes = json.load(quiz_data)
            except (FileNotFoundError, JSONDecodeError):
                quizzes = {}

        with open("db_cache/flashcard_deck.json", "r") as deck_data:
            try:
                decks = json.load(deck_data)
            except (FileNotFoundError, JSONDecodeError):
                decks = {}

        self.tables = {
            "module": modules,
            "lesson": lessons,
            "ai_quiz": quizzes,
            "flashcard_deck": decks,
        }
        self.sync_frequency = 3600
        self.sync_scheduled = False

        self.sync()
        logger.output(
                f"✅ All table contents written to cache"
            )


    # =========== File interaction ===========

    def sync(self) -> Dict[str, Any]:
        TABLES = ["module", "lesson", "ai_quiz", "flashcard_deck"]

        logger.output("Writing database content to JSON memory...")

        self.file_writing_allowed = False
        for table in TABLES:
            url = f"https://studentvault.co.uk/version-test/api/1.1/obj/{table}"
            try:
                data = requests.get(url).json()
            except Exception as e:
                return {"status": 400, "message": str(e)}

            results: List[str, Any] = data["response"].get("results")
            json_objects = {}

            for result in results:
                uid = result["_id"]
                title = result.get("title", "Untitled")

                self.tables[table][uid] = title
                json_objects[uid] = title

            with open(f"db_cache/{table}.json", "w") as f:
                json.dump(json_objects, f, indent=2)

        self.file_writing_allowed = True
        return {"status": 200, "message": "Data synced to cache successfully"}

    def schedule_sync(self):
        def background_sync():
            logger.output(f"⏳ Sync thread sleeping for {self.sync_frequency} seconds...")
            time.sleep(self.sync_frequency)
            self.sync()
            self.sync_scheduled = False
            logger.output(f"✅ Sync completed after delay of {self.sync_frequency} seconds.")

        if not self.sync_scheduled:
            self.sync_scheduled = True
            threading.Thread(target=background_sync, daemon=True).start()
        else:
            logger.output(f"🔄 Sync already scheduled to run (runs every {self.sync_frequency} seconds)")

    def append_json(self, table: str, unique_id: str, title: str) -> None:
        with open(f"db_cache/{table}.json", "r+") as f:
            entries = json.load(f)
            entries[unique_id] = title
            f.seek(0)
            json.dump(entries, f, indent=4)
            logger.output(f"Updated item '{title}' in shared JSON storage")

    def delete_json(self, table: str, unique_id: str, title: str) -> None:
        with open(f"db_cache/{table}.json", "r+") as f:
            entries = json.load(f)
            entries.pop(unique_id, entries)
            f.seek(0)
            f.truncate()
            json.dump(entries, f, indent=4)
            logger.output(f"Deleted item '{title}' from shared JSON storage")

    # =========== Local instance updates ===========

    def update(self, table: str, unique_id: str, title: str) -> Dict[str, str]:
        self.tables[table][unique_id] = title
        logger.output(f"Entry updated: {unique_id}: {title}")
        self.append_json(table, unique_id, title)
        self.schedule_sync()
        return {unique_id: title}

    def delete(self, table: str, unique_id: str, title: str) -> Dict[str, str]:
        self.tables[table].pop(unique_id, None)
        logger.output(f"Entry deleted: {unique_id}: {title}")
        self.delete_json(table, unique_id, title)
        self.schedule_sync()
        return {unique_id: title}

    # =========== Searching ===========

    def search(self, table: str, query: str, bucket_size: int):
        query = query.lower()
        id_to_title = self.tables[table]
        title_to_id = {title.lower(): uid for uid, title in id_to_title.items()}

        titles = list(title_to_id.keys())

        results = process.extract(query, titles, scorer=fuzz.ratio, limit=24)

        matches = []

        for title, score, _ in results:
            # round to nearest 5
            # a larger bucket size will prioritise relevance less
            # a smaller bucket size will prioritise relevance more
            rounded_score = round(score / bucket_size) * bucket_size
            uid = title_to_id[title]

            matches.append({"unique_id": uid, "title": title, "score": rounded_score})
        return matches
