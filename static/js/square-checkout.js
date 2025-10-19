// Get config values from template dataset
const configEl = document.getElementById("square-config");
const appId = configEl.dataset.appId;
const locationId = configEl.dataset.locationId;

// CSRF helper
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}
const csrftoken = getCookie("csrftoken");

// DOM elements
const statusEl = document.getElementById("status");
const payBtn = document.getElementById("pay-button");
const amountInput = document.getElementById("amount");

// Initialize Square payment form
async function initSquare(appId, locationId) {
  if (!window.Square) {
    statusEl.textContent = "Square SDK failed to load.";
    return;
  }

  // Create payments instance and card element
  const payments = window.Square.payments(appId, locationId);
  const card = await payments.card();
  await card.attach("#card-container");

  // On button click
  payBtn.addEventListener("click", async () => {
    console.log("Pay button clicked");
    statusEl.textContent = "Tokenizing card...";
    payBtn.disabled = true;

    const result = await card.tokenize();

    if (result.status === "OK") {
      const token = result.token;
      const amount = amountInput.value || "10.00";

      // Extract the order ID safely from the current page URL
      const orderId = window.location.pathname.match(/\/(\d+)\//)?.[1];
      if (!orderId) {
        console.error("Order ID not found in URL!");
        statusEl.textContent = "Error: order not found.";
        payBtn.disabled = false;
        return;
      }

      // Use the extracted orderId to hit the correct endpoint
      const resp = await fetch(`/payments/${orderId}/process-payment/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ token, amount }),
      });

      const data = await resp.json();
      if (resp.ok && data.ok) {
        statusEl.className = "status-msg success";
        statusEl.textContent = "Payment successful! Redirecting...";
        setTimeout(() => {
          window.location.href = `/payments/${data.order_id || "confirmation"}/success/`;
        }, 1500);
      } else {
        statusEl.className = "status-msg error";
        statusEl.textContent = "Server rejected token. Check server logs.";
      }
    } else {
      if (result.errors && result.errors.length > 0) {
        statusEl.className = "status-msg error";
        statusEl.textContent = `Tokenization failed: ${result.errors
          .map((e) => e.message)
          .join(", ")}`;
      } else {
        statusEl.className = "status-msg error";
        statusEl.textContent =
          "Tokenization failed: No detailed error returned.";
      }
    }
    payBtn.disabled = false;
  });
}

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", function () {
  // Get config values after DOM is loaded
  const configEl = document.getElementById("square-config");
  const appId = configEl?.dataset.appId;
  const locationId = configEl?.dataset.locationId;

  if (!appId || !locationId) {
    console.error("Square app or location ID missing from dataset.");
    return;
  }

  // Initialize Square after DOM and data are ready
  initSquare(appId, locationId);

  // Billing / Shipping address toggles
  const useBilling = document.getElementById("useBillingForshipping");
  const updateShipping = document.getElementById("updateshipping");
  const shippingSection = document.getElementById("shippingAddressSection");

  if (useBilling && updateShipping && shippingSection) {
    function toggleShippingSection() {
      shippingSection.style.display = updateShipping.checked ? "block" : "none";
    }
    useBilling.addEventListener("change", toggleShippingSection);
    updateShipping.addEventListener("change", toggleShippingSection);
    toggleShippingSection();
  }
});



