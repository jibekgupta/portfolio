// portfolio_web/static/portfolio_web/script.js

document.addEventListener("DOMContentLoaded", () => {
  // ----- Mobile menu toggle -----
  const toggleBtn = document.querySelector(".mobile-menu-toggle");
  const nav = document.querySelector(".nav-links");

  if (toggleBtn && nav) {
    const closeMenu = () => {
      nav.classList.remove("active");
      toggleBtn.classList.remove("active");
      toggleBtn.setAttribute("aria-expanded", "false");
    };

    const openMenu = () => {
      nav.classList.add("active");
      toggleBtn.classList.add("active");
      toggleBtn.setAttribute("aria-expanded", "true");
    };

    toggleBtn.addEventListener("click", () => {
      const isOpen = nav.classList.contains("active");
      isOpen ? closeMenu() : openMenu();
    });

    // Close on escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeMenu();
    });

    // Close when clicking outside
    document.addEventListener("click", (e) => {
      const clickedInsideNav = nav.contains(e.target);
      const clickedToggle = toggleBtn.contains(e.target);
      if (!clickedInsideNav && !clickedToggle) closeMenu();
    });

    // Close after clicking a nav link (nice on mobile)
    nav.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => closeMenu());
    });
  }

  // ----- Close alerts (messages framework) -----
  document.querySelectorAll(".alert").forEach((alertEl) => {
    const closeBtn = alertEl.querySelector(".alert-close");
    if (!closeBtn) return;

    closeBtn.addEventListener("click", () => {
      alertEl.style.transition = "opacity 200ms ease, transform 200ms ease";
      alertEl.style.opacity = "0";
      alertEl.style.transform = "translateY(-6px)";
      setTimeout(() => alertEl.remove(), 220);
    });
  });
});
