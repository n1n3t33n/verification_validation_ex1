/* GUDLFT — ameliorations progressives.
   Le site reste pleinement fonctionnel si ce script ne se charge pas. */
(function () {
  "use strict";

  /* 1) Ombre de l'en-tete au defilement. */
  var header = document.querySelector("[data-header]");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 4);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* 2) Messages flash : bouton de fermeture + disparition automatique. */
  var alertsBox = document.querySelector("[data-alerts]");
  if (alertsBox) {
    var dismiss = function (alert) {
      alert.classList.add("is-leaving");
      window.setTimeout(function () { alert.remove(); }, 200);
    };
    alertsBox.querySelectorAll(".alert").forEach(function (alert) {
      var close = document.createElement("button");
      close.type = "button";
      close.className = "alert__close";
      close.setAttribute("aria-label", "Fermer le message");
      close.textContent = "×";
      close.addEventListener("click", function () { dismiss(alert); });
      alert.appendChild(close);
      window.setTimeout(function () {
        if (document.body.contains(alert)) { dismiss(alert); }
      }, 6000);
    });
  }

  /* 3) Stepper -/+ sur le champ nombre de places. */
  document.querySelectorAll("[data-stepper]").forEach(function (stepper) {
    var input = stepper.querySelector("input[type='number']");
    if (!input) { return; }
    var min = input.min !== "" ? parseInt(input.min, 10) : 1;
    var max = input.max !== "" ? parseInt(input.max, 10) : Infinity;
    stepper.querySelectorAll("[data-step]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var current = parseInt(input.value, 10);
        if (isNaN(current)) { current = min; }
        var next = current + parseInt(btn.getAttribute("data-step"), 10);
        next = Math.max(min, Math.min(max, next));
        input.value = next;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      });
    });
  });
})();
