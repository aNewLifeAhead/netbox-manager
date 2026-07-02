from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    help = "Sync missing components from Device Type templates to existing devices."

    def add_arguments(self, parser):
        parser.add_argument("--commit", action="store_true", help="Actually create missing components.")
        parser.add_argument("--device-type", help="Only sync one Device Type model name.")

    def copy_fields(self, template, target_model, device):
        data = {"device": device, "name": template.name}
        target_fields = {f.name for f in target_model._meta.fields}
        skip = {
            "id", "created", "last_updated",
            "device", "module", "device_type", "module_type",
        }

        for field in template._meta.fields:
            name = field.name
            if name in skip or name not in target_fields:
                continue
            data[name] = getattr(template, name)

        return data

    def sync_simple_component(self, device, template_model, target_model, commit):
        created = 0
        templates = template_model.objects.filter(device_type=device.device_type)

        for template in templates:
            if target_model.objects.filter(device=device, name=template.name).exists():
                continue

            data = self.copy_fields(template, target_model, device)

            if commit:
                target_model.objects.create(**data)
                self.stdout.write(f"  ADDED {target_model.__name__}: {template.name}")
            else:
                self.stdout.write(f"  WOULD ADD {target_model.__name__}: {template.name}")

            created += 1

        return created

    def sync_front_ports(self, device, commit):
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
                    self.stdout.write(
                        f"  SKIP FrontPort {template.name}: missing rear port {template.rear_port.name}"
                    )
                    continue

            data = self.copy_fields(template, FrontPort, device)
            data["rear_port"] = rear_port

            if commit:
                FrontPort.objects.create(**data)
                self.stdout.write(f"  ADDED FrontPort: {template.name}")
            else:
                self.stdout.write(f"  WOULD ADD FrontPort: {template.name}")

            created += 1

        return created

    def handle(self, *args, **options):
        commit = options["commit"]
        device_type_name = options.get("device_type")

        if device_type_name:
            device_types = DeviceType.objects.filter(model=device_type_name)
        else:
            device_types = DeviceType.objects.all().order_by("manufacturer__name", "model")

        grand_total = 0

        for device_type in device_types:
            devices = Device.objects.filter(device_type=device_type)

            if not devices.exists():
                continue

            self.stdout.write(f"Device Type: {device_type}")
            self.stdout.write(f"Devices found: {devices.count()}")
            self.stdout.write(f"Dry run: {not commit}\n")

            total = 0

            for device in devices:
                identifier = device.name or device.asset_tag or f"Device #{device.pk}"
                self.stdout.write(identifier)

                device_total = 0

                for template_model, target_model in SIMPLE_COMPONENTS:
                    device_total += self.sync_simple_component(
                        device, template_model, target_model, commit
                    )

                device_total += self.sync_front_ports(device, commit)

                if device_total == 0:
                    self.stdout.write("  Already up to date")

                total += device_total
                self.stdout.write("")

            self.stdout.write(f"Total for {device_type}: {total}")
            self.stdout.write("-" * 60)
            grand_total += total

        self.stdout.write(
            f"Grand total components {'added' if commit else 'that would be added'}: {grand_total}"
        )
