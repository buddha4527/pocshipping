// assets/js/script.js
// Combined site JS: WhatsApp handlers, Shipping/Movers forms, mobile menu, smooth scroll, AOS init.

// ----- Configuration -----
const WHATSAPP_NUMBER = '971503469650'; // no + sign. Change here if needed.

// ----- Helper: open WhatsApp with encoded message -----
function openWhatsAppMessage(message) {
  const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
  // use _blank to open new tab / app where available
  window.open(url, '_blank', 'noopener');
}

// ----- Existing handler: generic WhatsApp form (index + contact pages) -----
function handleWhatsAppForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Safely read fields (guard if any missing)
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

// ----- New: Shipping & Packers/Movers forms and toggle -----
function initDualForms() {
  const shippingBtn = document.getElementById('showShipping');
  const moversBtn = document.getElementById('showMovers');
  const shippingForm = document.getElementById('shippingForm');
  const moversForm = document.getElementById('moversForm');

  // if forms/buttons are not present, silently return
  if (!shippingForm || !moversForm || !shippingBtn || !moversBtn) return;

  function showForm(which) {
    if (which === 'shipping') {
      shippingForm.classList.remove('hidden');
      moversForm.classList.add('hidden');
      shippingBtn.classList.add('opacity-100');
      moversBtn.classList.remove('opacity-100');
    } else {
      moversForm.classList.remove('hidden');
      shippingForm.classList.add('hidden');
      moversBtn.classList.add('opacity-100');
      shippingBtn.classList.remove('opacity-100');
    }
  }

  // attach button listeners
  shippingBtn.addEventListener('click', function () { showForm('shipping'); });
  moversBtn.addEventListener('click', function () { showForm('movers'); });

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

  // movers form submit
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

// ----- Mobile hamburger menu toggle -----
function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('nav-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', function () {
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
    // update aria-expanded if present
    if (btn.getAttribute) {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
    }
  });

  // Optional: close on link click (mobile)
  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', function () {
      if (window.innerWidth < 768) {
        menu.classList.add('hidden');
        menu.classList.remove('flex');
        if (btn.getAttribute) btn.setAttribute('aria-expanded', 'false');
      }
    });
  });
}

// ----- Smooth scrolling for anchor links -----
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function (e) {
      const targetSelector = this.getAttribute('href');
      if (!targetSelector || targetSelector === '#') return;
      const target = document.querySelector(targetSelector);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

// ----- AOS init (if AOS is loaded) -----
function initAOS() {
  if (window.AOS && typeof AOS.init === 'function') {
    AOS.init({ once: true });
  }
}

// ----- DOM ready -----
document.addEventListener('DOMContentLoaded', function () {
  // existing simple forms used on index/contact older pages
  handleWhatsAppForm('whatsappForm');
  handleWhatsAppForm('whatsappFormContact');

  // new dual forms
  initDualForms();

  // UI helpers
  initMobileMenu();
  initSmoothScroll();

  // AOS
  initAOS();

  // Hero buttons → open correct form
const heroShippingBtn = document.getElementById("heroShippingBtn");
const heroMoversBtn = document.getElementById("heroMoversBtn");

if (heroShippingBtn) {
  heroShippingBtn.addEventListener("click", function () {
    document.getElementById("showShipping")?.click();
  });
}

if (heroMoversBtn) {
  heroMoversBtn.addEventListener("click", function () {
    document.getElementById("showMovers")?.click();
  });
}

});
