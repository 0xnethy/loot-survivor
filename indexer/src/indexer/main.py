"""Apibara indexer entrypoint."""

import asyncio
from functools import wraps

import click

from apibara.protocol import StreamAddress

from indexer.indexer import run_indexer
from indexer.graphql import run_graphql_api


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.option("--mongo-url", default=None, help="MongoDB url.")
@click.option("--restart", is_flag=True, help="Restart indexing from the beginning.")
@click.option("--network", default=None, help="Network id.")
@click.option("--game", is_flag=None, help="Game contract address.")
@click.option("--start_block", is_flag=None, help="Indexer starting block.")
@async_command
async def start(mongo_url, restart, network, game, start_block):
    """Start the Apibara indexer."""
    if network is None:
        server_url = StreamAddress.StarkNet.Goerli
    elif network == "goerli":
        server_url = StreamAddress.StarkNet.Goerli
    elif network == "mainnet":
        server_url = StreamAddress.StarkNet.Mainnet

    if mongo_url is None:
        mongo_url = "mongodb://apibara:apibara@localhost:27017"

    await run_indexer(
        restart=restart,
        server_url=server_url,
        mongo_url=mongo_url,
        network=network,
        game=game,
        start_block=start_block,
    )


@cli.command()
@click.option("--mongo_goerli", default=None, help="Mongo url for goerli.")
@click.option("--mongo_mainnet", default=None, help="Mongo url for mainnet.")
@click.option("--port", default=None, help="Port number.")
@async_command
async def graphql(mongo_goerli, mongo_mainnet, port):
    """Start the GraphQL server."""
    if port is None:
        port = "8080"
    if mongo_goerli is None:
        mongo_goerli = "mongodb://apibara:apibara@localhost:27017"
    if mongo_mainnet is None:
        mongo_mainnet = "mongodb://apibara:apibara@localhost:27018"

    await run_graphql_api(
        mongo_goerli=mongo_goerli, mongo_mainnet=mongo_mainnet, port=port
    )
