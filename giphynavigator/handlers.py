"""Handlers module."""

from fastapi import  Depends, Query
from dependency_injector.wiring import inject, Provide
from fastapi.responses import JSONResponse
import json

from .services import SearchService
from .containers import Container


@inject
async def index(
    query: str = Query(default="giphy", description="Search query"),
    limit: int = Query(default=60, description="Number of results"),
    search_service: SearchService = Depends(Provide[Container.entity_a_package.search_service])
) -> JSONResponse:
    print("index")
    
    print("await")
    response = await search_service.search(query, limit)
    print(response)
    #json_response = json.dumps(response)

    return JSONResponse(
        content={
            "query": query,
            "limit": limit,
            "gifs": "",
        },
    )