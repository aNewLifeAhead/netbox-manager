from netbox.plugins import PluginConfig


class NetBoxSyncConfig(PluginConfig):
    name = "netbox_sync"
    verbose_name = "NetBox Sync"
    description = "Custom NetBox sync utilities"
    version = "0.1.0"
    base_url = "https://github.com/aNewLifeAhead/netbox-sync"


config = NetBoxSyncConfig
