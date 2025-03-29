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

        self.modules = modules
        self.lessons = lessons
        self.quizzes = quizzes
        self.decks = decks

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

    def update(self, table, unique_id, title) -> Dict[str, str]:
        if table == "module":
            self.modules[unique_id] = title
        elif table == "lesson":
            self.lessons[unique_id] = title
        elif table == "ai_quiz":
            self.quizzes[unique_id] = title
        elif table == "flashcard_deck":
            self.decks[unique_id] = title

        return {unique_id: title}

    def delete(self, table, unique_id, title) -> Dict[str, str]:
        if table == "module":
            self.modules.pop(unique_id)
        elif table == "lesson":
            self.lessons.pop(unique_id)
        elif table == "ai_quiz":
            self.quizzes.pop(unique_id)
        elif table == "flashcard_deck":
            self.decks.pop(unique_id)

        return {unique_id: title}

    def search(self, resource_type, query):
        if resource_type == "module":
            titles_to_search = list(self.modules.values())
        elif resource_type == "lesson":
            titles_to_search = list(self.lessons.values())
        elif resource_type == "ai_quiz":
            titles_to_search = list(self.quizzes.values())
        elif resource_type == "flashcard_deck":
            titles_to_search = list(self.decks.values())

        results = process.extract(query, titles_to_search, scorer=fuzz.ratio, limit=5)

        for match, score, _ in results:
            print(f"- {match} ({score})")
