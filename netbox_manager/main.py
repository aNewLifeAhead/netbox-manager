import sys

import click

from netbox_manager.client import get_netbox
from netbox_manager.wallplates import sync_wallplates


@click.group()
def cli():
    """NetBox Manager"""
    pass


# --------------------------------------------------------------------
# Test API
# --------------------------------------------------------------------

@cli.command()
def test():
    """Test the NetBox API connection."""

    try:
        click.echo("Getting NetBox client...", err=True)
        nb = get_netbox()

        click.echo("Checking NetBox status...", err=True)
        status = nb.status()

        click.echo("✅ Connected to NetBox")
        click.echo(f"Version : {status.get('netbox-version', 'Unknown')}")
    except Exception as error:
        click.echo(f"❌ NetBox connection failed: {error}", err=True)
        raise SystemExit(1)


# --------------------------------------------------------------------
# Sync commands
# --------------------------------------------------------------------

@cli.group()
def sync():
    """Synchronise workbook data into NetBox."""
    pass


@sync.command("wallplates")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be changed without writing to NetBox.",
)
def sync_wallplates_command(dry_run):
    """Sync wall plates from the FIX8 Network workbook."""

    try:
        click.echo(">>> Entered sync_wallplates_command")
        click.echo(">>> Getting NetBox client")
        sys.stdout.flush()

        nb = get_netbox()

        click.echo(">>> Calling sync_wallplates")
        sys.stdout.flush()

        sync_wallplates(
            nb,
            dry_run=dry_run,
        )

        click.echo(">>> Finished sync_wallplates")
    except Exception as error:
        click.echo(f"❌ Wall plate sync failed: {error}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()