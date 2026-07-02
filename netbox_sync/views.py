from django.shortcuts import render


def home(request):
    return render(request, "netbox_sync/home.html")
