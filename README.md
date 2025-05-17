# StudentVault API Endpoints

This repository contains the API endpoints for the StudentVault platform, designed to handle resource generation, flashcard extraction, image generation, search functionality, and more. Below is a comprehensive guide to all the available endpoints, their functionality, and usage.

---

## Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [Endpoints Overview](#endpoints-overview)
   - [Resource Functionality](#resource-functionality)
   - [Chat Functionality](#chat-functionality)
   - [Search/Memory Functionality](#searchmemory-functionality)
   - [Cache Management](#cache-management)
   - [Utility Endpoints](#utility-endpoints)
3. [Error Handling](#error-handling)
4. [License](#license)

---

## Setup Instructions

### Prerequisites

- Python 3.13
- Install dependencies using:

```bash
pip install -r requirements.txt
```

### Environment Variables

Ensure the following environment variables are set:

- `OPENAI_API_KEY`: API key for OpenAI.
- `REPLICATE_API_KEY`: API key for Replicate.
- `STUDENTVAULT_API_KEY`: Authentication key for cache management.

---

## Endpoints Overview

### Resource Functionality

#### 1. **Create AI Resource**

- **Endpoint**: `/create-with-ai/`
- **Method**: `POST`
- **Description**: Generates AI-based resources such as lessons, quizzes, or flashcard decks.
- **Request Body**:

```json
{
  "video_id": "uNeyu46JtIk",
  "generation_method": "video",
  "text_prompt": "",
  "resource_type": "lesson",
  "lesson_type": "twelve_blocks"
}
```

- **Response**:

```json
{
  "status": 200,
  "resource_type": "lesson",
  "payload": {}
}
```

#### 2. **Extract Flashcards**

- **Endpoint**: `/extract-flashcards/`
- **Method**: `POST`
- **Description**: Extracts flashcards from a provided text body.
- **Request Body**:

```json
{
  "body": "What is another name for stocks/shares? - Equities; ..."
}
```

- **Response**:

```json
[{ "front": "What is another name for stocks/shares?", "back": "Equities" }, {}]
```

#### 3. **Generate Image**

- **Endpoint**: `/generate-image/`
- **Method**: `POST`
- **Description**: Generates an AI-based image using Replicate.
- **Request Body**:

```json
{
  "topic": "Hooke's Law",
  "custom_prompt": "A car suspension system absorbing impact.",
  "prompt_type": "topic"
}
```

- **Response**:

```json
{
  "status": 200,
  "image_url": "https://example.com/image.webp"
}
```

---

### Chat Functionality

#### 4. **Answer Question**

- **Endpoint**: `/answer-question/`
- **Method**: `POST`
- **Description**: Provides an AI-generated answer to a question based on a lesson context.
- **Request Body**:

```json
{
  "question": "What is photosynthesis?",
  "lesson_context": "{...}"
}
```

- **Response**:

```json
{
  "status": 200,
  "payload": {
    "explanation": "...",
    "practice_question": {},
    "follow_up_output": "Would you like me to create some flashcards on this for you?"
  }
}
```

---

### Search/Memory Functionality

#### 5. **Search**

- **Endpoint**: `/search/`
- **Method**: `POST`
- **Description**: Searches for items in the database cache.
- **Request Body**:

```json
{
  "table": "ai_quiz",
  "query": "physics resistivity",
  "bucket_size": 5
}
```

- **Response**:

```json
[{ "unique_id": "12345", "title": "Physics Quiz", "score": 95 }, {}]
```

---

### Cache Management

#### 6. **Update Cache**

- **Endpoint**: `/update-cache/`
- **Method**: `POST`
- **Description**: Updates an entry in the database cache.
- **Request Body**:

```json
{
  "table": "lesson",
  "unique_id": "12345",
  "title": "Updated Lesson Title"
}
```

- **Headers**:
  - `X-StudentVault-Key`: Authentication key.
- **Response**:

```json
{
  "status": 200,
  "message": "Entry updated successfully"
}
```

#### 7. **Delete Item**

- **Endpoint**: `/delete-item/`
- **Method**: `POST`
- **Description**: Deletes an entry from the database cache.
- **Request Body**:

```json
{
  "table": "lesson",
  "unique_id": "12345",
  "title": "Lesson to Delete"
}
```

- **Headers**:
  - `X-StudentVault-Key`: Authentication key.
- **Response**:

```json
{
  "status": 200,
  "message": "Entry deleted successfully"
}
```

#### 8. **Force Sync**

- **Endpoint**: `/force-sync/`
- **Method**: `GET`
- **Description**: Forces a manual sync of the database cache.
- **Headers**:
  - `X-StudentVault-Key`: Authentication key.
- **Response**:

```json
{
  "status": 200,
  "message": "Data synced to cache successfully"
}
```

---

### Utility Endpoints

#### 9. **Get Captions**

- **Endpoint**: `/get-captions/`
- **Method**: `POST`
- **Description**: Retrieves captions for a YouTube video.
- **Request Body**:

```json
{
  "video_id": "MmgxJZeMCSc"
}
```

- **Response**:

```json
{
  "status": 200,
  "captions": "Full transcript of the video...",
  "errors": []
}
```

#### 10. **Show Cache**

- **Endpoint**: `/show-cache/`
- **Method**: `POST`
- **Description**: Displays the contents of the database cache.
- **Query Parameters**:
  - `table`: (Optional) The specific table to display.
- **Response**:

```json
{
  "module": {  },
  "lesson": {  },
  {  }
}
```

---

## Error Handling

- **400 Bad Request**: Returned for invalid input or unauthenticated requests.
- **500 Internal Server Error**: Returned for unexpected server errors.

Example error response:

```json
{
  "status": 400,
  "errors": ["Invalid video ID"]
}
```

---

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
