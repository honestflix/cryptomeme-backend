# Crypto Meme Generator

This application generates crypto memes based on text prompts using a commune model and FastAPI.

## Requirements

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/honestflix/cryptomeme-backend.git
   cd cryptomeme-backend

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

3. Send a POST request to http://127.0.0.1:8000/meme with a JSON body containing the text prompt. For example:

   ```bash
   curl -X 'POST' \
   'http://148.251.90.176/meme/' \
   -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{
   "type": "txt2img",
   "prompt": "Toronto sunset",
   "width": 512,
   "height": 512,
   "init_image": ""
   }'
   ```

