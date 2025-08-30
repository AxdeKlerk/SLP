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
                window.location.href = `/artist/${data.id}/`;
              } else {
                alert("Artist not found");
              }
            });
        }
      }
    });
  }

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

