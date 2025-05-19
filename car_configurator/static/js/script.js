document.addEventListener("DOMContentLoaded", function () {
  const wrapper = document.querySelector(".carousel-wrapper");
  const slides = document.querySelectorAll(".carousel-slide");
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");

  if (wrapper && slides.length > 0 && prevButton && nextButton) {
    const intervalTime = 4000;
    let currentIndex = 0;
    let autoScroll;
    const totalSlides = slides.length;

    // Clone first and last slides
    const firstClone = slides[0].cloneNode(true);
    const lastClone = slides[slides.length - 1].cloneNode(true);

    firstClone.classList.add("first-clone");
    lastClone.classList.add("last-clone");

    wrapper.appendChild(firstClone);
    wrapper.insertBefore(lastClone, slides[0]);

    const allSlides = document.querySelectorAll(".carousel-slide");
    const totalSlidesWithClones = allSlides.length;

    // Set wrapper width
    wrapper.style.width = `${totalSlidesWithClones * 100}%`;

    // Set each slide width
    allSlides.forEach((slide) => {
      slide.style.width = `${100 / totalSlidesWithClones}%`;
    });

    // Start from first real slide (not last-clone)
    wrapper.style.transition = "none";
    wrapper.style.transform = `translateX(-${100 / totalSlidesWithClones}%)`;

    currentIndex = 1; // because of lastClone in front

    function updateSlide() {
      wrapper.style.transition = "transform 0.7s ease-in-out";
      wrapper.style.transform = `translateX(-${
        (currentIndex * 100) / totalSlidesWithClones
      }%)`;
    }

    function nextSlide() {
      if (currentIndex >= totalSlidesWithClones - 1) return;
      currentIndex++;
      updateSlide();
    }

    function prevSlide() {
      if (currentIndex <= 0) return;
      currentIndex--;
      updateSlide();
    }

    // Handle looping nicely
    wrapper.addEventListener("transitionend", () => {
      if (allSlides[currentIndex].classList.contains("first-clone")) {
        wrapper.style.transition = "none";
        currentIndex = 1;
        wrapper.style.transform = `translateX(-${
          (currentIndex * 100) / totalSlidesWithClones
        }%)`;
      }
      if (allSlides[currentIndex].classList.contains("last-clone")) {
        wrapper.style.transition = "none";
        currentIndex = totalSlides;
        wrapper.style.transform = `translateX(-${
          (currentIndex * 100) / totalSlidesWithClones
        }%)`;
      }
    });

    function startAutoScroll() {
      autoScroll = setInterval(() => {
        nextSlide();
      }, intervalTime);
    }

    function resetAutoScroll() {
      clearInterval(autoScroll);
      startAutoScroll();
    }

    nextButton.addEventListener("click", () => {
      nextSlide();
      resetAutoScroll();
    });

    prevButton.addEventListener("click", () => {
      prevSlide();
      resetAutoScroll();
    });

    startAutoScroll();
  }

  const popupMessages = document.querySelectorAll(".popup-message");
  popupMessages.forEach((popup, index) => {
    setTimeout(() => {
      popup.style.display = "block";
      setTimeout(() => {
        popup.style.display = "none";
      }, 3000);
    }, index * 500); // stagger multiple popups
  });
});
