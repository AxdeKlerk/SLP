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

// Grab elements
const statusEl = document.getElementById("status");
const payBtn = document.getElementById("pay-button");
const amountInput = document.getElementById("amount");

async function initSquare() {
  if (!window.Square) {
    statusEl.textContent = "Square SDK failed to load.";
    return;
  }

  const payments = window.Square.payments(appId, locationId);
  const card = await payments.card();
  await card.attach("#card-container");

  // Handle click
  payBtn.addEventListener("click", async () => {

    statusEl.textContent = "Tokenizing card...";
    payBtn.disabled = true;

    const result = await card.tokenize();

    if (result.status === "OK") {
      const token = result.token;
      const amount = amountInput.value || "10.00";

      const resp = await fetch("/payments/process-payment/", {
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
        statusEl.textContent = "Payment details received. Proceeding...";
      } else {
        statusEl.className = "status-msg error";
        statusEl.textContent = "Server rejected token. Please try again.";
      }

      // If tokenization failed
      const first = (result.errors && result.errors[0]) || {};
      statusEl.className = "status-msg error";
      statusEl.textContent = `Tokenization failed: ${first.message || "Unknown error"}`;
    } 

    payBtn.disabled = false;
  });
}

console.log("appId =", appId, "locationId =", locationId);

// Run
initSquare();
