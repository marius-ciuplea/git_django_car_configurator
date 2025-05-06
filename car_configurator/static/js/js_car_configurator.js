
  const track = document.querySelector('.carousel-track');
  const images = document.querySelectorAll('.carousel-image');
  const prevBtn = document.querySelector('.carousel-btn.prev');
  const nextBtn = document.querySelector('.carousel-btn.next');

  let currentIndex = 0;

  function updateCarousel() {
    const width = images[0].clientWidth
    track.style.transform = `translateX(-${currentIndex * width}px)`;
  }

  nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % images.length;
    updateCarousel();
  });

  prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateCarousel();
  });

  window.addEventListener('resize', updateCarousel);
