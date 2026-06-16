/* ============================================================================
   Phase Walkthrough — shared interactivity engine
   Generic across every phase page. Drives:
     - Story | Reference view toggle (persisted to localStorage + URL hash)
     - the day-by-day timeline stepper
     - glossary tooltips
     - scroll-reveal + scroll progress bar
     - the click-to-check exit-gate checklist
   Everything degrades gracefully: with JS off, both tracks and all timeline
   steps are simply visible.
   ============================================================================ */
(function () {
  "use strict";

  /* ---- view toggle (Story | Reference) ----------------------------------- */
  function initToggle() {
    var buttons = Array.prototype.slice.call(document.querySelectorAll(".toggle button[data-view]"));
    var tracks = {
      story: document.getElementById("track-story"),
      reference: document.getElementById("track-reference")
    };
    if (!buttons.length || !tracks.story || !tracks.reference) return;

    function show(view) {
      if (view !== "story" && view !== "reference") view = "story";
      buttons.forEach(function (b) {
        b.setAttribute("aria-selected", String(b.dataset.view === view));
      });
      Object.keys(tracks).forEach(function (k) {
        tracks[k].classList.toggle("active", k === view);
      });
      try { localStorage.setItem("phase-view", view); } catch (e) {}
      if (("#" + view) !== location.hash) {
        history.replaceState(null, "", "#" + view);
      }
      // a track that was hidden never fired reveal observers — reveal its
      // in-view content once layout has settled for the now-visible track
      requestAnimationFrame(function () { revealAllIn(tracks[view]); });
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { show(b.dataset.view); });
    });

    var initial = (location.hash || "").replace("#", "");
    if (initial !== "story" && initial !== "reference") {
      try { initial = localStorage.getItem("phase-view") || "story"; } catch (e) { initial = "story"; }
    }
    show(initial);

    // in-page links and browser back/forward that change the hash switch views
    window.addEventListener("hashchange", function () {
      var h = (location.hash || "").replace("#", "");
      if (h === "story" || h === "reference") show(h);
    });
  }

  /* ---- timeline stepper --------------------------------------------------- */
  function initTimeline() {
    var tl = document.querySelector("[data-timeline]");
    if (!tl) return;
    var steps = Array.prototype.slice.call(tl.querySelectorAll(".tl-step"));
    if (steps.length < 2) return;

    tl.classList.add("js-stepper");

    var rail = tl.querySelector(".tl-rail");
    var prevBtn = tl.querySelector("[data-tl-prev]");
    var nextBtn = tl.querySelector("[data-tl-next]");
    var count = tl.querySelector("[data-tl-count]");
    var railButtons = [];
    var idx = 0;

    // build the day rail from each step's data-day label
    if (rail) {
      steps.forEach(function (step, i) {
        var b = document.createElement("button");
        b.type = "button";
        b.textContent = step.getAttribute("data-day") || ("Step " + (i + 1));
        b.addEventListener("click", function () { go(i); });
        rail.appendChild(b);
        railButtons.push(b);
      });
    }

    function go(n) {
      idx = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, i) { s.classList.toggle("active", i === idx); });
      railButtons.forEach(function (b, i) {
        b.setAttribute("aria-current", String(i === idx));
        if (i <= idx) b.classList.add("visited");
      });
      if (prevBtn) prevBtn.disabled = (idx === 0);
      if (nextBtn) nextBtn.disabled = (idx === steps.length - 1);
      if (count) count.textContent = (idx + 1) + " / " + steps.length;
    }

    if (prevBtn) prevBtn.addEventListener("click", function () { go(idx - 1); });
    if (nextBtn) nextBtn.addEventListener("click", function () {
      if (idx === steps.length - 1) return;
      go(idx + 1);
      steps[idx].scrollIntoView({ block: "nearest" });
    });

    // arrow keys when the timeline has focus within it
    tl.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(idx + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(idx - 1); }
    });

    go(0);
  }

  /* ---- glossary tooltips -------------------------------------------------- */
  function initTooltips() {
    var terms = Array.prototype.slice.call(document.querySelectorAll(".term[data-def]"));
    if (!terms.length) return;

    var tip = document.createElement("div");
    tip.id = "tip";
    tip.setAttribute("role", "tooltip");
    document.body.appendChild(tip);
    var hideTimer = null;

    function place(el) {
      var label = el.getAttribute("data-term") || el.textContent;
      tip.innerHTML = '<span class="t"></span>';
      tip.querySelector(".t").textContent = label;
      tip.appendChild(document.createTextNode(el.getAttribute("data-def")));
      tip.classList.add("show");
      // measure then position (fixed — never clipped by overflow)
      var r = el.getBoundingClientRect();
      var tr = tip.getBoundingClientRect();
      var left = Math.min(Math.max(8, r.left), window.innerWidth - tr.width - 8);
      var top = r.top - tr.height - 10;
      if (top < 8) top = r.bottom + 10;       // flip below if no room above
      tip.style.left = left + "px";
      tip.style.top = top + "px";
    }
    function hide() { tip.classList.remove("show"); }

    terms.forEach(function (el) {
      el.setAttribute("tabindex", "0");
      el.addEventListener("mouseenter", function () { clearTimeout(hideTimer); place(el); });
      el.addEventListener("mouseleave", function () { hideTimer = setTimeout(hide, 80); });
      el.addEventListener("focus", function () { place(el); });
      el.addEventListener("blur", hide);
      el.addEventListener("click", function (e) { e.preventDefault(); place(el); });
    });
    window.addEventListener("scroll", hide, { passive: true });
  }

  /* ---- exit-gate checklist ------------------------------------------------ */
  function initGate() {
    var items = Array.prototype.slice.call(document.querySelectorAll(".gate li"));
    items.forEach(function (li) {
      var box = li.querySelector(".box");
      function toggle() {
        var on = li.classList.toggle("checked");
        if (box) box.textContent = on ? "✓" : "";
        li.setAttribute("aria-pressed", String(on));
      }
      li.setAttribute("role", "button");
      li.setAttribute("tabindex", "0");
      li.setAttribute("aria-pressed", "false");
      li.addEventListener("click", toggle);
      li.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
      });
    });
  }

  /* ---- scroll reveal + progress ------------------------------------------ */
  function revealAllIn(root) {
    if (!root) return;
    Array.prototype.slice.call(root.querySelectorAll(".reveal:not(.in)")).forEach(function (el) {
      if (el.offsetParent === null) return;            // skip hidden (inactive track)
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) el.classList.add("in");
    });
  }

  function initReveal() {
    var els = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
    if (!els.length) return;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    // No observer support or motion disabled: leave everything visible, no animation.
    if (!("IntersectionObserver" in window) || reduce) return;

    document.documentElement.classList.add("js-anim");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });

    // Safety sweep once layout has settled: reveal anything at or above the
    // fold that the observer may not have fired for (e.g. direct deep-link load).
    function sweep() {
      els.forEach(function (el) {
        if (el.classList.contains("in") || el.offsetParent === null) return;
        if (el.getBoundingClientRect().top < window.innerHeight * 1.15) el.classList.add("in");
      });
    }
    window.addEventListener("load", function () { requestAnimationFrame(sweep); });
  }

  function initProgress() {
    var bar = document.querySelector(".progress .bar");
    if (!bar) return;
    function update() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    }
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---- boot --------------------------------------------------------------- */
  function boot() {
    initToggle();
    initTimeline();
    initTooltips();
    initGate();
    initReveal();
    initProgress();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
