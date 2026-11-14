/* ═══════════════════════════════════════════════════════════
   Kačí & Ričí — Svatba 2027 — Minimal JS
   ═══════════════════════════════════════════════════════════ */

// ── Sticky nav: highlight active section on scroll ───────
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
        const scrollY = window.scrollY + 120;
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

// ── Smooth-scroll for nav links (fallback for older browsers) ──
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
