"""Console script for epss."""
import sys
import click
from .epss import EPSS,Status

@click.command()
def main(args=None):
    """Console script for epss."""
    click.echo("Replace this message by putting your code into "
               "epss.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
