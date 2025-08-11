# Flashcard Application

## Overview
This is a simple flashcard application built using Flask for the backend and HTML/CSS/JavaScript for the frontend. The application allows users to create, view, and manage flashcards for study purposes.

## Project Structure
```
flashcard-app
├── app.py
├── requirements.txt
├── README.md
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       └── main.js
├── templates
│   ├── index.html
│   └── flashcards.html
└── flashcards
    └── __init__.py
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flashcard-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```
   python app.py
   ```

2. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Features
- Create new flashcards
- View existing flashcards
- Interactive flashcard interface

## Contributing
Feel free to submit issues or pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.