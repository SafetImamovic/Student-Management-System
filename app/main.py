from fastapi import FastAPI
from app.database.database import SessionLocal, engine
from app.database.database import Base
from app.utils.seeding import seed
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
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router)
app.include_router(user_types.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(utility.router)


@app.on_event("startup")
def on_startup():
    """On server startup, seed the database."""
    db = SessionLocal()
    seed(db)
    db.close()


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World!"}
