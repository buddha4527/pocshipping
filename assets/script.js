// Handles WhatsApp form submission on both index and contact pages

function handleWhatsAppForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const name = encodeURIComponent(form.name.value.trim());
    const whatsapp = encodeURIComponent(form.whatsapp.value.trim());
    const pickup = encodeURIComponent(form.pickup.value.trim());
    const delivery = encodeURIComponent(form.delivery.value.trim());
    const weight = encodeURIComponent(form.weight.value.trim());
    const item = encodeURIComponent(form.item.value.trim());

    const msg = `Name: ${name}%0AWhatsApp: ${whatsapp}%0APickup: ${pickup}%0ADelivery: ${delivery}%0AWeight: ${weight}Kg%0AItem: ${item}`;
    const url = `https://wa.me/971503469650?text=${msg}`;
    window.open(url, "_blank");
  });
}

document.addEventListener("DOMContentLoaded", function () {
  handleWhatsAppForm("whatsappForm");
  handleWhatsAppForm("whatsappFormContact");

  // Smooth scroll for nav and CTA links
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", function (e) {
      const target = document.querySelector(link.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
});
