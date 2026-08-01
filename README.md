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
[Options]
path=C:\Users\Projects\PersonalDB
login=false
```

For server mode change login variable in true.

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

To start app run the command in terminal:

```bash
uv run main.py
```
