
let images = document.querySelectorAll('.carousel-image');
let currentIndex = 0;
setInterval(() => {
    images[currentIndex].style.opacity = 0;
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].style.opacity = 1;
}, 3000);