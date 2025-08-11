from flask import Blueprint

flashcards_bp = Blueprint('flashcards', __name__)

# filepath: c:\Users\daves\OneDrive\Desktop\VS Code\flashcard-app\flashcards\__init__.py
from . import routes