document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll('.nav-link');
  const currentPath = window.location.pathname;

  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});

// Function to fetch artist and venue IDs based on search input fro both mobile and desktop
document.addEventListener("DOMContentLoaded", function () {
  // Reusable function for Artist & Venue (PK based)
  function handlePKSearch(inputId, apiUrl, redirectPrefix, notFoundMsg) {
    const input = document.getElementById(inputId);
    if (input) {
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          let query = this.value.trim();
          if (query) {
            fetch(`${apiUrl}?name=${encodeURIComponent(query)}`)
              .then(response => response.json())
              .then(data => {
                if (data.id) {
                  window.location.href = `${redirectPrefix}${data.id}/`;
                } else {
                  alert(notFoundMsg);
                }
              });
          }
        }
      });
    }
  }

  // Artist (desktop + mobile)
  handlePKSearch("artist-search", "/products/api/artist-id/", "/products/artist/", "Artist not found");
  handlePKSearch("artist-search-mobile", "/products/api/artist-id/", "/products/artist/", "Artist not found");

  // Venue (desktop + mobile)
  handlePKSearch("venue-search", "/products/api/venue-id/", "/products/venue/", "Venue not found");
  handlePKSearch("venue-search-mobile", "/products/api/venue-id/", "/products/venue/", "Venue not found");

  // Merch (query-based, no PK lookup)
  function handleMerchSearch(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          let query = this.value.trim();
          if (query) {
            window.location.href = `/products/merch/?q=${encodeURIComponent(query)}`;
          }
        }
      });
    }
  }

  handleMerchSearch("merch-search");        // desktop
  handleMerchSearch("merch-search-mobile"); // mobile
});


// Function to update price based on quantity selection and to handle size dropdowns
document.addEventListener("DOMContentLoaded", function () {
  const totalPriceEl = document.getElementById("total-price");

  if (totalPriceEl) {
    const basePrice = parseFloat(totalPriceEl.dataset.price);

  // --- Quantity dropdown ---
  const qtyDropdown = document.getElementById("qtyDropdown");
  const qtyItems = document.querySelectorAll('[aria-labelledby="qtyDropdown"] .dropdown-item');
  const hiddenQtyInput = document.getElementById("selected-qty");

  qtyItems.forEach(item => {
    item.addEventListener("click", function (e) {
      e.preventDefault();

      const selectedQty = parseInt(this.dataset.value, 10);

      // Update button text
      qtyDropdown.textContent = `Quantity: ${selectedQty}`;

      // Update hidden input so form posts correct value
        hiddenQtyInput.value = selectedQty;

      // Update total price
      const total = (selectedQty * basePrice).toFixed(2);
      totalPriceEl.textContent = `Total Price: £${total}`;
    });
  });

  // --- Size dropdown ---
  const sizeDropdown = document.getElementById("sizeDropdown");
  const sizeItems = document.querySelectorAll('[aria-labelledby="sizeDropdown"] .dropdown-item');

  sizeItems.forEach(item => {
    item.addEventListener("click", function (e) {
      e.preventDefault();

      const value = this.dataset.value;

      // Update button text
      sizeDropdown.textContent = `Size: ${this.textContent}`;
    });
  });
  }
});
