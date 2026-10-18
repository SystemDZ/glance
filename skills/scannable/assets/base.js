(function () {
  // Copy buttons: <button class="copy" data-copy="text">Copy</button>. Falls back to selecting the text.
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var label = btn.textContent;
      function ok() { btn.textContent = "Copied"; btn.classList.add("ok"); setTimeout(function () { btn.textContent = label; btn.classList.remove("ok"); }, 1600); }
      function fallback() {
        var src = btn.closest(".code") ? btn.closest(".code").querySelector("pre") : (btn.closest(".copyrow") || document).querySelector("b");
        if (src) { var r = document.createRange(); r.selectNodeContents(src); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
        btn.textContent = "Press Ctrl/Cmd+C";
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, fallback); else fallback();
    });
  });

  // Remembered tick-boxes: <input type="checkbox" data-persist="unique-id">. Works without storage.
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  var boxes = document.querySelectorAll("input[data-persist]");
  boxes.forEach(function (box) {
    var key = "scannable:" + location.pathname + ":" + box.getAttribute("data-persist");
    if (store.get(key) === "1") box.checked = true;
    box.addEventListener("change", function () { store.set(key, box.checked ? "1" : "0"); update(); });
  });

  // Progress bar: <div class="progress" data-total="5" data-done="3" data-now="4">; ticks listed in data-ticks add to "done".
  function update() {
    document.querySelectorAll(".progress[data-total]").forEach(function (p) {
      var total = +p.dataset.total, done = +(p.dataset.done || 0);
      var ticked = document.querySelectorAll("input[data-persist]:checked").length;
      done = Math.min(total, done + ticked);
      var segs = p.querySelector(".segs"), label = p.querySelector(".progress-label");
      if (segs) {
        segs.innerHTML = "";
        for (var i = 0; i < total; i++) { var s = document.createElement("div"); s.className = "seg" + (i < done ? " done" : i === done ? " now" : ""); segs.appendChild(s); }
      }
      if (label) label.innerHTML = done + " of " + total + " done" + (done < total ? " <span>· you are on step " + (done + 1) + "</span>" : " <span>· all finished</span>");
    });
  }
  update();
})();
