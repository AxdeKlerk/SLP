document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll('.nav-link');
  const currentPath = window.location.pathname;

  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});

// Function to fetch artist ID based on search input
document.addEventListener("DOMContentLoaded", function () {
  const artistSearch = document.getElementById("artist-search");

  if (artistSearch) {
    artistSearch.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        let query = this.value.trim();
        if (query) {
          fetch(`/products/api/artist-id/?name=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
              if (data.id) {
                window.location.href = `/products/artist/${data.id}/`;
              } else {
                alert("Artist not found");
              }
            });
        }
      }
    });
  }
});

  // Function to fetch venue ID based on search input
document.addEventListener("DOMContentLoaded", function () {
  const venueSearch = document.getElementById("venue-search");
  if (venueSearch) {
    venueSearch.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        let query = this.value.trim();
        if (query) {
          fetch(`/products/api/venue-id/?name=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
              if (data.id) {
                window.location.href = `/products/venue/${data.id}/`;
              } else {
                alert("Venue not found");
              }
            });
        }
      }
    });
  }
});

// Function to update price based on quantity selection
document.addEventListener("DOMContentLoaded", function () {
  const totalPriceEl = document.getElementById("total-price");
  const basePrice = parseFloat(totalPriceEl.dataset.price);  // get from data-price
  const qtySelect = document.getElementById("quantity-select");

  function updatePrice() {
    const qty = parseInt(qtySelect.value, 10) || 1;
    const total = (qty * basePrice).toFixed(2);
    totalPriceEl.textContent = `Total Price: £${total}`;
  }

  qtySelect.addEventListener("change", updatePrice);
  updatePrice(); // run on load
});

