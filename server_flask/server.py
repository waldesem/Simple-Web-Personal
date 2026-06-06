"""Start server module."""

from app import create_app


def main(host: str = "127.0.0.1", port: int = 5000, *, debug: bool = False) -> None:
    """Run the server based on the provided arguments."""
    app = create_app()
    app.run(host, port, debug=debug)


if __name__ == "__main__":
    main()
