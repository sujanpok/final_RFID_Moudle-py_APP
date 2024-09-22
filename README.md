# RFID Reader Project

## Overview
This project is an **Employee Attendance System** that utilizes RFID technology to track and manage employee attendance. The system is built using Python and Django, and is designed to work with an RFID reader module. The project uses SQLite for database management and involves communication between a PC and a Raspberry Pi using JSON.

## Features
- **RFID Tag Reading**: Reads RFID tags to identify employees.
- **Attendance Logging**: Logs the attendance of employees in a SQLite database.
- **User Interface**: Provides a simple interface for managing and viewing attendance records.
- **Web Application**: Built using the Django framework for robust and scalable web development.
- **JSON Communication**: Sends and receives data between the PC and Raspberry Pi using JSON.

## Requirements
- **Hardware**:
  - RFID Reader Module (e.g., RC522)
  - RFID Tags
  - l2C LCD 1602 (for disply tag user name ...)
  - Raspberry Pi (or any compatible microcontroller)
  - PC for running the Django web application
  - Breadboard and Jumper Wires

- **Software**:
  - Python 3.x
  - Django
  - SQLite
  - Required Python libraries (e.g., `RPi.GPIO`, `MFRC522`, `requests`)

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/sujanpok/final_RFID_Moudle-py_APP.git
    cd final_RFID_Moudle-py_APP/rfid_reader
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the RFID reader application on Raspberry Pi**:
    ```bash
    python rfid_reader.py
    ```

## Django Web Application Setup
1. **Navigate to the Django project directory on your PC**:
    ```bash
    cd ../myproject
    ```

2. **Install Django and other dependencies as requied**:

3. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

4. **Run the Django development server**:
    ```bash
    python manage.py runserver
    ```

## Usage
1. **Connect the RFID reader** to your Raspberry Pi using the GPIO pins.
2. **Run the RFID reader application** on the Raspberry Pi using the command mentioned above.
3. **Access the Django web application** at `http://localhost:8000` on your PC to manage and view attendance records.
4. **Scan RFID tags** to log attendance. The data will be sent from the Raspberry Pi to the PC using JSON.

## Code Explanation
The main script `rfid_reader.py` handles the reading of RFID tags and logging attendance. Here is a brief overview of the code:

- **Initialization**: Sets up the RFID reader and initializes the GPIO pins.
- **Main Loop**: Continuously checks for RFID tags and logs the attendance when a tag is detected.
- **Database Interaction**: Stores the attendance records in a SQLite database for later retrieval and analysis.
- **JSON Communication**: Sends attendance data from the Raspberry Pi to the Django web application on the PC using JSON.

The Django project, located in the `myproject` directory, provides a web interface for managing and viewing attendance records. It includes:

- **Models**: Defines the database schema for storing attendance records.
- **Views**: Handles the logic for displaying attendance data and managing records.
- **Templates**: Provides the HTML templates for the web interface.

## Contributing
Feel free to fork this repository and contribute by submitting pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments
- Thanks to the open-source community for providing the libraries and tools used in this project.
