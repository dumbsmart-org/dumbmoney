import sys

# Don't write .pyc files
sys.dont_write_bytecode = True

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file if present