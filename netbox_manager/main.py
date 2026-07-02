import click
from netbox_manager.client import get_netbox


@click.group()
def cli():
    """NetBox Manager."""
    pass


@cli.command()
def test():
    """Test NetBox API connection."""
    nb = get_netbox()
    status = nb.status()

    click.echo("✅ Connected to NetBox")
    click.echo(f"Version: {status.get('netbox-version', 'unknown')}")


if __name__ == "__main__":
    cli()
