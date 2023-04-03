import asyncio

import click


@click.group("extract")
def aps_extract():
    """
    Container for all APS extract commands
    """
    pass


@aps_extract.command("gplay")
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
)
def gplay(recursive: bool):
    from aps.gplay import GPlay

    gp = GPlay()
    if recursive:
        asyncio.run(gp.fetch_all_recursive())
    else:
        asyncio.run(gp.fetch_all())


@aps_extract.command("appstore")
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
)
def appstore(recursive: bool):
    from aps.appstore import AppStore

    appstore = AppStore()
    if recursive:
        asyncio.run(appstore.fetch_all_recursive())
    else:
        asyncio.run(appstore.fetch_all())
