from utils.mongodb import get_collection

def get_average_reviews():
    collection = get_collection("reviews")
    pipeline = [
        {
            "$group": {
                "_id": "$id_song",
                "average_rating": { "$avg": "$rating" },
                "total_reviews": { "$sum": 1 }
            }
        },
        {
            "$lookup": {
                "from": "songs",
                "localField": "_id",
                "foreignField": "_id",
                "as": "song"
            }
        },
        { "$unwind": "$song" },
        {
            "$project": {
                "_id": 0,
                "song_id": { "$toString": "$_id" },
                "song_name": "$song.name",
                "average_rating": { "$round": ["$average_rating", 2] },
                "total_reviews": 1
            }
        }
    ]
    return list(collection.aggregate(pipeline))