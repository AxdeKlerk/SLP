console.log("Square checkout JS loaded successfully!");

document.addEventListener("DOMContentLoaded", async () => {
  // Get config values from template dataset
  setTimeout(() => {
    console.log(" Timeout reached");

  const configEl = document.getElementById("square-config");
  if (!configEl) {
    console.error("Square config element not found.");
    return;
  }

  const appId = configEl.dataset.appId;
  const locationId = configEl.dataset.locationId;

  console.log("App ID:", appId, "Loc ID:", locationId); // test log

  if (!appId || !locationId) {
    console.error("Square app or location ID missing from dataset.");
    return;
  }

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
          window.location.href = `/payments/${data.order_id || "confirmation"}/success/`;
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

  // Now initialize
  initSquare(appId, locationId);
  }, 300);
});
