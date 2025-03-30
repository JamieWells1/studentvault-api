# Used for controlling the db_cache files in real-time
import json
import requests
from json.decoder import JSONDecodeError
from typing import Dict, List, Any

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

    def sync(self) -> Dict[str, Any]:
        TABLES = ["module", "lesson", "ai_quiz", "flashcard_deck"]

        logger.output("Writing database content to JSON memory...")

        for table in TABLES:
            url = f"https://studentvault.co.uk/version-test/api/1.1/obj/{table}"
            try:
                data = requests.get(url).json()
            except Exception as e:
                return {"status": 400, "message": str(e)}

            results: List[str, Any] = data["response"].get("results")
            json_objects = {}

            for result in results:
                json_objects[result["_id"]] = result.get("title", "Untitled")

            with open(f"db_cache/{table}.json", "w") as f:
                json.dump(json_objects, f, indent=2)

            logger.output(
                f"Successfully written contents from table '{table}' to cache."
            )

        return {"status": 200, "message": "Data synced to cache successfully"}

    def update(self, table: str, unique_id: str, title: str) -> Dict[str, str]:
        self.tables[table][unique_id] = title
        return {unique_id: title}

    def delete(self, table: str, unique_id: str, title: str) -> Dict[str, str]:
        self.tables[table].pop(unique_id, None)
        return {unique_id: title}

    def search(self, table: str, query: str):
        query = query.lower()
        titles = [title.lower() for title in self.tables[table].values()]

        results = process.extract(query, titles, scorer=fuzz.ratio, limit=24)

        matches = []
        scores = []
        ids = []

        for match, score, _ in results:
            matches.append(match)
            scores.append(score)
            # ids.append(title_to_id.get(match))

            # Need to return id too, not sure this will work

            # Group entries with similar scores together and
            # then add a wrapper filter of studies/user reviews??

            # also add async disk-writing

        return {"matches": matches, "scores": scores, "ids": ids}
