"""Giphy client module."""

from aiohttp import ClientSession, ClientTimeout
from opensearchpy import AsyncOpenSearch
import random
import string

class EntityRepository:
    def __init__(self, elastic_client: AsyncOpenSearch):
        self.elastic_client = elastic_client
        
    async def insert_random_data(self, index):
        random_data = {
            "field": ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        }
        response = await self.elastic_client.index(index=index, body=random_data)
        return response

    async def search(self, query, limit):
        # Insert random data before searching
        await self.insert_random_data("some_index")
     
        response = await self.elastic_client.search(index="some_index", body={"query": {"match_all": {}}})
        return response
