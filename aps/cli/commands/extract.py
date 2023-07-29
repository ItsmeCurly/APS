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
@click.option(
    "-r",
    "--load-reviews",
    is_flag=True,
    default=False,
)
@click.option(
    "-p",
    "--load-policy-content",
    is_flag=True,
    default=False,
)
def gplay(
    recursive: bool,
    load_reviews: bool,
    load_policy_content: bool,
):
    from aps.gplay import GPlay

    gp = GPlay()
    if recursive:
        asyncio.run(
            gp.fetch_all_recursive(
                load_policy_content=load_policy_content, load_reviews=load_reviews
            )
        )
    else:
        asyncio.run(
            gp.fetch_all(
                load_policy_content=load_policy_content, load_reviews=load_reviews
            )
        )


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
