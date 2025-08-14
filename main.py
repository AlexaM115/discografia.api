import uvicorn
import logging

from fastapi import FastAPI, Request

from controllers.users import create_user, login
from models.users import User
from models.login import Login

from utils.security import validateuser, validateadmin

from routes.artist import router as artist_router
from routes.artist_type import router as artist_type_router
from routes.artist_skill import router as artist_skill_router
from routes.recording_studio import router as recording_studio_router
from routes.album import router as album_router
from routes.song import router as song_router
from routes.song_pipeline import router as song_pipeline_router
from routes.genre import router as genre_router
from routes.review import router as review_router
from routes.colaboration import router as colaboration_router
from routes.colaboration_pipeline import router as colaboration_pipeline_router
from routes.review_pipeline import router as review_pipeline_router
from routes.songs_by_filter import router as songs_by_filter_router



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


from fastapi.openapi.utils import get_openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Discografía API",
        version="1.0.0",
        description="API para gestión de artistas y música",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


app.include_router(artist_router)
app.include_router(artist_type_router)
app.include_router(artist_skill_router)
app.include_router(recording_studio_router)
app.include_router(album_router)
app.include_router(song_router)
app.include_router(song_pipeline_router)
app.include_router(genre_router)
app.include_router(review_router)
app.include_router(colaboration_router)
app.include_router(colaboration_pipeline_router)
app.include_router(review_pipeline_router)
app.include_router(songs_by_filter_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"status": "healthy", "version": "0.0.0", "service": "discografia-api"}

@app.get("/health")
def health_check():
    try:
        return {
            "status": "healthy", 
            "timestamp": "2025-08-02", 
            "service": "discografia-api",
            "environment": "production"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/ready")
def readiness_check():
    try:
        from utils.mongodb import test_connection
        db_status = test_connection()
        return {
            "status": "ready" if db_status else "not_ready",
            "database": "connected" if db_status else "disconnected",
            "service": "dulceria-api"
        }
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}


@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)


@app.get("/exampleadmin")
@validateadmin
async def example_admin(request: Request):
    return {
        "message": "This is an example admin endpoint."
        , "admin": request.state.admin
    }

@app.get("/exampleuser")
@validateuser
async def example_user(request: Request):
    return {
        "message": "This is an example user endpoint."
        ,"email": request.state.email
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")