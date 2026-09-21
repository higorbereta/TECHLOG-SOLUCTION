from fastapi import Depends
from typing import Annotated

from src.database.local import LocalDatabase
from src.database.client_repository import ClientRepository

database = LocalDatabase()
database.initialize()

def get_local_db() -> LocalDatabase:
    return database

def get_client_repository(local_database: Annotated[LocalDatabase, Depends(get_local_db)]) -> 'ClientRepository':
    return ClientRepository(local_database)