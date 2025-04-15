# Used for controlling the db_cache files in real-time
import json
import requests
from json.decoder import JSONDecodeError
from typing import Dict, List, Any
import asyncio
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
        self._dirty_tables = set()
        self._last_write = {}
        self._write_threads = {}
        self._write_interval = 2
        self.file_writing_allowed = True

        self._start_sync_scheduler()

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

            logger.output(
                f"✅ Successfully written contents from table '{table}' to cache."
            )

        self.file_writing_allowed = True
        return {"status": 200, "message": "Data synced to cache successfully"}

    def _schedule_write(self, table: str):
        if self.file_writing_allowed:

            def write_later():
                while True:
                    time.sleep(self._write_interval)

                    if time.time() - self._last_write[table] >= self._write_interval:
                        with open(f"db_cache/{table}.json", "w") as f:
                            json.dump(self.tables[table], f, indent=2)
                        logger.output(f"✅ Wrote updated JSON for table '{table}'")

                        self._dirty_tables.discard(table)
                        self._write_threads.pop(table, None)
                        break

            self._last_write[table] = time.time()

            if table not in self._dirty_tables:
                self._dirty_tables.add(table)

                if table not in self._write_threads:
                    self._write_threads[table] = threading.Thread(target=write_later)
                    self._write_threads[table].start()

    def _start_sync_scheduler(self):
        def periodic_sync():
            while True:
                try:
                    self.sync()
                except Exception as e:
                    logger.output(f"Periodic sync failed: {e}")
                time.sleep(60)

        threading.Thread(target=periodic_sync, daemon=True).start()

    # =========== Local instance updates ===========

    def update(self, table: str, unique_id: str, title: str) -> Dict[str, str]:
        self.tables[table][unique_id] = title
        self._schedule_write(table)
        return {unique_id: title}

    def delete(self, table: str, unique_id: str, title: str) -> Dict[str, str]:
        self.tables[table].pop(unique_id, None)
        self._schedule_write(table)
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
