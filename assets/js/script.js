/* POC Shipping — site script */

/* ===== SETTINGS: edit these two lines ===== */
// WhatsApp number in international format, digits only (no + or spaces)
const WHATSAPP_NUMBER = '919400776671';
// Google Apps Script web-app URL (see SETUP-ENQUIRIES.md). Leave '' to send enquiries by WhatsApp only.
const ENQUIRY_ENDPOINT = '';
/* ========================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu
  const menuBtn = document.getElementById('menuBtn');
  const navLinks = document.getElementById('navLinks');
  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }

  // Footer year
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  // Plain WhatsApp links use the configured number
  document.querySelectorAll('[data-wa]').forEach(el => {
    const text = el.getAttribute('data-wa') || 'Hi POC Shipping, I would like a container shipping quote.';
    el.href = waLink(text);
    el.target = '_blank';
    el.rel = 'noopener';
  });

  // Reveal on scroll
  const items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    items.forEach(el => io.observe(el));
  } else {
    items.forEach(el => el.classList.add('in'));
  }

  initQuoteForm();
});

function waLink(text) {
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(text)}`;
}

function makeRef() {
  const d = new Date();
  const p = n => String(n).padStart(2, '0');
  const rand = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `POC-${String(d.getFullYear()).slice(2)}${p(d.getMonth() + 1)}${p(d.getDate())}-${rand}`;
}

function initQuoteForm() {
  const form = document.getElementById('quoteForm');
  if (!form) return;

  const fclBox = document.getElementById('fclFields');
  const lclBox = document.getElementById('lclFields');
  const status = document.getElementById('formStatus');
  const submitBtn = form.querySelector('button[type="submit"]');

  // Toggle FCL / LCL fields
  const syncType = () => {
    const type = (form.querySelector('input[name="shipment_type"]:checked') || {}).value;
    const isFcl = type !== 'LCL';
    fclBox.classList.toggle('hidden', !isFcl);
    lclBox.classList.toggle('hidden', isFcl);
    fclBox.querySelectorAll('[data-req]').forEach(i => { i.required = isFcl; });
    lclBox.querySelectorAll('[data-req]').forEach(i => { i.required = !isFcl; });
  };
  form.querySelectorAll('input[name="shipment_type"]').forEach(r => r.addEventListener('change', syncType));
  syncType();

  // Pre-fill destination from ?to=... (used by route pages) or data-dest on the form
  const dest = form.querySelector('[name="destination"]');
  const preset = new URLSearchParams(location.search).get('to') || form.getAttribute('data-dest');
  if (dest && preset && !dest.value) dest.value = preset;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (form.website && form.website.value) return; // spam trap
    if (!form.reportValidity()) return;

    const fd = new FormData(form);
    const data = Object.fromEntries(fd.entries());
    delete data.website;
    data.reference = makeRef();
    data.page = location.pathname;
    data.submitted_at = new Date().toISOString();

    const msg = buildMessage(data);

    if (!ENQUIRY_ENDPOINT) {
      window.open(waLink(msg), '_blank');
      showStatus('ok', `Thanks! WhatsApp has opened with your enquiry (ref ${data.reference}). Please press send there.`);
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';
    try {
      await fetch(ENQUIRY_ENDPOINT, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(data).toString()
      });
      form.reset();
      syncType();
      showStatus('ok', `Thank you, ${escapeHtml(data.name || '')}! Your enquiry <strong>${data.reference}</strong> has been received. We'll email your quote shortly.<br><a class="btn btn-whatsapp" style="margin-top:12px" target="_blank" rel="noopener" href="${waLink(msg)}">Also send on WhatsApp for a faster reply</a>`);
    } catch (err) {
      showStatus('err', `Sorry, something went wrong. Please <a target="_blank" rel="noopener" href="${waLink(msg)}">send your enquiry on WhatsApp</a> instead.`);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Get my quote';
    }
  });

  function showStatus(kind, html) {
    status.className = `form-status ${kind}`;
    status.innerHTML = html;
    status.classList.remove('hidden');
    status.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

function buildMessage(d) {
  const lines = [
    `*Container quote request* (${d.reference})`,
    '',
    `Type: ${d.shipment_type || '-'}`,
    `From: ${d.origin || '-'}`,
    `To: ${d.destination || '-'}`
  ];
  if (d.shipment_type === 'LCL') {
    lines.push(`Packages: ${d.packages || '-'}`, `Volume: ${d.volume_cbm || '-'} CBM`);
  } else {
    lines.push(`Container: ${d.container_qty || '-'} x ${d.container_type || '-'}`);
  }
  lines.push(
    `Total weight: ${d.weight_kg || '-'} kg`,
    `Commodity: ${d.commodity || '-'}`,
    `Hazardous: ${d.hazardous || '-'}`,
    `Service: ${d.service || '-'}`,
    `Cargo ready: ${d.ready_date || '-'}`,
    '',
    `Name: ${d.name || '-'}`,
    `Company: ${d.company || '-'}`,
    `Email: ${d.email || '-'}`,
    `Phone: ${d.phone || '-'}`
  );
  if (d.notes) lines.push('', `Notes: ${d.notes}`);
  return lines.join('\n');
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
