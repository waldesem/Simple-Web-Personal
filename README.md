# StaffSec

StaffSec is a desktop webapp for managing local database.

## The technology stack used in this project

- Flask;
- Pydantic(legacy);
- Sqlite;
- Vue3;
- NuxtUi;

## Installation

To use this project, you will need to have Python 3.11 or higher.

```bash
git clone https://github.com/waldesem/Simple-Web-Personal.git
cd Web-Personal-DB/server_flask
wget -qO- https://astral.sh/uv/install.sh | sh
uv sync
```

## Settings

You need creating settings.ini file with:

```ini
[Destination]
path=
```

Where path is a destination for files share.

DEFAULT_PASSWORD for created user is `88888888`.

## Build frontend (Optional)

First install Node.js. Then run in terminal:

```bash
cd Simple_Web-Personal/web_vue
npm i
npm run build
```

Builded files can be found in `server_flask/app/static`.

## Start

To start server run the command in terminal:

```bash
uv run server.py
```

or as desktop app:

```bash
uv run webgui.py
```
