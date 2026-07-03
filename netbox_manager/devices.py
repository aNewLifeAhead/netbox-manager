import csv
from pathlib import Path


WALLPLATES_CSV = Path("data/wallplates.csv")


def sync_wallplates(nb, dry_run=False):
    """Create/update wall plate devices from data/wallplates.csv."""

    if not WALLPLATES_CSV.exists():
        raise FileNotFoundError(f"Missing CSV: {WALLPLATES_CSV}")

    with WALLPLATES_CSV.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"].strip()
            site_name = row["site"].strip()
            status = row.get("status", "active").strip().lower()
            location_name = row.get("location", "").strip()
            role_name = row["role"].strip()
            manufacturer_name = row["manufacturer"].strip()
            device_type_model = row["device_type"].strip()
            description = row.get("description", "").strip()

            site = nb.dcim.sites.get(name=site_name)
            role = nb.dcim.device_roles.get(name=role_name)
            manufacturer = nb.dcim.manufacturers.get(name=manufacturer_name)

            if not site:
                raise ValueError(f"Site not found: {site_name}")
            if not role:
                raise ValueError(f"Role not found: {role_name}")
            if not manufacturer:
                raise ValueError(f"Manufacturer not found: {manufacturer_name}")

            device_type = nb.dcim.device_types.get(
                model=device_type_model,
                manufacturer_id=manufacturer.id,
            )

            if not device_type:
                raise ValueError(f"Device type not found: {manufacturer_name} / {device_type_model}")

            location = None
            if location_name:
                matches = list(nb.dcim.locations.filter(name=location_name, site_id=site.id))
                if len(matches) == 0:
                    raise ValueError(f"Location not found: {location_name}")
                if len(matches) > 1:
                    raise ValueError(f"Multiple locations found: {location_name}")
                location = matches[0]

            payload = {
                "name": name,
                "status": status,
                "site": site.id,
                "role": role.id,
                "device_type": device_type.id,
                "description": description,
            }

            if location:
                payload["location"] = location.id

            existing = nb.dcim.devices.get(name=name, site_id=site.id)

            if existing:
                print(f"~ update {name}")
                if not dry_run:
                    existing.update(payload)
            else:
                print(f"+ create {name}")
                if not dry_run:
                    nb.dcim.devices.create(payload)