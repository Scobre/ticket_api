# App - BACK

## Installation

*The project work with python3.12*

### In local

Create your venv and activate it :
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the dependencies with the command :
```bash
pip install -r requirements.txt
```

Optionally, create an env file based on the template :
```bash
cp .env.example .env
```

Then run the server :
 ```bash
# in development mode
fastapi dev main.py

# in production mode
fastapi run main.py
```

### With docker

Create an env file :
```bash
cp .env.example .env
```

Then run the docker with the command :
```bash
docker-compose up -d
```

*PS : those 2 commands can be run with the command :*
```bash
./start.sh
```

## Environnement

An env file is required. Here the detail of the keys :
```bash
# the engine of the database. default : sqlite
DATABASE_ENGINE=
# the url of the database. default : sqlite:///./db/sql_app.db
DATABASE_URL=
# the environement of the app. Possible values : dev | test | preproduction | production. default : dev
FASTAPI_ENV=
# the title of the app. default : Ticket - API
FASTAPI_TITLE=
```

## Tests Unitaires

To run all the test :
```bash
pytest
```

To run the test and get the coverage report in html mode :
```bash
pytest --cov-report html
```
