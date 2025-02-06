# YouTube Captions API

Simply send a POST request to the URL below with the ID of the video you want to get captions for as a parameter.

## Start the gunicorn server

Use the following command to start the server:

```shell
gunicorn --config gunicorn_config.py main:app
```

Or run the development server using Flask:

```shell
python3 main.py
```

## Send a request

Use the following curl command to send a POST request:

```shell
curl -X POST "http://0.0.0.0:8080/transcript/?video_id=XeFOzxozypY"
```
