from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

connection_string = 'mongodb://localhost:27017'
db_name = 'wallet_db'

def get_database():
    client = AsyncIOMotorClient(connection_string)
    return client[db_name]