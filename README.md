# StaffSec

StaffSec is a desktop webapp for managing local database.

## The technology stack used in this project

- Flask;
- Pydantic(legacy);
- Sqlite;
- Vue3;
- NuxtUi;

## Installation

To use this project, you will need to have Python 3.11.

```bash
git clone https://github.com/waldesem/Simple-Web-Personal.git
cd Web-Personal-DB/server_flask
wget -qO- https://astral.sh/uv/install.sh | sh
uv sync
```

## Settings

All app options contains in settings.ini.
For server mode change login variable in true and change default password if needs.

To create full-text search run:

```bash
uv run fts.py
```

## Build frontend (Optional)

First install Node.js. Then run in terminal:

```bash
cd Simple_Web-Personal/web_vue
npm i
npm run build
```

Builded files can be found in `server_flask/app/static`.

## Start

To start app run the command in terminal:

```bash
uv run main.py
```
