document.addEventListener("DOMContentLoaded", function () {
    const flashcards = document.querySelectorAll(".flashcard");

    flashcards.forEach(card => {
        card.innerHTML = `
            <div class="flashcard-front">${card.getAttribute("data-question")}</div>
            <div class="flashcard-back">${card.getAttribute("data-answer")}</div>
        `;

        card.addEventListener("click", function () {
            card.classList.toggle("flipped");
        });
    });
});
