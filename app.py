from flask import Flask
from flashcards import flashcards_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions

app.register_blueprint(flashcards_bp)

if __name__ == '__main__':
    app.run(debug=True)