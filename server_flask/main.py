"""Main file."""

from __future__ import annotations

import shutil
import signal
import subprocess
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import click
import psutil

from app import create_app
from config import Config


def start_browser(address: str, port: int) -> None:
    """Start the browser."""
    profile_dir = tempfile.mkdtemp(prefix=f"webgui{uuid.uuid1().hex}")
    paths = [
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/snap/bin/chromium",
    ]
    if browser_path := next((p for p in paths if Path(p).is_file()), None):
        subprocess.Popen(  # noqa: S603
            [
                browser_path,
                f"--app=http://{address}:{port}",
                f"--user-data-dir={profile_dir}",
                "--new-window",
                "--no-first-run",
                "--disable-extensions",
                "--no-default-browser-check",
                "--window-size=1280,960",
            ],
        ).wait()

    shutil.rmtree(profile_dir, ignore_errors=True)
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                psutil.Process(conn.pid).send_signal(signal.SIGTERM)
            except psutil.AccessDenied:
                continue
            break


@click.command()
@click.option("--host", default="localhost", help="The hostname to listen on")
@click.option("--port", default=5000, help="The port of the webserver")
def main(host: str, port: int) -> None:
    """Start point of the programme."""
    app = create_app()
    if Config.AUTH:
        app.run(host=host, port=port)
    else:
        with ThreadPoolExecutor(max_workers=2) as executor:
            server_future = executor.submit(app.run, host, port)
            browser_future = executor.submit(start_browser, host, port)
            try:
                server_future.result()
                browser_future.result()
            except KeyboardInterrupt:
                executor.shutdown()


if __name__ == "__main__":
    main()
