from fastapi import FastAPI
from .database import Base, engine
from .routes.app_routes import router as app_router
from .routes.auth_routes import router as auth_router
from .auth import auth_middleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.middleware("http")(auth_middleware)
Base.metadata.create_all(bind=engine)

app.include_router(app_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

