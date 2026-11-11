/* Theme toggle only. Everything else is rendered at build time. */
(function () {
  var btn = document.getElementById("theme");
  if (!btn) return;
  function apply(mode) {
    document.documentElement.setAttribute("data-theme", mode);
    btn.textContent = mode === "dark" ? "Light" : "Dark";
    try { localStorage.setItem("claude-trends-theme", mode); } catch (e) { /* private mode */ }
  }
  var saved = null;
  try { saved = localStorage.getItem("claude-trends-theme"); } catch (e) { /* ignore */ }
  apply(saved === "light" ? "light" : "dark");
  btn.addEventListener("click", function (ev) {
    ev.preventDefault();
    apply(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });
})();
