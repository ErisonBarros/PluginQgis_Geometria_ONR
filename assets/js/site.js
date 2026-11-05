// Interações do site: sumário automático, menu móvel, tabelas e cópia de código.
(function () {
  "use strict";
  var content = document.querySelector(".content");
  if (!content) return;

  // Tabelas com rolagem horizontal
  content.querySelectorAll("table").forEach(function (t) {
    var w = document.createElement("div");
    w.className = "table-wrap";
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  // Links externos em nova aba
  content.querySelectorAll('a[href^="http"]').forEach(function (a) {
    if (a.hostname !== location.hostname) { a.target = "_blank"; a.rel = "noopener"; }
  });

  // Botão "Copiar" nos blocos de código
  content.querySelectorAll("pre").forEach(function (pre) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "copy-btn"; b.textContent = "Copiar";
    b.addEventListener("click", function () {
      var txt = (pre.querySelector("code") || pre).innerText;
      navigator.clipboard.writeText(txt).then(function () {
        b.textContent = "Copiado"; setTimeout(function () { b.textContent = "Copiar"; }, 1500);
      }).catch(function () { b.textContent = "Erro"; });
    });
    pre.appendChild(b);
  });

  // Sumário a partir de h2/h3
  var toc = document.getElementById("toc");
  var heads = Array.prototype.filter.call(content.querySelectorAll("h2, h3, h4"), function (h) { return h.id; });
  if (toc && heads.length > 1) {
    var ul = document.createElement("ul");
    heads.forEach(function (h) {
      var li = document.createElement("li");
      li.className = "lvl" + h.tagName.charAt(1);
      var a = document.createElement("a");
      a.href = "#" + h.id; a.textContent = h.textContent;
      li.appendChild(a); ul.appendChild(li);
    });
    toc.appendChild(ul);
    if ("IntersectionObserver" in window) {
      var links = toc.querySelectorAll("a");
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            links.forEach(function (l) { l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id); });
          }
        });
      }, { rootMargin: "-80px 0px -70% 0px" });
      heads.forEach(function (h) { obs.observe(h); });
    }
  } else if (toc) {
    toc.parentNode.classList.add("is-empty");
  }

  // Menu móvel
  var btn = document.querySelector(".menu-toggle"), nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
})();
