# Crypto Meme Generator

This application generates crypto memes based on text prompts using a Hugging Face model and FastAPI.

## Features

- Generates images from text prompts.
- Utilizes the `CompVis/stable-diffusion-v-1-4` model from Hugging Face.
- FastAPI for serving the model.

## Requirements

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/honestflix/cryptomeme.git
   cd cryptomeme

2. Create a virtual environment:
    
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install the required packages:

   ```bash
   pip install -r requirements.txt


## Usage

1. Start the FastAPI server:
   
   ```bash
   uvicorn app.main:app --reload

2. The server will start at http://127.0.0.1:8000.

3. Send a POST request to http://127.0.0.1:8000/generate-meme with a JSON body containing the text prompt. For example:

   ```json
   {
    "text": "Bitcoin to the moon"
   }

4. The server will respond with a base64 encoded image string. You can decode and display this image in a web application or save it as a file.
