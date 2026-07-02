import os
import pynetbox
from dotenv import load_dotenv


def get_netbox():
    load_dotenv()

    url = os.getenv("NETBOX_URL")
    token = os.getenv("NETBOX_TOKEN")
    verify_ssl = os.getenv("VERIFY_SSL", "true").lower() == "true"

    if not url or not token:
        raise RuntimeError("NETBOX_URL and NETBOX_TOKEN must be set in .env")

    nb = pynetbox.api(url, token=token)
    nb.http_session.verify = verify_ssl
    return nb
