from netbox.plugins import PluginConfig


class NetBoxSyncConfig(PluginConfig):
    name = "netbox_sync"
    verbose_name = "NetBox Sync"
    description = "Device Type component synchronisation tool for NetBox"
    version = "0.1.1"
    author = "Charles Wright"
    author_email = "charlie@fix8group.com"
    base_url = "https://github.com/aNewLifeAhead/netbox-sync"


config = NetBoxSyncConfig
