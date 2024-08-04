import requests
import time
from mfrc522 import SimpleMFRC522 # type: ignore
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize RFID reader
reader = SimpleMFRC522()

# Get the API endpoint from environment variables
api_url = os.getenv('API_URL')

if not api_url:
    raise ValueError("API_URL not found in environment variables")

def read_rfid():
    try:
        while True:
            print("Hold an RFID card near the reader")
            id, _ = reader.read()
            print(f"IC No: {id}")

            # Send IC number to the Django API
            response = requests.post(api_url, data={'ic_no': id})
            print(response.json())

            # Add a short delay to avoid excessive reading
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated")

if __name__ == "__main__":
    read_rfid()
