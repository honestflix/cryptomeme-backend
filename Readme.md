# Meme Generator API

## Description
A FastAPI-based web service for generating memes using a text-to-image API.

## Setup
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory and add your API token:
    ```
    TOKEN=your_api_token_here
    ```
5. Run the application:
    ```
    uvicorn app.main:app --reload
    ```

## Endpoints
- `POST /generate`: Generates an image based on the provided text prompt.

## Example Request
```json
{
    "text": "Bitcoin to the moon",
    "cfg_scale": 2,
    "height": 1024,
    "width": 1024,
    "steps": 8,
    "engine": "proteus"
}
