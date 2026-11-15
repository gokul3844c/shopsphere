/**
 * ShopSphere E-Commerce - Cart & AJAX Dynamic Updates
 */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
  const csrftoken = getCookie("csrftoken");

  // Quantity change in cart page via select or buttons
  document.querySelectorAll(".cart-qty-select").forEach(function (select) {
    select.addEventListener("change", function () {
      const productId = this.getAttribute("data-product-id");
      const newQty = this.value;
      updateCartQuantity(productId, newQty);
    });
  });

  // Quantity stepper buttons
  document.querySelectorAll(".qty-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const productId = this.getAttribute("data-product-id");
      const action = this.getAttribute("data-action");
      const qtySpan = document.getElementById(`qty-${productId}`);
      if (!qtySpan) return;

      let currentQty = parseInt(qtySpan.innerText, 10) || 1;
      let targetQty = action === "inc" ? currentQty + 1 : currentQty - 1;

      if (targetQty < 1) targetQty = 0;
      updateCartQuantity(productId, targetQty);
    });
  });

  function updateCartQuantity(productId, quantity) {
    const formData = new FormData();
    formData.append("quantity", quantity);

    fetch(`/cart/update/${productId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          // Update cart badge in header
          const badge = document.getElementById("header-cart-count");
          if (badge) badge.textContent = data.cart_count;

          // If quantity became 0, remove row
          if (data.item_quantity === 0) {
            const row = document.getElementById(`cart-row-${productId}`);
            if (row) row.remove();
          } else {
            const lineTotalEl = document.getElementById(`line-total-${productId}`);
            if (lineTotalEl) lineTotalEl.textContent = `₹${parseFloat(data.line_total).toLocaleString("en-IN", {minimumFractionDigits: 2})}`;

            const qtySpan = document.getElementById(`qty-${productId}`);
            if (qtySpan) qtySpan.textContent = data.item_quantity;
          }

          // Update Subtotal & Grand Total
          const subtotalEls = document.querySelectorAll(".cart-subtotal-val");
          subtotalEls.forEach((el) => {
            el.textContent = `₹${parseFloat(data.subtotal).toLocaleString("en-IN", {minimumFractionDigits: 2})}`;
          });

          const grandTotalEl = document.getElementById("cart-grand-total");
          if (grandTotalEl) {
            grandTotalEl.textContent = `₹${parseFloat(data.grand_total).toLocaleString("en-IN", {minimumFractionDigits: 2})}`;
          }

          // Reload if cart became completely empty
          if (data.cart_count === 0) {
            window.location.reload();
          }
        }
      })
      .catch((err) => {
        console.error("Cart update error:", err);
      });
  }
});
