from fastapi import FastAPI
from app.routes import download, metadata, history
from app.db.database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

create_db_and_tables()



app.include_router(download.router)
app.include_router(metadata.router)
app.include_router(history.router)

