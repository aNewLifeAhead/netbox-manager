import html
import subprocess

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


NETBOX_MANAGER_PATH = "/opt/netbox-manager"
NETBOX_MANAGER_PYTHON = "/opt/netbox-manager/.venv/bin/python"


def _run_command(command):
    result = subprocess.run(
        command,
        cwd=NETBOX_MANAGER_PATH,
        text=True,
        capture_output=True,
        timeout=300,
    )

    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += "\n--- STDERR ---\n" + result.stderr

    return result.returncode, output.strip()


@login_required
@require_http_methods(["GET", "POST"])
def sync_wallplates_view(request):
    if not request.user.is_superuser:
        return HttpResponse("Permission denied", status=403)

    output_sections = []
    dry_run = True

    if request.method == "POST":
        dry_run = request.POST.get("dry_run", "on") == "on"

        commands = [
            ["git", "pull", "origin", "main"],
            [NETBOX_MANAGER_PYTHON, "-m", "netbox_manager.main", "sync", "wallplates"]
            + (["--dry-run"] if dry_run else []),
        ]

        for command in commands:
            returncode, output = _run_command(command)
            output_sections.append(
                f"$ {' '.join(command)}\n{output}\n\nReturn code: {returncode}"
            )
            if returncode != 0:
                break

    checked = "checked" if dry_run else ""
    output_html = html.escape("\n\n".join(output_sections))

    return HttpResponse(
        f"""
        <!doctype html>
        <html>
        <head>
            <title>Sync Wallplates</title>
            <style>
                body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
                pre {{ background: #111; color: #eee; padding: 1rem; border-radius: 8px; white-space: pre-wrap; }}
                button {{ padding: 0.5rem 1rem; font-size: 1rem; }}
                .warning {{ color: #b45309; font-weight: 600; }}
            </style>
        </head>
        <body>
            <h1>Sync Wallplates</h1>
            <p>This pulls the latest <code>netbox-manager</code> from Git, then runs the wallplate workbook sync.</p>
            <form method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                <p>
                    <label>
                        <input type="checkbox" name="dry_run" {checked}>
                        Dry run only
                    </label>
                </p>
                <p class="warning">Untick dry run only when you are ready to write changes into NetBox.</p>
                <button type="submit">Run Sync</button>
            </form>
            <h2>Output</h2>
            <pre>{output_html}</pre>
        </body>
        </html>
        """
    )