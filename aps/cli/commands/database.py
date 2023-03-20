import asyncio
import click


@click.group("database")
def aps_database():
    pass


@aps_database.command("init")
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    default=False,
)
def initialize_database(overwrite: bool):
    from aps.db.core import engine
    from aps.db.manage import init_database

    click.echo("Initializing new database...")

    asyncio.run(init_database(engine, overwrite=overwrite))

    click.secho("Success", fg="green")


@aps_database.command("drop")
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="silences all confirmation prompts",
)
def drop(yes: bool):
    from aps.db.core import engine
    from aps.db.manage import drop_database

    try:
        asyncio.run(drop_database(engine))
        click.secho("Success", fg="green")
    except Exception as e:
        click.secho(f"Database drop failed. Failure reason: \n{e}", fg="red")
