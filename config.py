import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEY = os.getenv('VERKADA_API_KEY')
ORG_ID = os.getenv('VERKADA_ORG_ID')
BASE_URL = 'https://api.verkada.com'

# Headers for every API request
HEADERS = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json'
}

# Monitoring Settings
CHECK_INTERVAL = 60  # Check every 60 seconds
OFFLINE_THRESHOLD = 2  # Alert after 2 failed checks