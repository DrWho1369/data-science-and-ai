document.addEventListener("DOMContentLoaded", function () {
    const flashcards = document.querySelectorAll(".flashcard");

    flashcards.forEach(card => {
        const question = card.getAttribute("data-question");
        const answer = card.getAttribute("data-answer");

        card.innerHTML = `
            <div class="flashcard-inner">
                <div class="flashcard-front">${question}</div>
                <div class="flashcard-back">${answer}</div>
            </div>
        `;

        card.addEventListener("click", function () {
            card.classList.toggle("flipped");
        });
    });
});
