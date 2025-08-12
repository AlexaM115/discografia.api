from utils.mongodb import get_collection

def get_colaboration_details():
    collection = get_collection("colaborations")
    pipeline = [
        {
            "$lookup": {
                "from": "artists",
                "localField": "id_artist",
                "foreignField": "_id",
                "as": "artist"
            }
        },
        { "$unwind": "$artist" },
        {
            "$lookup": {
                "from": "songs",
                "localField": "id_song",
                "foreignField": "_id",
                "as": "song"
            }
        },
        { "$unwind": "$song" },
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "artist": {
                    "name": "$artist.name",
                    "lastname": "$artist.lastname"
                },
                "song": {
                    "name": "$song.name",
                    "duration": "$song.duration"
                }
            }
        }
    ]
    return list(collection.aggregate(pipeline))