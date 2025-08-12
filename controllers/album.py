from models.album import Album
from utils.mongodb import get_collection
from bson import ObjectId
from fastapi import HTTPException

collection = get_collection("albums")
artist_collection = get_collection("artists")

def create_album(album: Album):
    if not artist_collection.find_one({"_id": ObjectId(album.id_artist)}):
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    if collection.find_one({"nombre": album.nombre, "año": album.año, "id_artist": album.id_artist}):
        raise HTTPException(status_code=400, detail="El álbum ya existe para ese artista")
    result = collection.insert_one(album.dict(by_alias=True, exclude={"id"}))
    return {"message": "Álbum creado", "id": str(result.inserted_id)}

def get_all_albums():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_album(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    doc["_id"] = str(doc["_id"])
    return doc

def get_albums_by_artist(id_artist: str):
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find({"id_artist": id_artist})]

def update_album(id: str, album: Album):
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": album.dict(by_alias=True, exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No se modificó ningún álbum")
    return {"message": "Álbum actualizado"}

def delete_album(id: str):
    songs = get_collection("songs")
    if songs.find_one({"id_album": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: álbum en uso")
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    return {"message": "Álbum eliminado"}