from netbox.plugins import PluginMenu, PluginMenuItem

menu = PluginMenu(
    label="NetBox Sync",
    groups=(
        (
            "Tools",
            (
                PluginMenuItem(
                    link="plugins:netbox_sync:home",
                    link_text="Device Type Sync",
                ),
            ),
        ),
    ),
    icon_class="mdi mdi-sync",
)
