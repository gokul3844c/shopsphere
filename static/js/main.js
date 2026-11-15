/**
 * ShopSphere E-Commerce - Main Vanilla JavaScript
 */

function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const isPass = input.type === "password";
  input.type = isPass ? "text" : "password";
  btn.textContent = isPass ? "Hide" : "Show";
}

document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss Django alert messages after 5 seconds
  const alerts = document.querySelectorAll(".alert-message");
  alerts.forEach(function (alert) {
    const closeBtn = alert.querySelector(".alert-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", function () {
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 250);
      });
    }
    setTimeout(function () {
      if (document.body.contains(alert)) {
        alert.style.transition = "opacity 0.5s ease";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 500);
      }
    }, 5000);
  });

  // Product detail thumbnail switcher
  const thumbBtns = document.querySelectorAll(".thumb-btn");
  const mainImage = document.getElementById("main-product-image");
  if (thumbBtns.length && mainImage) {
    thumbBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        thumbBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const fullSrc = btn.getAttribute("data-full-image");
        if (fullSrc) {
          mainImage.src = fullSrc;
        }
      });
    });
  }

  // Back to top button
  const backToTopBtn = document.getElementById("back-to-top");
  if (backToTopBtn) {
    backToTopBtn.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Prevent duplicate form submissions on button click
  document.querySelectorAll("form:not(.search-form)").forEach(function (form) {
    form.addEventListener("submit", function () {
      const submitBtn = form.querySelector('button[type="submit"]:not(.no-disable)');
      if (submitBtn && !submitBtn.disabled) {
        submitBtn.dataset.originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = "Processing...";
        // In case submission errors or stays on page, restore after 8s
        setTimeout(() => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = submitBtn.dataset.originalText;
        }, 8000);
      }
    });
  });
});
