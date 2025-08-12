from utils.mongodb import get_collection
from bson import ObjectId

def get_songs_by_album(id_album: str):
    collection = get_collection("songs")
    return [
        {**doc, "_id": str(doc["_id"])}
        for doc in collection.find({"id_album": id_album})
    ]