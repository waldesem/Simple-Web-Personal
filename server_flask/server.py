"""Start server module."""

from app import create_app


def main() -> None:
    """Run the server based on the provided arguments."""
    app = create_app()
    app.run("127.0.0.1", 5000, debug=False)


if __name__ == "__main__":
    main()
