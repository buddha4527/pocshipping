// assets/js/script.js
const WHATSAPP_NUMBER = '971503469650'; // change here if needed
const HEADER_OFFSET = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-height')) || 72;

// helpers
function openWhatsAppMessage(message) {
  const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
  window.open(url, '_blank', 'noopener');
}

function scrollToElementWithOffset(el) {
  if (!el) return;
  const rect = el.getBoundingClientRect();
  const top = window.scrollY + rect.top - HEADER_OFFSET - 12; // extra 12px breathing room
  window.scrollTo({ top, behavior: 'smooth' });
}

/* ------------------------
   Existing generic WhatsApp form
   ------------------------ */
function handleWhatsAppForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const name = form.name ? form.name.value.trim() : '';
    const whatsapp = form.whatsapp ? form.whatsapp.value.trim() : '';
    const pickup = form.pickup ? form.pickup.value.trim() : '';
    const delivery = form.delivery ? form.delivery.value.trim() : '';
    const weight = form.weight ? form.weight.value.trim() : '';
    const item = form.item ? form.item.value.trim() : '';

    let msg = 'POC Shipping - Inquiry\n';
    if (name) msg += `Name: ${name}\n`;
    if (whatsapp) msg += `WhatsApp: ${whatsapp}\n`;
    if (pickup) msg += `Pickup: ${pickup}\n`;
    if (delivery) msg += `Delivery: ${delivery}\n`;
    if (weight) msg += `Weight: ${weight} Kg\n`;
    if (item) msg += `Item: ${item}\n`;

    openWhatsAppMessage(msg);
  });
}

/* ------------------------
   Dual forms (Shipping / Movers)
   ------------------------ */
function initDualForms() {
  const shippingBtn = document.getElementById('showShipping');
  const moversBtn = document.getElementById('showMovers');
  const shippingForm = document.getElementById('shippingForm');
  const moversForm = document.getElementById('moversForm');

  if (!shippingBtn || !moversBtn || !shippingForm || !moversForm) return;

  function showForm(which) {
    if (which === 'shipping') {
      shippingForm.classList.remove('hidden');
      moversForm.classList.add('hidden');
    } else {
      moversForm.classList.remove('hidden');
      shippingForm.classList.add('hidden');
    }
  }

  // show based on button + scroll with offset
  shippingBtn.addEventListener('click', function (e) {
    e.preventDefault();
    showForm('shipping');
    // scroll to the form container (use the form itself)
    scrollToElementWithOffset(shippingForm);
  });

  moversBtn.addEventListener('click', function (e) {
    e.preventDefault();
    showForm('movers');
    scrollToElementWithOffset(moversForm);
  });

  // Hero buttons (one click) - safe if they exist
  document.getElementById('heroShippingBtn')?.addEventListener('click', function (e) {
    e.preventDefault();
    // show + scroll
    showForm('shipping');
    scrollToElementWithOffset(shippingForm);
  });
  document.getElementById('heroMoversBtn')?.addEventListener('click', function (e) {
    e.preventDefault();
    showForm('movers');
    scrollToElementWithOffset(moversForm);
  });

  // shipping form submit
  shippingForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const data = {
      company: document.getElementById('ship_company')?.value.trim() || '',
      email: document.getElementById('ship_email')?.value.trim() || '',
      mode: document.getElementById('transport_mode')?.value || '',
      commodity: document.getElementById('commodity')?.value.trim() || '',
      no_pkgs: document.getElementById('no_pkgs')?.value.trim() || '',
      dims_each: document.getElementById('dims_each')?.value.trim() || '',
      weight_each: document.getElementById('weight_each')?.value.trim() || '',
      incoterm: document.getElementById('incoterm')?.value || '',
      name: document.getElementById('ship_name')?.value.trim() || '',
      phone: document.getElementById('ship_phone')?.value.trim() || '',
      notes: document.getElementById('ship_message')?.value.trim() || ''
    };

    let msg = 'POC Shipping - Shipping Enquiry\n';
    msg += `Form: Shipping\n`;
    if (data.company) msg += `Company: ${data.company}\n`;
    if (data.email) msg += `Email: ${data.email}\n`;
    if (data.mode) msg += `Mode: ${data.mode}\n`;
    if (data.commodity) msg += `Commodity: ${data.commodity}\n`;
    if (data.no_pkgs) msg += `No. of pkgs: ${data.no_pkgs}\n`;
    if (data.dims_each) msg += `Dims (each): ${data.dims_each}\n`;
    if (data.weight_each) msg += `Weight (each): ${data.weight_each}\n`;
    if (data.incoterm) msg += `INCO Term: ${data.incoterm}\n`;
    if (data.name) msg += `Contact: ${data.name}\n`;
    if (data.phone) msg += `Phone: ${data.phone}\n`;
    if (data.notes) msg += `Notes: ${data.notes}\n`;

    openWhatsAppMessage(msg);
  });

  // movers submit
  moversForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const data = {
      from: document.getElementById('move_from')?.value.trim() || '',
      to: document.getElementById('move_to')?.value.trim() || '',
      date: document.getElementById('move_date')?.value || '',
      bedrooms: document.getElementById('no_bedrooms')?.value || '',
      name: document.getElementById('mover_name')?.value.trim() || '',
      phone: document.getElementById('mover_phone')?.value.trim() || '',
      email: document.getElementById('mover_email')?.value.trim() || '',
      notes: document.getElementById('move_notes')?.value.trim() || ''
    };

    let msg = 'POC Shipping - Packers & Movers Enquiry\n';
    msg += `Form: Packers & Movers\n`;
    if (data.from) msg += `From: ${data.from}\n`;
    if (data.to) msg += `To: ${data.to}\n`;
    if (data.date) msg += `Moving Date: ${data.date}\n`;
    if (data.bedrooms) msg += `Bedrooms: ${data.bedrooms}\n`;
    if (data.name) msg += `Contact: ${data.name}\n`;
    if (data.phone) msg += `Phone: ${data.phone}\n`;
    if (data.email) msg += `Email: ${data.email}\n`;
    if (data.notes) msg += `Notes: ${data.notes}\n`;

    openWhatsAppMessage(msg);
  });

  // show shipping by default
  showForm('shipping');
}

/* ------------------------
   Mobile menu, smooth scroll, AOS init
   ------------------------ */
function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('nav-menu');
  if (!btn || !menu) return;
  btn.addEventListener('click', function () {
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!expanded));
  });
  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', function () {
      if (window.innerWidth < 768) {
        menu.classList.add('hidden');
        menu.classList.remove('flex');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  });
}

function initSmoothScroll() {
  // Keep anchors but adjust to offset when clicked
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      scrollToElementWithOffset(target);
    });
  });
}

function initAOS() {
  if (window.AOS && typeof AOS.init === 'function') {
    AOS.init({ once: true });
  }
}

/* ------------------------
   Simple hero carousel auto slide (2 images)
   ------------------------ */
function initHeroCarousel() {
  const carousel = document.getElementById('heroCarousel');
  if (!carousel) return;
  let heroIndex = 0;
  setInterval(() => {
    heroIndex = (heroIndex + 1) % 2;
    carousel.style.transform = `translateX(-${heroIndex * 50}%)`; // each image is 50% of 200% width
  }, 4000);
}

/* ------------------------
   DOM Ready
   ------------------------ */
document.addEventListener('DOMContentLoaded', function () {
  // old simple forms on index/contact if present
  handleWhatsAppForm('whatsappForm');
  handleWhatsAppForm('whatsappFormContact');

  // init new functionality
  initDualForms();
  initMobileMenu();
  initSmoothScroll();
  initAOS();
  initHeroCarousel();
});
