/**
 * ShopSphere E-Commerce - Live Search Suggestions
 */

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("header-search-input");
  const suggestionsBox = document.getElementById("search-suggestions");
  const categorySelect = document.getElementById("header-category-select");

  if (!searchInput || !suggestionsBox) return;

  let debounceTimer = null;

  searchInput.addEventListener("input", function () {
    clearTimeout(debounceTimer);
    const query = searchInput.value.trim();

    if (query.length < 2) {
      suggestionsBox.style.display = "none";
      suggestionsBox.innerHTML = "";
      return;
    }

    debounceTimer = setTimeout(function () {
      fetch(`/shop/api/search-suggestions/?q=${encodeURIComponent(query)}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.results && data.results.length > 0) {
            let html = "";
            data.results.forEach((item) => {
              html += `
                <a href="${item.url}" class="suggestion-item">
                  <img src="${item.image}" alt="${item.name}" class="suggestion-thumb">
                  <div class="suggestion-details">
                    <div class="suggestion-title">${escapeHtml(item.name)}</div>
                    <div class="suggestion-meta">in ${escapeHtml(item.category)} · by ${escapeHtml(item.brand)}</div>
                  </div>
                  <div class="suggestion-price">${item.price}</div>
                </a>
              `;
            });
            suggestionsBox.innerHTML = html;
            suggestionsBox.style.display = "block";
          } else {
            suggestionsBox.style.display = "none";
          }
        })
        .catch(() => {
          suggestionsBox.style.display = "none";
        });
    }, 250);
  });

  // Close suggestions when clicking outside
  document.addEventListener("click", function (e) {
    if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
      suggestionsBox.style.display = "none";
    }
  });

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
  }
});
