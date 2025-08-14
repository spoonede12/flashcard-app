import os
import json
from flask import render_template, request, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename
from . import flashcards_bp

USERNAME = "dave"
PASSWORD = "india"

# Data file path
DATA_FILE = 'flashcard_data.json'

# Data storage functions
def load_data():
    """Load data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                return data.get('flashcards', []), data.get('decks', [])
        else:
            return [], []
    except (json.JSONDecodeError, FileNotFoundError):
        print("Warning: Could not load data file, starting with empty data")
        return [], []

def save_data():
    """Save data to JSON file"""
    try:
        data = {
            'flashcards': flashcards,
            'decks': decks
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

# Load data on startup
flashcards, decks = load_data()

# Login routes

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("flashcards.login"))
        return f(*args, **kwargs)
    return decorated_function

@flashcards_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('flashcards.index'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

@flashcards_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('flashcards.login'))

# Flashcard routes

@flashcards_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@flashcards_bp.route('/flashcards')
@login_required
def show_flashcards():
    return render_template('flashcards.html', flashcards=flashcards)

@flashcards_bp.route('/flashcards/create', methods=['GET', 'POST'])
@login_required
def create_flashcard():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        deck_index = int(request.form['deck'])
        decks[deck_index]['flashcards'].append({'question': question, 'answer': answer})
        save_data()  # Save data after adding flashcard
        return redirect(url_for('flashcards.show_flashcards'))
    return render_template('create_flashcard.html', decks=decks)

# Bulk Upload

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@flashcards_bp.route('/flashcards/bulk_upload', methods=['GET', 'POST'])
@login_required
def bulk_upload_flashcards():
    if request.method == 'POST':
        deck_index = int(request.form['deck'])
        files = request.files.getlist('images')
        upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        elif not os.path.isdir(upload_path):
            raise RuntimeError(f"{upload_path} exists and is not a directory.")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_path, filename))
                image_url = url_for('static', filename=f'uploads/{filename}')
                # Associate with selected deck
                decks[deck_index]['flashcards'].append({
                    'question': filename,
                    'answer': image_url
                })
        save_data()  # Save data after bulk upload
        return redirect(url_for('flashcards.show_flashcards'))
    return render_template('bulk_upload.html', decks=decks)

# Deck routes

@flashcards_bp.route('/decks')
@login_required
def show_decks():
    return render_template('decks.html', decks=decks)

@flashcards_bp.route('/decks/create', methods=['GET', 'POST'])
@login_required
def create_deck():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        decks.append({'name': name, 'description': description, 'flashcards': []})
        save_data()  # Save data after creating deck
        return redirect(url_for('flashcards.show_decks'))
    return render_template('create_deck.html')

@flashcards_bp.route('/flashcards/play', methods=['GET', 'POST'])
@login_required
def play_flashcards():
    if request.method == 'POST':
        deck_index = int(request.form['deck'])
        selected_deck = decks[deck_index]
        return render_template('play_flashcards.html', flashcards=selected_deck['flashcards'], deck_name=selected_deck['name'])
    return render_template('select_deck.html', decks=decks)

