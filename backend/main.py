from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes.app_routes import router as app_router
from .routes.auth_routes import router as auth_router
from .auth import auth_middleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_middleware)
Base.metadata.create_all(bind=engine)

app.include_router(app_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

