import logging
import os
from dotenv import load_dotenv
load_dotenv()
# Disable uvicorn access logger
# uvicorn_access = logging.getLogger("uvicorn.access")
# uvicorn_access.disabled = True
# logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%Y-%m-%d:%H:%M:%S')

logger = logging.getLogger("app")
logger.setLevel(logging.getLevelName(os.getenv('LOGGING_LEVEL')))
