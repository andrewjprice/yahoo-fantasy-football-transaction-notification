import os
from functools import lru_cache
from pymongo import MongoClient

class DB():
    def __init__(self, *args, **kwargs):
        self.client = MongoClient(os.getenv('mongodb'))

    @lru_cache
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)