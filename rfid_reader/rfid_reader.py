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
    """Initialize the LCD display with 'Ready...' and 'Place Card'."""
    LCD1602.init(0x27, 1)  # Adjust according to your LCD
    LCD1602.write(0, 0, 'Ready...')
    LCD1602.write(1, 1, 'Place Card')

def scroll_text(line, col, text):
    """Scroll the given text from right to left on the specified line and column if it's longer than 16 characters."""
    if len(text) > 16:
        for i in range(len(text) + 16):
            display_text = text[i:i + 16].ljust(16)
            LCD1602.write(line, col, display_text)
            time.sleep(0.005)  # Reduced sleep time
    else:
        LCD1602.write(line, col, text.ljust(16))

def update_lcd(greeting, name):
    """Update the LCD display with a scrolling greeting on the first line and name on the second line."""
    greeting_length = len(greeting)
    name_length = len(name)
    print(f"Greeting length: {greeting_length}, Name length: {name_length}")

    max_length = max(greeting_length, name_length)
    for i in range(max_length + 16):
        greeting_display = greeting[i:i + 16].ljust(16) if greeting_length > 16 else greeting.ljust(16)
        name_display = name[i:i + 16].ljust(16) if name_length > 16 else name.ljust(16)
        LCD1602.write(0, 0, greeting_display)
        LCD1602.write(1, 1, name_display)
        time.sleep(0.05)  # Reduced sleep time

    # Wait for 1 seconds before resetting to 'Ready...'
    #time.sleep(1)
    setup_lcd()

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
        full_name = response_data.get('employee', {}).get('full_name', 'Unknown')
        #employee_id = response_data.get('employee', {}).get('employee_id', 'No ID')
        status = response_data.get('employee', {}).get('status', 'I')  # Default to 'I' if not found

        # Determine the greeting based on status
        if status == "O":
            greeting = "Have a good Day"
        elif status == "I":
            greeting = "Good Morning"
        else:
            greeting = "Hello"

        # Update LCD with greeting and employee name
        update_lcd(greeting, full_name)

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        update_lcd('Request failed', 'Error')

def main():
    setup_lcd()  # Initialize the LCD display
    while True:
        print("Reading...Please place the card...")
        id, text = reader.read()
        # Print raw ID and text read from the RFID
        print(f"Raw ID: {id}, Text: {text}")

        # Send the IC number in a POST request
        send_post_request(id)

def destroy():
    """Clean up GPIO pins and clear the LCD."""
    GPIO.cleanup()
    LCD1602.clear()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
