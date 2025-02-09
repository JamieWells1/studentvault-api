# YouTube Captions API

This is a proprietary API designed to retrieve captions from YouTube videos using the YouTube Transcript API. This API allows you to send a request with a YouTube video ID, and it will return the captions for that video.

## Setup Instructions

### Prerequisites

- Python 3.13
- Required Python packages (listed below)
- A working YouTube video ID with captions enabled

Install the required dependencies using pip:

```shell
pip install -r requirements.txt
```

### Environment Variables

This API requires specific environment variables to run. Ensure you have the following set up:

- `PROXY`: The proxy URL for accessing external resources.
- `OPENAI_API_KEY`: The API key for OpenAI access (if needed for future enhancements).

These variables can be set in your environment or stored in a `.env` file (using the `python-dotenv` package to load them).

## Running the Server

### Gunicorn Server (Recommended for Production)

To start the production server, use the following command:

```shell
gunicorn --config config/gunicorn_config.py app:app
```

This will launch the server using Gunicorn, which is optimized for handling production traffic.

### Flask Development Server

For development purposes, you can run the server with Flask:

```shell
python3 main.py
```

This starts the development server, which is useful for testing and debugging.

## Sending a Request

### Using Curl

You can send a POST request to the API to retrieve captions for a YouTube video. Use the following command:

```shell
python3 request.py
```

Make sure that `request.py` is set up with the correct data, including the `video_id` of the YouTube video for which you want to retrieve captions.

### API Request Structure

The API expects a POST request at the endpoint `/create-with-ai/` with the following JSON payload:

```json
{
  "video_id": "uNeyu46JtIk",
  "generation_method": "video",
  "text_prompt": "",
  "resource_type": "lesson"
}
```

- `video_id`: The YouTube video ID (required).
- `generation_method`: Defines the type of resource to generate (e.g., "video").
- `text_prompt`: Optional text prompt for AI generation (can be left empty).
- `resource_type`: The type of resource to generate (e.g., "lesson").

### Response

The API will return a JSON response with the following structure:

```json
{
  "status": 200,
  "captions": "The full transcript of the video...",
  "errors": []
}
```

- `status`: The HTTP status code (200 for success).
- `captions`: A string containing the captions from the video.
- `errors`: Any error messages if the request fails.

### Error Handling

If there's an issue with retrieving captions (e.g., invalid URL, video doesn't support captions), the API will return a `400` status code with error details:

```json
{
  "status": 400,
  "errors": [
    "The video URL you provided either isn't a valid URL or the video doesn't support captions."
  ]
}
```

## Code Overview

- **`app.py`**: The main Flask application file that handles incoming requests and sends responses.
- **`youtube.py`**: Contains the `Youtube` class, which interacts with the YouTube Transcript API to fetch captions.
- **`request.py`**: A script for sending test requests to the API.
- **`gunicorn_config.py`**: Configuration for running the app with Gunicorn in a production environment.
- **`response_objects.py`**: Defines data structures (e.g., Pydantic models) for handling responses.

## License

This project is proprietary and for personal use only. Unauthorized use, duplication, or distribution is prohibited.
