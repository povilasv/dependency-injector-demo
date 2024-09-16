"""Containers module."""

from dependency_injector import containers, providers
from elasticsearch import AsyncElasticsearch
from typing import AsyncIterator, Optional
from . import giphy, services

async def create_elasticsearch_client() -> AsyncIterator[Optional[AsyncElasticsearch]]:
    client = AsyncElasticsearch(
        hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],  # Add 'scheme': 'http'
        verify_certs=False
    )
    try:
        yield client
    finally:
        await client.close()

class ConfigurationContainer(containers.DeclarativeContainer):
    elastic_client = providers.Resource(
        create_elasticsearch_client
    )



class EntityAContainer(containers.DeclarativeContainer):
    elastic_client = providers.Dependency(instance_of=AsyncElasticsearch)

    entity_repository = providers.Factory(
        giphy.EntityRepository, 
        elastic_client=elastic_client
    )
    search_service = providers.Factory(
        services.SearchService,
        giphy_client=entity_repository,
    )




class Container(containers.DeclarativeContainer):
    #config = providers.DependenciesContainer()
    config = providers.Configuration(yaml_files=["config.yml"])
    wiring_config = containers.WiringConfiguration(modules=[".handlers", ".containers"])
    # TODO:

    infra_package = providers.Container(ConfigurationContainer)

    entity_a_package = providers.Container(
        EntityAContainer,
        elastic_client=infra_package.elastic_client
    )

    #elastic_client = providers.Dependency(instance_of=AsyncOpenSearch)
    #elastic_client = providers.Resource(
    #    create_opensearch_client
    #)

