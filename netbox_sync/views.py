from io import StringIO

from django.core.management import call_command
from django.shortcuts import render


def home(request):
    output = None

    if request.method == "POST":
        commit = request.POST.get("commit") == "on"

        buffer = StringIO()

        call_command(
            "sync_device_type_components",
            stdout=buffer,
            commit=commit,
        )

        output = buffer.getvalue()

    return render(request, "netbox_sync/home.html", {
        "output": output,
    })
