/* ═══════════════════════════════════════════════════════════
   Kačí & Ričí — Svatba 2027 — JavaScript
   ═══════════════════════════════════════════════════════════ */

// ── Sticky nav: zvýraznění aktivní sekce při rolování ────
(function () {
    const nav = document.getElementById('nav');
    const links = nav ? nav.querySelectorAll('a[href^="#"]') : [];
    const sections = [];

    links.forEach(link => {
        const id = link.getAttribute('href').slice(1);
        const section = document.getElementById(id);
        if (section) sections.push({ link, section });
    });

    function onScroll() {
        const scrollY = window.scrollY + 100;
        let current = null;
        sections.forEach(({ link, section }) => {
            if (section.offsetTop <= scrollY) {
                current = link;
            }
        });
        links.forEach(l => l.classList.remove('active'));
        if (current) current.classList.add('active');
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
})();

// ── Plynulé rolování pro navigační odkazy ────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ── Živý odpočet času ("Uvidíme se za...") ─────────────
(function () {
    const el = document.getElementById('countdown');
    if (!el) return;

    const targetDate = new Date(el.getAttribute('data-target') || '2027-06-12T13:00:00+02:00').getTime();
    const dEl = document.getElementById('cd-days');
    const hEl = document.getElementById('cd-hours');
    const mEl = document.getElementById('cd-minutes');
    const sEl = document.getElementById('cd-seconds');

    function update() {
        const now = Date.now();
        const diff = Math.max(0, targetDate - now);

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((diff / (1000 * 60)) % 60);
        const seconds = Math.floor((diff / 1000) % 60);

        if (dEl) dEl.textContent = String(days).padStart(2, '0');
        if (hEl) hEl.textContent = String(hours).padStart(2, '0');
        if (mEl) mEl.textContent = String(minutes).padStart(2, '0');
        if (sEl) sEl.textContent = String(seconds).padStart(2, '0');
    }

    update();
    setInterval(update, 1000);
})();
