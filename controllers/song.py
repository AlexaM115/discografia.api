from models.song import Song
from utils.mongodb import get_collection
from bson import ObjectId
from fastapi import HTTPException

collection = get_collection("songs")
artist_collection = get_collection("artists")
genre_collection = get_collection("genres")
album_collection = get_collection("albums")
studio_collection = get_collection("recording_studios")

def create_song(song: Song):
    if not artist_collection.find_one({"_id": ObjectId(song.id_artist)}):
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    if not genre_collection.find_one({"_id": ObjectId(song.id_genre)}):
        raise HTTPException(status_code=404, detail="Género no encontrado")
    if not album_collection.find_one({"_id": ObjectId(song.id_album)}):
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    if not studio_collection.find_one({"_id": ObjectId(song.id_estudio)}):
        raise HTTPException(status_code=404, detail="Estudio no encontrado")

    result = collection.insert_one(song.dict(by_alias=True, exclude={"id"}))
    return {"message": "Canción creada", "id": str(result.inserted_id)}

def get_all_songs():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_song(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    doc["_id"] = str(doc["_id"])
    return doc

def update_song(id: str, song: Song):
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": song.dict(by_alias=True, exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No se modificó ninguna canción")
    return {"message": "Canción actualizada"}

def delete_song(id: str):
    # Verificar si hay reviews asociadas
    reviews = get_collection("reviews")
    if reviews.find_one({"id_song": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: canción tiene reviews")

    # Verificar si hay colaboraciones asociadas
    colabs = get_collection("colaborations")
    if colabs.find_one({"id_song": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: canción en colaboración")

    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return {"message": "Canción eliminada"}