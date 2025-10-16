document.addEventListener("DOMContentLoaded", function () {
  // ========================================================
  // Highlight active nav link
  // ========================================================
  const navLinks = document.querySelectorAll(".nav-link");
  const currentPath = window.location.pathname;

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });


  // ========================================================
  // Search helpers (artist, venue, merch)
  // ========================================================
  function handlePKSearch(inputId, apiUrl, redirectPrefix, notFoundMsg) {
    const input = document.getElementById(inputId);
    if (input) {
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          let query = this.value.trim();
          if (query) {
            fetch(`${apiUrl}?name=${encodeURIComponent(query)}`)
              .then((response) => response.json())
              .then((data) => {
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


  // ========================================================
  // Merch detail page (live price + size selection)
  // ========================================================
  const totalPriceEl = document.getElementById("total-price");

  if (totalPriceEl) {
    const basePrice = parseFloat(totalPriceEl.dataset.price);

    // Quantity dropdown (merch detail)
    const qtyDropdown = document.getElementById("qtyDropdown");
    const qtyItems = document.querySelectorAll(
      '[aria-labelledby="qtyDropdown"] .dropdown-item'
    );
    const hiddenQtyInput = document.getElementById("selected-qty");

    qtyItems.forEach((item) => {
      item.addEventListener("click", function (e) {
        e.preventDefault();

        const selectedQty = parseInt(this.dataset.value, 10);
        qtyDropdown.textContent = `Quantity: ${selectedQty}`;
        hiddenQtyInput.value = selectedQty;

        const total = (selectedQty * basePrice).toFixed(2);
        totalPriceEl.textContent = `Total Price: £${total}`;
      });
    });

    // Size dropdown (merch detail)
    const sizeDropdown = document.getElementById("sizeDropdown");
    const sizeItems = document.querySelectorAll('[aria-labelledby="sizeDropdown"] .dropdown-item');
    const hiddenSizeInput = document.getElementById("selected-size");

    sizeItems.forEach((item) => {
      item.addEventListener("click", function (e) {
        e.preventDefault();

        // Show size on the button
        sizeDropdown.textContent = `Size: ${this.textContent}`;

        // Store the size value in the hidden input
        hiddenSizeInput.value = this.textContent;
      });
    });
  }


  // ========================================================
  // Basket page (quantity update auto-submit)
  // ========================================================
  const basketQtyOptions = document.querySelectorAll(".basket-qty-option");

  basketQtyOptions.forEach((option) => {
    option.addEventListener("click", function (e) {
      e.preventDefault();

      const selectedQty = this.dataset.value;
      const itemId = this.dataset.itemId;

      const btn = document.getElementById(`basketQtyDropdown-${itemId}`);
      const hiddenInput = document.getElementById(
        `basket-selected-qty-${itemId}`
      );

      btn.textContent = `Qty: ${selectedQty}`;
      hiddenInput.value = selectedQty;

      // Delay form submission slightly to ensure value updates
      setTimeout(() => {
        this.closest("form").submit();
      }, 0);

      const dropdown = bootstrap.Dropdown.getInstance(btn);
      if (dropdown) dropdown.hide();
    });
  });

  
  // ========================================================
  // Mobile search input stretch
  // ========================================================
  const searchToggle = document.querySelector('[data-bs-toggle="collapse"][href="#offcanvasSearch"]');
  const offcanvas = document.querySelector(".offcanvas.offcanvas-end");
  const searchSection = document.getElementById("offcanvasSearch");

  if (searchToggle && offcanvas && searchSection) {
    // Expand when search section opens
    searchSection.addEventListener("shown.bs.collapse", () => {
      offcanvas.classList.add("search-expanded");
    });

    // Collapse back when search section closes
    searchSection.addEventListener("hidden.bs.collapse", () => {
      offcanvas.classList.remove("search-expanded");
    });
  }
});
