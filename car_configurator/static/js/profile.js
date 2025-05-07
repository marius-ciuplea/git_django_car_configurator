document.addEventListener("DOMContentLoaded", function () {
  let selectedMessageId = null;

  // Handle the confirmation modal for deleting messages (on the delete page)
  const modal = document.getElementById("confirmModal");
  const confirmBtn = document.getElementById("confirmDelete");
  const cancelBtn = document.getElementById("cancelDelete");

  // Handle delete confirmation modal (only on pages where delete action is possible)
  if (modal) {
    document.querySelectorAll(".delete-btn").forEach((button) => {
      button.addEventListener("click", function () {
        selectedMessageId = this.dataset.id;
        modal.style.display = "flex"; // Show the confirmation modal
      });
    });

    cancelBtn.addEventListener("click", function () {
      modal.style.display = "none"; // Hide the confirmation modal
      selectedMessageId = null;
    });

    confirmBtn.addEventListener("click", function () {
      if (!selectedMessageId) return;

      const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

      fetch(deleteUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          message_id: selectedMessageId,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const msgEl = document.getElementById("message-" + selectedMessageId);
            if (msgEl) msgEl.remove(); // Remove the message if successfully deleted
          } else {
            alert("Error deleting message.");
          }
          modal.style.display = "none"; // Hide the modal after action
          selectedMessageId = null;
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An unexpected error occurred.");
          modal.style.display = "none";
          selectedMessageId = null;
        });
    });
  }

  
 
  // Reusable cancel button functionality for modals
  // if (modalCancel) {
  //   modalCancel.addEventListener("click", function () {
  //     closeModal(); // Close the modal if cancel button is clicked
  //   });
  // }
});





















