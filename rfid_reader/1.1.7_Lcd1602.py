#!/usr/bin/env python3

import LCD1602
import time
import json
import requests
import os
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# Initialize the RFID reader
reader = SimpleMFRC522()

# API endpoint
POST_URL = 'http://192.168.3.109:8000/record_attendance/'

# Define the timeout (in seconds)
TIMEOUT = 10

def setup_lcd():
    """Initialize the LCD display."""
    LCD1602.init(0x27, 1)  # Adjust according to your LCD
    LCD1602.write(0, 0, 'Ready...')
    LCD1602.write(1, 1, 'Place Card')

def update_lcd(line1, line2):
    """Update the LCD display with messages."""
    LCD1602.write(0, 0, line1)
    LCD1602.write(1, 1, line2)

def send_post_request(ic_no):
    """Send a POST request with the IC number in the JSON payload."""
    if not POST_URL:
        print("API_URL environment variable not set.")
        return

    # Clean up the IC number
    ic_no = str(ic_no).strip()

    payload = json.dumps({'ic_no': ic_no})
    headers = {'Content-Type': 'application/json'}

    print(f"Sending request: URL={POST_URL}, Payload={payload}, Headers={headers}")

    try:
        response = requests.post(POST_URL, data=payload, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()  # Raises HTTPError for bad responses
        response_data = response.json()  # Get JSON response
        print(f"Response: {response.status_code} - {response.text}")

        # Extract details from response
        message_line1 = response_data.get('employee', {}).get('full_name', 'Unknown')
        message_line2 = response_data.get('message', 'Error')

        # Update LCD with response
        update_lcd(message_line1, message_line2)

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        update_lcd('Request failed', str(e))

def main():
    setup_lcd()  # Initialize the LCD display
    while True:
        print("Reading...Please place the card...")
        id, text = reader.read()
        # Print raw ID and text read from the RFID
        print(f"Raw ID: {id}, Text: {text}")

        # Send the IC number in a POST request
        send_post_request(id)

        time.sleep(3)

def destroy():
    """Clean up GPIO pins and clear the LCD."""
    GPIO.cleanup()
    LCD1602.clear()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
