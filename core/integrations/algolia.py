from typing import List

from algoliasearch.search.client import SearchClientSync

app_id = "WCKUJMGIF6"
api_key = "9020be9bfaf3b94f6894dd8a12c0df8b"
index_name = "quizzes_index"

client = SearchClientSync(app_id, api_key)


def search() -> List[object]:
    search_response = client.search(
        {"requests": [{"indexName": index_name, "query": "civil"}]}
    )

    search_results = search_response.results

    search_response_obj = search_results[0].actual_instance

    hits = search_response_obj.hits

    print(type(hits[0]))

    return hits
