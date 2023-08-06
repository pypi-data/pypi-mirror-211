__app_name__ = "translatesub"
__version__ = "0.1.0"

(
    SUCCESS,
    AZURE_CONFIG_ERROR,
    FFMPEG_ERROR,
) = range(3)

ERRORS = {
    AZURE_CONFIG_ERROR: "TRANSLATOR_TEXT_ENDPOINT, TRANSLATOR_TEXT_SUBSCRIPTION_KEY or TRANSLATOR_TEXT_REGION variables not defined",
    FFMPEG_ERROR: "ffmpeg or ffprobe not found in path",
}

import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()
load_dotenv(".env")