from utils.mongodb import get_collection

def get_song_details():
    collection = get_collection("songs")
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
                "from": "genres",
                "localField": "id_genre",
                "foreignField": "_id",
                "as": "genre"
            }
        },
        { "$unwind": "$genre" },
        {
            "$lookup": {
                "from": "albums",
                "localField": "id_album",
                "foreignField": "_id",
                "as": "album"
            }
        },
        { "$unwind": "$album" },
        {
            "$lookup": {
                "from": "recording_studios",
                "localField": "id_estudio",
                "foreignField": "_id",
                "as": "studio"
            }
        },
        { "$unwind": "$studio" },
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "name": 1,
                "duration": 1,
                "artist": {
                    "name": "$artist.name",
                    "lastname": "$artist.lastname"
                },
                "genre": {
                    "description": "$genre.description"
                },
                "album": {
                    "nombre": "$album.nombre",
                    "año": "$album.año"
                },
                "studio": {
                    "description": "$studio.description",
                    "ubication": "$studio.ubication"
                }
            }
        }
    ]
    return list(collection.aggregate(pipeline))