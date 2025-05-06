document.addEventListener("DOMContentLoaded", function () {
  const contactLinks = document.querySelectorAll('.open-contact-form');
  const contactFormContainer = document.querySelector('.contact-form-container');
  const pageContent = document.getElementById('page-content');
  const overlay = document.getElementById('overlay');
  const form = document.querySelector('form');
  const successPopup = document.getElementById('success-popup');
  const homeButton = document.getElementById('go-home-button');

  if (contactLinks && contactFormContainer) {
    contactLinks.forEach(contactLink => {
      contactLink.addEventListener('click', (e) => {
        e.preventDefault();
        contactFormContainer.classList.remove('hidden');
      });
    });
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      const csrfToken = formData.get('csrfmiddlewaretoken');

      const submitButton = form.querySelector('.submit-btn');
      const originalButtonText = submitButton.textContent;
      submitButton.textContent = 'Sending...';
      submitButton.disabled = true;

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken,
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Show success popup with custom message
          if (successPopup) {
            successPopup.querySelector('p').innerText =
              'Thank you! Your message has been sent. Our team will get back to you shortly.';
            successPopup.classList.remove('hidden');
            successPopup.classList.add('show');
          }

          if (homeButton) {
            homeButton.classList.remove('hidden');
          }

          // Clear form and hide it
          form.reset();
          form.classList.add('hidden');

          // Apply blur and disable background interaction
          if (pageContent) {
            pageContent.classList.add('blur');
          }
          if (overlay) {
            overlay.classList.remove('hidden');
          }
        } else {
          let errorMessages = '';
          for (const field in data.errors) {
            errorMessages += `${field}: ${data.errors[field].join(', ')}\n`;
          }
          alert('Errors:\n' + errorMessages);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An unexpected error occurred. Please try again.');
      })
      .finally(() => {
        submitButton.textContent = originalButtonText;
        submitButton.disabled = false;
      });
    });
  }
});
