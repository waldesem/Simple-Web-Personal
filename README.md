# StaffSec

StaffSec is a desktop webapp for managing local database.

### The technology stack used in this project:

- Flask;
- Sqlite;
- Vue;

### Installation

To use this project, you will need to have Python 3.12 or higher.

```
git clone https://github.com/waldesem/Simple-Web-Personal.git
cd Web-Personal-DB/server_flask
wget -qO- https://astral.sh/uv/install.sh | sh
uv venv
uv sync
```

### Settings

You need creating settings.ini file run with:

```
[Destination]
path =
```

Where path is a destination for files share.

DEFAULT_PASSWORD for created user is `88888888`.

### Cli

Use this command for help.
```
python3 command.py --help
```

### Build frontend

First install Node.js. Then run in terminal:

```
cd Simple_Web-Personal/web_vue
npm i
```

To build app:

```
npm run build
```

Builded files can be found in `server_flask/app/static`.

### Start webapp

To start server run the command in terminal:

```
uv run webgui.py
```
