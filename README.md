# StaffSec

StaffSec is a desktop webapp for managing local database.

### The technology stack used in this project:

- Flask;
- Sqlite;
- Vue;

### Installation

To use this project, you will need to have Python 3.12 or higher.

```
git clone https://github.com/waldesem/Web-Personal-DB.git
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

For creating new user:

```
source .venv/bin/activate
```

DEFAULT_PASSWORD for created user is `88888888`.

### Cli

Use this command for help.
```
python3 command.py --help
```

### Build frontend

First install Node.js. Then run in terminal:

```
cd Web-Personal-DB/web_nuxt
npm i
```

To build Nuxt with Client-side Rendering:

```
npx nuxi generate
```

Builded files can be found in `server_flask/app/static`.

### Start backend server

To start server run the command in terminal:

```
uv run serve.py
```
