import click

from aps.cli.application import Application
from aps.cli.commands.database import aps_database
from aps.cli.commands.extract import aps_extract
from aps.logging import configure_logging


def _init():
    configure_logging()


@click.group(
    context_settings={"help_option_names": ["h", "--help"]},
    invoke_without_command=True,
)
@click.pass_context
def cli(ctx):
    _init()

    app = Application()
    ctx.obj = app
    
    if not ctx.invoked_subcommand:
        print(ctx.get_help())
        return

cli.add_command(aps_database)
cli.add_command(aps_extract)


def main() -> int:
    return cli()
