import uuid
from threading import Lock

searches = {}

lock = Lock()


def create_search(query):
    search_id = str(uuid.uuid4())

    with lock:
        searches[search_id] = {
            "query": query,      # <-- Add this line
            "amazon": {
                "status": "loading",
                "data": None
            },
            "flipkart": {
                "status": "loading",
                "data": None
            },
            "ajio": {
                "status": "loading",
                "data": None
            },
            "meesho": {
                "status": "loading",
                "data": None
            }
        }

    return search_id


def update_site(search_id, site, data):
    with lock:
        if search_id in searches:
            searches[search_id][site]["status"] = "done"
            searches[search_id][site]["data"] = data


def update_error(search_id, site, error):
    with lock:
        if search_id in searches:
            searches[search_id][site]["status"] = "error"
            searches[search_id][site]["data"] = str(error)


def get_search(search_id):
    with lock:
        return searches.get(search_id)