document.addEventListener("DOMContentLoaded", function () {
  let selectedId = null;
  let selectedType = null; // 'message' or 'config'

  const modal = document.getElementById("confirmModal");
  const confirmBtn = document.getElementById("confirmDelete");
  const cancelBtn = document.getElementById("cancelDelete");

  function showModal(id, type) {
    selectedId = id;
    selectedType = type;
    modal.style.display = "flex";
  }

  // Message delete buttons
  document.querySelectorAll(".delete-btn").forEach(button => {
    button.addEventListener("click", function () {
      showModal(this.dataset.id, "message");
    });
  });

  // Config delete buttons
  document.querySelectorAll(".saved-delete-btn").forEach(button => {
    button.addEventListener("click", function () {
      showModal(this.dataset.id, "config");
    });
  });

  cancelBtn.addEventListener("click", function () {
    modal.style.display = "none";
    selectedId = null;
    selectedType = null;
  });

  confirmBtn.addEventListener("click", function () {
      if (!selectedId || !selectedType) return;

      const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
      let url, body;

      if (selectedType === "message") {
          url = deleteMessageUrl; // URL for deleting messages
          body = new URLSearchParams({
              message_id: selectedId,
          });
      } else if (selectedType === "config") {
          url = deleteConfigUrl; // URL for deleting configurations
          body = new URLSearchParams({
              config_id: selectedId, // Only send the config ID here
          });
      }

      fetch(url, {
          method: "POST",
          headers: {
              "X-CSRFToken": csrftoken,
              "Content-Type": "application/x-www-form-urlencoded",
          },
          body: body,
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              // Determine which element to remove from the DOM
              const elementId = selectedType === "message" ? "message-" : "config-";
              const el = document.getElementById(elementId + selectedId);
              
              if (el) {
                const card = el.closest(".saved-config-card")

                if (card) {
                  card.remove();

                } else { 
                  el.remove();
                }
            }// Remove the element without refreshing the page
          } else {
              alert("Error deleting item.");
          }
          modal.style.display = "none";
          selectedId = null;
          selectedType = null;
      })
      .catch(error => {
          console.error("Error:", error);
          alert("An unexpected error occurred.");
          modal.style.display = "none";
          selectedId = null;
          selectedType = null;
      });
    });

    document.querySelectorAll(".saved-send-btn").forEach(button => {
    button.addEventListener("click", function (e) {
      e.preventDefault();

      const configId = this.dataset.id;
      const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

      fetch(sendOfferUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          config_id: configId,
        }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert("Offer sent successfully!");
          window.location.reload(); // Optional
        } else {
          alert("Error: " + (data.error || "Could not send offer."));
        }
      })
      .catch(error => {
        console.error("Error sending offer:", error);
        alert("An unexpected error occurred.");
      });
    });
  });


});




















