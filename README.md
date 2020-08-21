## Serverles CRUD app

> Flask application running into severless environment

# Usage

Local installation:

```sh
$ poetry install
```

To run tests:
```sh
$ poetry run pytest app_test.py -vv
```

Deploy the app typing:
```sh
$ sls deploy
```

Run a command to install DynamoDB local:
```sh
$ sls dynamodb install
```

Let's see it if works. You'll need two different terminal windows now. In your first window, start up DynamoDB local:

```sh
$ sls dynamodb start
```

In the second window, start up your local WSGI server:
```sh
$ sls wsgi serve
```
