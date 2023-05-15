## About

This is the main service. It is built using [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQLite](https://www.sqlite.org/index.html). This service is intended to main service. You can access the service at this url: [http://127.0.0.1:5001](http://127.0.0.1:5001)

## TODO's

- [ ] Create the database schema and the models.
- [ ] Create the routes for the service (token generation, listing rooms, etc).
- [ ] Create the tests for the service.
- [ ] Create the container image for the service.

## Developing

### Setting up the environment

In order to extract the dependencies from the code, run the following command:

```bash
pipreqs ./ --force --ignore=.venv --encoding utf-8
```

In order to install all the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Running the server

In order to run the server, run the following command:

```bash
python app.py
```

In order to run the server with hot reloading, run the following command:

```bash
flask --app app.py --debug run -p 5001
```
> Note: This command will prevent the server from creating a database if it does not exist.


### Handling the database

No passwords will be stored in this database. The database will be used to store the rooms, equipments, the users and their respective tokens.