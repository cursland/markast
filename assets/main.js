/* ──────────────────────────────────────────────────────────────────────────
   markast docs — theme + sidebar + TOC scroll-spy
   ────────────────────────────────────────────────────────────────────────── */

(function () {
    /* ---- Theme (light / dark) -------------------------------------------- */
    const themeKey = "markast-theme";
    const root = document.documentElement;

    function applyTheme(t) {
        root.setAttribute("data-theme", t);
        const btn = document.querySelector("[data-theme-toggle]");
        if (btn) {
            btn.setAttribute("aria-pressed", t === "dark");
            const sun = btn.querySelector(".icon-sun");
            const moon = btn.querySelector(".icon-moon");
            if (sun && moon) {
                sun.style.display  = t === "dark" ? "none"  : "inline";
                moon.style.display = t === "dark" ? "inline" : "none";
            }
        }
    }

    function initialTheme() {
        const stored = localStorage.getItem(themeKey);
        if (stored) return stored;
        return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }

    applyTheme(initialTheme());

    document.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-theme-toggle]");
        if (!btn) return;
        const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        applyTheme(next);
        localStorage.setItem(themeKey, next);
    });

    /* ---- Language preference --------------------------------------------- */
    const langKey = "markast-lang";

    document.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-lang]");
        if (!btn) return;
        localStorage.setItem(langKey, btn.dataset.lang);
    });

    /* ---- Sidebar (mobile drawer) ----------------------------------------- */
    const sidebar = document.querySelector(".sidebar");
    const backdrop = document.querySelector(".sidebar-backdrop");
    const navToggle = document.querySelector(".nav-toggle");

    function openSidebar(open) {
        if (!sidebar || !backdrop) return;
        sidebar.classList.toggle("open", open);
        backdrop.classList.toggle("show", open);
        document.body.style.overflow = open ? "hidden" : "";
    }

    if (navToggle) navToggle.addEventListener("click", () => openSidebar(!sidebar.classList.contains("open")));
    if (backdrop)  backdrop.addEventListener("click",  () => openSidebar(false));

    document.addEventListener("click", (e) => {
        const a = e.target.closest(".sidebar a");
        if (a) openSidebar(false);
    });

    /* ---- Highlight current sidebar link ---------------------------------- */
    const path = location.pathname.replace(/\/$/, "").split("/").pop() || "index.html";
    document.querySelectorAll(".sidebar a").forEach((a) => {
        const href = a.getAttribute("href") || "";
        const last = href.split("/").pop();
        if (last === path) a.classList.add("active");
    });

    /* ---- TOC: build & scroll-spy ----------------------------------------- */
    const toc = document.querySelector(".toc-list");
    const headings = document.querySelectorAll(".content h2, .content h3");
    if (toc && headings.length) {
        headings.forEach((h) => {
            if (!h.id) {
                h.id = h.textContent.trim().toLowerCase()
                    .replace(/[^\w\s-]/g, "")
                    .replace(/\s+/g, "-");
            }
            const a = document.createElement("a");
            a.href = "#" + h.id;
            a.textContent = h.textContent;
            if (h.tagName === "H3") a.classList.add("toc-h3");
            toc.appendChild(a);
        });

        const links = toc.querySelectorAll("a");
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                const id = entry.target.id;
                const link = toc.querySelector(`a[href="#${id}"]`);
                if (!link) return;
                if (entry.isIntersecting) {
                    links.forEach((l) => l.classList.remove("active"));
                    link.classList.add("active");
                }
            });
        }, { rootMargin: "-72px 0px -70% 0px", threshold: 0 });
        headings.forEach((h) => observer.observe(h));
    }

    /* ---- External links open in new tab ---------------------------------- */
    document.querySelectorAll(".content a[href^='http']").forEach((a) => {
        if (!a.getAttribute("target")) {
            a.setAttribute("target", "_blank");
            a.setAttribute("rel", "noopener noreferrer");
        }
    });
})();
