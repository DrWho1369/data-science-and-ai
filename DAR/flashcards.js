document.addEventListener("DOMContentLoaded", function () {
    const flashcards = document.querySelectorAll(".flashcard");
    
    flashcards.forEach(card => {
        card.textContent = card.getAttribute("data-question");
        let isQuestion = true;
        
        card.addEventListener("click", function () {
            if (isQuestion) {
                card.textContent = card.getAttribute("data-answer");
            } else {
                card.textContent = card.getAttribute("data-question");
            }
            isQuestion = !isQuestion;
        });
    });
});
