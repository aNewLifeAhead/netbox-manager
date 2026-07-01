import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netbox.settings")
django.setup()

from dcim.models import (
    Device,
    DeviceType,

    InterfaceTemplate,
    ConsolePortTemplate,
    ConsoleServerPortTemplate,
    PowerPortTemplate,
    PowerOutletTemplate,
    RearPortTemplate,
    FrontPortTemplate,
    ModuleBayTemplate,
    DeviceBayTemplate,

    Interface,
    ConsolePort,
    ConsoleServerPort,
    PowerPort,
    PowerOutlet,
    RearPort,
    FrontPort,
    ModuleBay,
    DeviceBay,
)


DEVICE_TYPE_NAME = "Ubiquiti Edgeswitch POE+ 48 (750W)"
DRY_RUN = True


SIMPLE_COMPONENTS = [
    (InterfaceTemplate, Interface),
    (ConsolePortTemplate, ConsolePort),
    (ConsoleServerPortTemplate, ConsoleServerPort),
    (PowerPortTemplate, PowerPort),
    (PowerOutletTemplate, PowerOutlet),
    (ModuleBayTemplate, ModuleBay),
    (DeviceBayTemplate, DeviceBay),
    (RearPortTemplate, RearPort),
]


def copy_fields(template, target_model, device):
    data = {
        "device": device,
        "name": template.name,
    }

    target_fields = {f.name for f in target_model._meta.fields}
    skip = {
        "id",
        "created",
        "last_updated",
        "device",
        "module",
        "device_type",
        "module_type",
    }

    for field in template._meta.fields:
        name = field.name

        if name in skip:
            continue

        if name not in target_fields:
            continue

        data[name] = getattr(template, name)

    return data


def sync_simple_component(device, template_model, target_model):
    created = 0

    templates = template_model.objects.filter(device_type=device.device_type)

    for template in templates:
        if target_model.objects.filter(device=device, name=template.name).exists():
            continue

        data = copy_fields(template, target_model, device)

        if DRY_RUN:
            print(f"  WOULD ADD {target_model.__name__}: {template.name}")
        else:
            target_model.objects.create(**data)
            print(f"  ADDED {target_model.__name__}: {template.name}")

        created += 1

    return created


def sync_front_ports(device):
    created = 0

    templates = FrontPortTemplate.objects.filter(device_type=device.device_type)

    for template in templates:
        if FrontPort.objects.filter(device=device, name=template.name).exists():
            continue

        rear_port = None

        if template.rear_port:
            rear_port = RearPort.objects.filter(
                device=device,
                name=template.rear_port.name,
            ).first()

            if not rear_port:
                print(f"  SKIP FrontPort {template.name}: missing rear port {template.rear_port.name}")
                continue

        data = copy_fields(template, FrontPort, device)
        data["rear_port"] = rear_port

        if DRY_RUN:
            print(f"  WOULD ADD FrontPort: {template.name}")
        else:
            FrontPort.objects.create(**data)
            print(f"  ADDED FrontPort: {template.name}")

        created += 1

    return created


def main():
    device_type = DeviceType.objects.get(model=DEVICE_TYPE_NAME)
    devices = Device.objects.filter(device_type=device_type)

    print(f"Device Type: {device_type}")
    print(f"Devices found: {devices.count()}")
    print(f"Dry run: {DRY_RUN}")
    print()

    total = 0

    for device in devices:
        print(f"{device.name}")

        device_total = 0

        for template_model, target_model in SIMPLE_COMPONENTS:
            device_total += sync_simple_component(device, template_model, target_model)

        # Front ports need rear ports to exist first.
        device_total += sync_front_ports(device)

        if device_total == 0:
            print("  Already up to date")

        total += device_total
        print()

    print(f"Total components {'that would be added' if DRY_RUN else 'added'}: {total}")


if __name__ == "__main__":
    main()