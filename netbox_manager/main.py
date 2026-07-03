import click

from netbox_manager.client import get_netbox
from netbox_manager.devices import sync_wallplates


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

    nb = get_netbox()
    status = nb.status()

    click.echo("✅ Connected to NetBox")
    click.echo(f"Version : {status.get('netbox-version', 'Unknown')}")


# --------------------------------------------------------------------
# Sync commands
# --------------------------------------------------------------------

@cli.group()
def sync():
    """Synchronise CSV data into NetBox."""
    pass


@sync.command("wallplates")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be changed without writing to NetBox."
)
def sync_wallplates_command(dry_run):
    """Import wall plates."""

    nb = get_netbox()

    sync_wallplates(
        nb,
        dry_run=dry_run,
    )


if __name__ == "__main__":
    cli()