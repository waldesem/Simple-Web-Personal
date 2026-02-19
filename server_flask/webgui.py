"""WebGUI module."""

from __future__ import annotations

import shutil
import signal
import subprocess
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psutil

from app import create_app


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
                "--disable-extensions",
                "--new-window",
                "--no-default-browser-check",
                "--no-first-run",
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


def serve(host: str = "127.0.0.1", port: int = 5000) -> None:
    """Run the application based on the provided arguments."""
    app = create_app()
    with ThreadPoolExecutor(max_workers=2) as executor:
        server_future = executor.submit(app.run, host, port)
        browser_future = executor.submit(start_browser, host, port)
        try:
            server_future.result()
            browser_future.result()
        except KeyboardInterrupt:
            executor.shutdown()


if __name__ == "__main__":
    serve()
