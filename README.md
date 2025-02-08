# YouTube Captions API

## Start the gunicorn server

Use the following command to start the server:

```shell
gunicorn --config config/gunicorn_config.py app:app
```

Or run the development server using Flask:

```shell
python3 main.py
```

## Send a request

Use the following curl command to send a POST request:

```shell
python3 request.py
```
