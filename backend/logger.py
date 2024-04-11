import logging
import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger("app")
logger.setLevel(logging.getLevelName(os.getenv('LOGGING_LEVEL')==None and 'INFO' or os.getenv('LOGGING_LEVEL')))
