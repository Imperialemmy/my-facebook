window.addEventListener('load', () => {
    setTimeout(() => {
        document.getElementById('preloader').classList.add('hidden');
        document.getElementById('content').style.display = 'block';
    }, 2000);
});
