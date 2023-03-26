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
