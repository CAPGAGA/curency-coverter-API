from dotenv import load_dotenv
from pathlib import Path
import os

# loading env

BASE_DIR = Path(__file__).resolve().parent

dotenv_path = os.path.join(BASE_DIR, 'dev.env')

load_dotenv(dotenv_path)

API_KEY = str(os.getenv('API_KEY'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_PORT = str(os.getenv('DB_PORT'))
DB_USERNAME = str(os.getenv('DB_USERNAME'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB = str(os.getenv('DB'))
