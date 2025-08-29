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
  const venueSearch = document.getElementById("venue-search");

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
                window.location.href = `/artist/${data.id}/`;
              } else {
                alert("Artist not found");
              }
            });
        }
      }
    });
  }

  if (venueSearch) {
    venueSearch.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        let query = this.value.trim();
        if (query) {
          fetch(`/products/venue-id/?name=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
              if (data.id) {
                window.location.href = `/venue/${data.id}/`;
              } else {
                alert("Venue not found");
              }
            });
        }
      }
    });
  }
});

console.log("script.js loaded");

document.addEventListener("DOMContentLoaded", function () {
  const artistSearch = document.getElementById("artist-search");

  if (artistSearch) {
    console.log("Artist input found");

    artistSearch.addEventListener("keydown", function (e) {
      console.log("Key pressed:", e.key);  // <— Add this
      if (e.key === "Enter") {
        e.preventDefault();
        const query = this.value.trim();
        console.log("Searching for:", query); // <— Add this

        if (query) {
          fetch(`/api/artist-id/?name=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
              console.log("Response:", data); // <— Add this
              if (data.id) {
                window.location.href = `/artist/${data.id}/`;
              } else {
                alert("Artist not found");
              }
            })
            .catch(err => {
              console.error("Fetch error:", err);
            });
        }
      }
    });
  }
});

document.addEventListener('DOMContentLoaded', () => {
    console.log("🎉 Bootstrap JS is loaded!");
  });
