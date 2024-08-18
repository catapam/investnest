window.onload = function() {
    var adjustHeightsAndAttachFlip = function() {
        var maxHeight = 0;
        var minHeight = 220;  // Set the minimum height
        var flipCardFronts = document.querySelectorAll('.flip-card-front');
        var flipCardBacks = document.querySelectorAll('.flip-card-back');
        var flipCardInners = document.querySelectorAll('.flip-card-inner');

        // Find the maximum height of all flip-card-front elements
        flipCardFronts.forEach(function(card) {
            var cardHeight = card.offsetHeight;
            if (cardHeight > maxHeight) {
                maxHeight = cardHeight;
            }
        });

        // Ensure the height is at least the minimum height
        maxHeight = Math.max(maxHeight, minHeight);

        // Set the height of all flip-card-front and flip-card-back elements to the maximum or minimum height
        flipCardFronts.forEach(function(card) {
            card.style.height = maxHeight + 'px';
        });

        flipCardBacks.forEach(function(card) {
            card.style.height = maxHeight + 'px';
        });

        // Set the height of all flip-card-inner elements to match the tallest card
        flipCardInners.forEach(function(card) {
            card.style.height = maxHeight + 'px';
        });

        // Set the max-height for card-text inside flip-card-back
        var cardTexts = document.querySelectorAll('.flip-card-back .card-body .card-text');
        cardTexts.forEach(function(text) {
            text.style.maxHeight = (maxHeight - text.closest('.card-body').offsetTop) * 0.6 + 'px';
        });

        // Attach flip event listeners
        document.querySelectorAll('.card-flip').forEach(card => {
            card.addEventListener('click', function() {
                card.querySelector('.flip-card-inner').classList.toggle('flipped');
            });
        });
    };

    // Run the function after the window is fully loaded
    adjustHeightsAndAttachFlip();
};
