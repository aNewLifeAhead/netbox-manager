cat > netbox_manager/netbox_lookup.py << 'EOF'
def get_required(endpoint, label, **filters):
    obj = endpoint.get(**filters)

    if obj is None:
        rendered = ", ".join(f"{k}={v}" for k, v in filters.items())
        raise ValueError(f"{label} not found: {rendered}")

    return obj


def get_unique_location(nb, name, site_id):
    matches = list(
        nb.dcim.locations.filter(
            name=name,
            site_id=site_id,
        )
    )

    if len(matches) == 0:
        raise ValueError(f"Location not found: {name}")

    if len(matches) > 1:
        raise ValueError(f"Multiple locations found: {name}")

    return matches[0]
EOF