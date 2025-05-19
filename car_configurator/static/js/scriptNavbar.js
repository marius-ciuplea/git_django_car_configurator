document.addEventListener("DOMContentLoaded", function () {

  // Contact page navbar
  const contactLink = document.querySelector(".open-contact-form.active");

  if (contactLink) {
    document.querySelector(".navbar")?.classList.add("on-contact-page");
    const navLinks = document.querySelectorAll(".nav-links a");
    navLinks.forEach(link => {
      link.classList.add("contact-page-link");
    });
  }

  const navbar = document.querySelector(".navbar");
  let lastScrollTop = 0;


  window.addEventListener("scroll", function () {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    // Add background class after certain scroll
    if (currentScroll > 100) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }

    // Hide/show navbar on scroll direction
    if (currentScroll > lastScrollTop && currentScroll > 100) {
      // Scrolling down
      navbar.style.top = "-150px"; // Adjust based on your navbar height
    } else {
      // Scrolling up
      navbar.style.top = "0";
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
  });


  

  // Toggle dropdown menu for user profile
const toggle = document.getElementById("userDropdownToggle");
const menu = document.getElementById("userDropdownMenu");

if (toggle) {
  toggle.addEventListener("click", function (e) {
    e.stopPropagation();
    menu.style.display = menu.style.display === "block" ? "none" : "block";
  });

  document.addEventListener("click", function () {
    menu.style.display = "none";
  });
}




  

  
});
