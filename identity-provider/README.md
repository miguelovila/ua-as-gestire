## About

This is a simple service that allows users to and login. It is built using [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQLite](https://www.sqlite.org/index.html). This service is intended to be used as prototype for a more complex service. You can access the service at this url: [http://127.0.0.1:5000/idp/profile/saml2/redirect/sso](http://127.0.0.1:5000/idp/profile/saml2/redirect/sso)

## TODO's

- [ ] Update the redirect url to the correct one.
- [ ] Add some visual feedback to the user when the login fails.
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
flask --app app.py --debug run
```
> Note: This command will prevent the server from creating a database if it does not exist.


### Handling the database

The passwords on the database are hashed and salted using the [bcrypt](https://en.wikipedia.org/wiki/Bcrypt) algorithm.