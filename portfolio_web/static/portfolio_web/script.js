document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".mobile-menu-toggle");
  const nav = document.getElementById("primary-nav");

  if (btn && nav) {
    btn.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("active");
      btn.classList.toggle("active", isOpen);
      btn.setAttribute("aria-expanded", String(isOpen));
    });
  }

  document.querySelectorAll(".alert-close").forEach((x) => {
    x.addEventListener("click", () => {
      const alert = x.closest(".alert");
      if (alert) alert.remove();
    });
  });
});
