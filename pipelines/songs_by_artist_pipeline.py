from utils.mongodb import get_collection
from bson import ObjectId

def get_songs_by_artist(id_artist: str):
    collection = get_collection("songs")
    pipeline = [
        {
            "$match": {
                "id_artist": id_artist
            }
        },
        {
            "$lookup": {
                "from": "albums",
                "localField": "id_album",
                "foreignField": "_id",
                "as": "album"
            }
        },
        {
            "$unwind": {
                "path": "$album",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "name": 1,
                "duration": 1,
                "album": "$album.nombre"
            }
        }
    ]
    return list(collection.aggregate(pipeline))