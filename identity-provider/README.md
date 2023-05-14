# Developing

In order to extract the dependencies from the code, run the following command:

```bash
pipreqs ./ --force --ignore=.venv --encoding utf-8
```

In order to install all the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

# :warning: Attention! :warning:

The passwords on the database are stored in plain text. This is a security issue and should be fixed in the future. The passwords should be hashed and salted. For now, just be careful with the database and don't share it with anyone.
