// function toggleMoreItems() {
//   const moreItems = document.getElementById('more-items');
//   if (moreItems.style.display === 'none') {
//     moreItems.style.display = 'block';
//   } else {
//     moreItems.style.display = 'none';
//     }
//   }

  console.log('sidebar.js loaded');




  document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.toggle-button');
    const moreItems = document.getElementById('more-items');

    toggleButton.addEventListener('click', function() {
      if (moreItems.style.display === 'none') {
        moreItems.style.display = 'block';
        toggleButton.textContent = 'Show Less';
      } else {
        moreItems.style.display = 'none';
        toggleButton.textContent = 'Show More';
      }
    });
  });