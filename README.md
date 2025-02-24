# Brainwave_Matrix_Intern
# ATM Web Application

## Overview
This is a simple ATM web application built using Flask. It allows users to log in with their account number and PIN, check their balance, deposit and withdraw money, change their PIN, and view their transaction history.

## Features
- User authentication with account number and PIN
- Account lock after multiple incorrect PIN attempts
- Deposit and withdraw functionality
- Transaction history display
- Change PIN option
- Secure session management

## Project Structure
```
atm_web_project/
│── app.py               # Flask backend (Python)
│── database.json        # Database for user accounts
│── requirements.txt     # Required dependencies
│── README.md            # Project documentation
│── static/
│   ├── style.css        # CSS for styling
│── templates/
│   ├── login.html       # Login page
│   ├── dashboard.html   # User dashboard
│   ├── change_pin.html  # Change PIN page
```

## Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/your-repo/atm-web-project.git
cd atm-web-project
```

### 2. Install Dependencies
Ensure you have Python installed (Python 3.8 or later recommended). Then install required packages:
```
pip install -r requirements.txt
```

### 3. Run the Application
```
python app.py
```
The application will start on `http://127.0.0.1:5000/`

### 4. Open in Browser
Go to `http://127.0.0.1:5000/` in your web browser to access the login page.

## Usage
- Enter your account number and PIN to log in.
- View your account balance and transaction history.
- Deposit or withdraw money using the provided forms.
- Change your PIN if needed.
- Click 'Logout' to exit the session.

## Technologies Used
- Python (Flask for backend)
- HTML, CSS (for frontend styling)
- JSON (for storing user data)

