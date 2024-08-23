from fastapi import FastAPI
from app.controllers.utility_controller import UtilityController, seed
from app.database.database import SessionLocal, engine
from app.database.database import Base
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, user_types, courses, enrollments, utility

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:63342",
    "file://",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# TODO: Implement a better way for versioning
prefix = "/api/v0"

# Register routers
app.include_router(users.router, prefix=prefix)
app.include_router(user_types.router, prefix=prefix)
app.include_router(courses.router, prefix=prefix)
app.include_router(enrollments.router, prefix=prefix)
app.include_router(utility.router, prefix=prefix)


@app.on_event("startup")
def on_startup():
    """On server startup, seed the database."""
    db = SessionLocal()
    uc = UtilityController(db);
    seed(uc)
    db.close()
