      const track = document.querySelector(".carousel-track");
      let images = document.querySelectorAll(".carousel-image");
      const prevBtn = document.querySelector(".carousel-btn.prev");
      const nextBtn = document.querySelector(".carousel-btn.next");
      let currentIndex = 0;

      function updateCarousel() {
        images = document.querySelectorAll(".carousel-image"); // update reference
        if (images.length === 0) return;
        const width = images[0].clientWidth;
        track.style.transform = `translateX(-${currentIndex * width}px)`;
      }

      // ✅ Color circle click logic
      document.querySelectorAll(".color-circle").forEach((circle) => {
        circle.addEventListener("click", function () {
          const imagesData = this.dataset.images;
          const colorId = this.dataset.colorId;

            // Remove 'selected' class from all color circles
          document.querySelectorAll(".color-circle").forEach((c) =>
            c.classList.remove("selected")
          );

          // Add 'selected' class to the clicked circle
          this.classList.add("selected");

          try {
            const imageUrls = JSON.parse(imagesData.replace(/'/g, '"'));

            const carouselTrack = document.querySelector(".carousel-track");
            const newImages = imageUrls
              .map(
                (url, index) =>
                  `<img src="${url}" class="carousel-image" alt="Color image ${
                    index + 1
                  }">`
              )
              .join("");

            carouselTrack.innerHTML = newImages;
            // Reset index and update references
            currentIndex = 0;
            images = document.querySelectorAll(".carousel-image");
            updateCarousel();
          } catch (e) {
            console.error("Failed to load images for selected color:", e);
          }

          const selectedOption = document.querySelector(
            `#color option[value="${colorId}"]`
          );
          const colorName = selectedOption.textContent.trim();
          const colorPrice = selectedOption.dataset.price;

          // Hide all other color info divs
          document.querySelectorAll(".color-info").forEach((infoDiv) => {
            infoDiv.style.display = "none";
          });

          // Update the color select dropdown to match the clicked color
          const colorSelect = document.getElementById("color");
          colorSelect.value = colorId;
          updateTotalPrice(); // Update the total price based on new color selection
        });

      });

      nextBtn.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateCarousel();
      });

      prevBtn.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateCarousel();
      });

      window.addEventListener("resize", updateCarousel);

      function getSelectedOptionPrice(selectId) {
        const select = document.getElementById(selectId);
        if (!select || select.selectedIndex === -1) return 0;
        const selectedOption = select.options[select.selectedIndex];
        return parseFloat(selectedOption.dataset.price || 0);
      }

      function updateTotalPrice() {
        const basePrice = parseFloat(
          document.getElementById("basePrice").innerText
        );
        const engineSelect = document.getElementById("engine");
        const colorSelect = document.getElementById("color");
        const wheelSelect = document.getElementById("wheel");

        const enginePrice = getSelectedOptionPrice("engine");
        const colorPrice = getSelectedOptionPrice("color");
        const wheelPrice = getSelectedOptionPrice("wheel");

        const total = basePrice + enginePrice + colorPrice + wheelPrice;

        // Update the total price in both summary and form
        document.getElementById("totalPrice").innerText = total.toFixed(2);
        document.getElementById("totalPriceDisplay").innerText = total.toFixed(2);

        // Update display texts for selected options
        document.getElementById("selectedEngine").innerText =
          engineSelect.options[engineSelect.selectedIndex].text;
        document.getElementById("selectedColor").innerText =
          colorSelect.options[colorSelect.selectedIndex].text;
        document.getElementById("selectedWheel").innerText =
          wheelSelect.options[wheelSelect.selectedIndex].text;

        // Update individual prices
        document.getElementById("enginePrice").innerText = enginePrice.toFixed(2);
        document.getElementById("colorPrice").innerText = colorPrice.toFixed(2);
        document.getElementById("wheelPrice").innerText = wheelPrice.toFixed(2);
      }

      document.querySelectorAll(".wheel-name").forEach((wheel) => {
        wheel.addEventListener("click", function () {
          const wheelId = this.dataset.wheelId;
          const wheelPrice = parseFloat(this.dataset.price);

          // Set the selected wheel in the dropdown
          document.getElementById("wheel").value = wheelId;

          // Manually trigger the total price update
          updateTotalPrice();
        });
      });

      document.querySelectorAll(".engine-name").forEach((engine) => {
        engine.addEventListener("click", function () {
          const engineId = this.dataset.engineId;
          const enginePrice = parseFloat(this.dataset.price);

          // Set the selected engine in the dropdown
          document.getElementById("engine").value = engineId;

          // Manually trigger the total price update
          updateTotalPrice();
        });
      });

      // Update price when engine, color, or wheel changes
      document
        .getElementById("engine")
        .addEventListener("change", updateTotalPrice);
      document
        .getElementById("color")
        .addEventListener("change", updateTotalPrice);
      document
        .getElementById("wheel")
        .addEventListener("change", updateTotalPrice);

      // ✅ On page load: initialize total price and simulate click on default color
      window.addEventListener("load", () => {
        updateTotalPrice();
        updateCarousel();

        const defaultColorOption = document.querySelector(
          "#color option[selected]"
        );
        if (defaultColorOption) {
          const defaultColorId = defaultColorOption.value;
          const colorCircle = document.querySelector(
            `.color-circle[data-color-id="${defaultColorId}"]`
          );
          if (colorCircle) {
            setTimeout(() => colorCircle.click(), 50); // delay ensures images render first
          }
        }
      });

      function selectOption(button) {
  // Find the closest container (e.g., wheels-container or engines-container)
        const container = button.closest(".wheels-container, .engines-container");

        // Remove 'selected' class only within that container
        const buttonsInGroup = container.querySelectorAll(".option-btn");
        buttonsInGroup.forEach((btn) => btn.classList.remove("selected"));

        // Add 'selected' class to the clicked button
        button.classList.add("selected");
      }

      document.addEventListener("DOMContentLoaded", function () {
    // Highlight default wheel
        const selectedWheelOption = document.querySelector('#wheel option[selected]');
        if (selectedWheelOption) {
          const wheelId = selectedWheelOption.value;
          const wheelDiv = document.querySelector(`[data-wheel-id="${wheelId}"]`);
          if (wheelDiv) {
            wheelDiv.parentElement.classList.add("selected");
          }
        }

        // Highlight default engine
        const selectedEngineOption = document.querySelector('#engine option[selected]');
        if (selectedEngineOption) {
          const engineId = selectedEngineOption.value;
          const engineDiv = document.querySelector(`[data-engine-id="${engineId}"]`);
          if (engineDiv) {
            engineDiv.parentElement.classList.add("selected");
          }
        }

        // Highlight default color
        const selectedColorOption = document.querySelector('#color option[selected]');
        if (selectedColorOption) {
          const colorId = selectedColorOption.value;
          const colorDiv = document.querySelector(`[data-color-id="${colorId}"]`);
          if (colorDiv) {
            colorDiv.classList.add("selected");
            colorDiv.click(); // Simulate click to load carousel images
          }
        }
      });