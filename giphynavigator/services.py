"""Services module."""


from .giphy import EntityRepository

class SearchService:

    def __init__(self, giphy_client: EntityRepository):
        self._giphy_client = giphy_client

    async def search(self, query, limit):
        """Search for gifs and return formatted data."""
        if not query:
            return []

        result = await self._giphy_client.search(query, limit)

        return [result]
