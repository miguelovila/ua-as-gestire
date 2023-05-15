# Developing

## Setting up the environment

In order to extract the dependencies from the code, run the following command:

```bash
pipreqs ./ --force --ignore=.venv --encoding utf-8
```

In order to install all the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Running the server

In order to run the server, run the following command:

```bash
python app.py
```

In order to run the server with hot reloading, run the following command:

```bash
flask --app app.py --debug run
```
> Note: This command will prevent the server from creating a database if it does not exist.


# Handling the database

The passwords on the database are hashed and salted using the [bcrypt](https://en.wikipedia.org/wiki/Bcrypt) algorithm.