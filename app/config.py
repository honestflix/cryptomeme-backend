import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
COEL_API_URL = "https://api.corcel.io/v1/image/vision/text-to-image"

if not TOKEN:
    raise ValueError("API token is missing. Please set the TOKEN environment variable.")

def setup_logging():
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()
