document.addEventListener('DOMContentLoaded', function() {
    const flashcardContainer = document.getElementById('flashcard-container');
    const nextButton = document.getElementById('next-button');
    const prevButton = document.getElementById('prev-button');
    let currentFlashcardIndex = 0;
    let flashcards = [];

    function fetchFlashcards() {
        fetch('/api/flashcards')
            .then(response => response.json())
            .then(data => {
                flashcards = data;
                displayFlashcard(currentFlashcardIndex);
            })
            .catch(error => console.error('Error fetching flashcards:', error));
    }

    function displayFlashcard(index) {
        if (flashcards.length === 0) return;
        const flashcard = flashcards[index];
        flashcardContainer.innerHTML = `
            <div class="flashcard">
                <div class="question">${flashcard.question}</div>
                <div class="answer">${flashcard.answer}</div>
            </div>
        `;
    }

    nextButton.addEventListener('click', function() {
        if (currentFlashcardIndex < flashcards.length - 1) {
            currentFlashcardIndex++;
            displayFlashcard(currentFlashcardIndex);
        }
    });

    prevButton.addEventListener('click', function() {
        if (currentFlashcardIndex > 0) {
            currentFlashcardIndex--;
            displayFlashcard(currentFlashcardIndex);
        }
    });

    fetchFlashcards();
});