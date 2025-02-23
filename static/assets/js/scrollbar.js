const mainFeed = document.querySelector('.main-feed');

// Show scrollbar when scrolling
mainFeed.addEventListener('scroll', () => {
  mainFeed.style.overflowY = 'scroll'; // Make scrollbar visible on scroll
});

// Optionally, hide the scrollbar after a delay when scrolling stops
let timeout;
mainFeed.addEventListener('mouseenter', () => {
  timeout = setTimeout(() => {
    mainFeed.style.overflowY = 'hidden'; // Hide scrollbar when not scrolling
  }, 1000);  // Wait 1 second after scrolling stops
});

mainFeed.addEventListener('mouseleave', () => {
  clearTimeout(timeout);  // Clear the timeout if the user leaves the area
});
