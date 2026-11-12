#!/usr/bin/env python3
"""Builds the static HTML pages for pocshipping.com.

Edit the content below, then run:  python3 _build/build.py
The generated .html files are what GitHub Pages serves.
(Folders starting with "_" are not published by GitHub Pages.)
"""
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://pocshipping.com"

BIZ = {
    "name": "POC Shipping",
    "since": "2012",
    "email": "sales@pocshipping.com",
    "wa_display": "+91 94007 76671",
    "wa_digits": "919400776671",
    "address": "Office No. 304, Al Murar, Dubai, UAE",
}

# ---------------------------------------------------------------- routes
# Transit times are indicative port-to-port ranges; confirm with each quote.
ROUTES = [
    {
        "slug": "jebel-ali-to-mombasa", "port": "Mombasa", "country": "Kenya", "region": "East Africa",
        "transit": "10–16 days",
        "gateway": "Kenya and inland Uganda, Rwanda and South Sudan",
        "cargo": ["Building materials and hardware", "Electronics and home appliances", "Auto parts and tyres", "General trading goods and FMCG"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "KEBS PVoC Certificate of Conformity for regulated goods", "Importer's PIN / clearing agent details"],
    },
    {
        "slug": "jebel-ali-to-dar-es-salaam", "port": "Dar es Salaam", "country": "Tanzania", "region": "East Africa",
        "transit": "12–18 days",
        "gateway": "Tanzania and transit cargo to Zambia, Malawi, DR Congo, Burundi and Rwanda",
        "cargo": ["Building and construction materials", "Electronics", "Used vehicles and spare parts", "General merchandise"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "TBS PVoC certificate for regulated goods", "Importer TIN / clearing agent details"],
    },
    {
        "slug": "jebel-ali-to-djibouti", "port": "Djibouti", "country": "Djibouti", "region": "East Africa",
        "transit": "6–10 days",
        "gateway": "Djibouti and transit cargo to Ethiopia",
        "cargo": ["Machinery and equipment", "Construction materials", "Food and consumer goods", "Transit cargo for Ethiopia"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "Transit documents for Ethiopia-bound cargo", "Consignee / clearing agent details"],
    },
    {
        "slug": "jebel-ali-to-lagos", "port": "Lagos (Apapa / Tin Can)", "country": "Nigeria", "region": "West Africa",
        "transit": "25–35 days",
        "gateway": "Nigeria — Africa's largest consumer market",
        "cargo": ["Electronics and mobile accessories", "Auto parts and tyres", "Textiles and garments", "General trading goods"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "Form M (opened by the importer)", "SONCAP certificate for regulated goods"],
    },
    {
        "slug": "jebel-ali-to-tema", "port": "Tema", "country": "Ghana", "region": "West Africa",
        "transit": "25–35 days",
        "gateway": "Ghana and transit cargo to Burkina Faso, Mali and Niger",
        "cargo": ["Building materials", "Electronics and appliances", "Used vehicles and spare parts", "General merchandise"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "Import declaration via the importer's clearing agent", "Certificate of origin (if requested)"],
    },
    {
        "slug": "jebel-ali-to-durban", "port": "Durban", "country": "South Africa", "region": "Southern Africa",
        "transit": "16–22 days",
        "gateway": "South Africa and inland Southern African countries",
        "cargo": ["Machinery and industrial goods", "Furniture and interior materials", "Consumer goods", "Auto parts"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "Importer's customs code (registered with SARS)", "Certificate of origin (if requested)"],
    },
    {
        "slug": "jebel-ali-to-rotterdam", "port": "Rotterdam", "country": "Netherlands", "region": "Europe",
        "transit": "25–40 days",
        "gateway": "Netherlands, Belgium, Germany and wider Europe",
        "cargo": ["Re-export goods from UAE free zones", "Furniture and interior materials", "Food products (dry and reefer)", "Industrial goods"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "Importer's EORI number", "Certificate of origin and product certificates where required"],
    },
    {
        "slug": "jebel-ali-to-hamburg", "port": "Hamburg", "country": "Germany", "region": "Europe",
        "transit": "27–42 days",
        "gateway": "Germany, Scandinavia and Central / Eastern Europe",
        "cargo": ["Re-export goods", "Industrial goods and machinery parts", "Furniture and interiors", "Consumer goods"],
        "docs": ["Commercial invoice and packing list", "Bill of lading", "Importer's EORI number", "Certificate of origin and product certificates where required"],
    },
]

REGION_EXTRA = {
    "East Africa": ["Berbera", "Mogadishu", "Port Sudan"],
    "West Africa": ["Lomé", "Abidjan", "Cotonou", "Dakar"],
    "Southern Africa": ["Maputo", "Beira", "Walvis Bay"],
    "Europe": ["Antwerp", "Felixstowe", "Genoa", "Barcelona"],
}

# ---------------------------------------------------------------- icons
def icon(name):
    paths = {
        "container": '<rect x="2" y="6" width="20" height="13" rx="1.5"/><path d="M6 9v7M10 9v7M14 9v7M18 9v7"/>',
        "boxes": '<path d="M3 13h8v8H3zM13 13h8v8h-8zM8 3h8v8H8z"/>',
        "snow": '<path d="M12 2v20M4.9 6l14.2 12M19.1 6 4.9 18"/>',
        "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
        "truck": '<path d="M1 6h13v10H1zM14 10h4l3 3v3h-7z"/><circle cx="5.5" cy="18" r="1.8"/><circle cx="17.5" cy="18" r="1.8"/>',
        "shield": '<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="m9 12 2 2 4-4"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.5 3.8 9s-1.3 6.5-3.8 9c-2.5-2.5-3.8-5.5-3.8-9S9.5 5.5 12 3z"/>',
        "flatrack": '<path d="M2 17h20M4 17V9M20 17V9M6 14h12"/><circle cx="7" cy="20" r="1"/><circle cx="17" cy="20" r="1"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        "pin": '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
        "chat": '<path d="M21 12a8 8 0 0 1-11.8 7L3 21l2-6A8 8 0 1 1 21 12z"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.4c-2.1 0-4.1-.6-5.9-1.7l-.4-.3-3.8 1.2 1.2-3.7-.3-.4a10.4 10.4 0 0 1-1.6-5.6C5.2 10 10 5.3 16 5.3S26.8 10 26.8 15.8 22 26.4 16 26.4zm5.9-7.8c-.3-.2-1.9-1-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.7c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.2-.6-.4z"/></svg>'

LOGO_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="3" y="7" width="18" height="11" rx="1"/><path d="M7.5 10v5M12 10v5M16.5 10v5"/></svg>'

# ---------------------------------------------------------------- layout
NAV = [("index.html", "Home"), ("services.html", "Services"), ("routes.html", "Routes"), ("about.html", "About"), ("faq.html", "FAQ"), ("contact.html", "Contact")]


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": BIZ["name"],
        "description": "Container shipping (FCL & LCL) from UAE / Jebel Ali to Africa, Europe and worldwide.",
        "url": SITE + "/",
        "email": BIZ["email"],
        "telephone": "+" + BIZ["wa_digits"],
        "foundingDate": BIZ["since"],
        "image": SITE + "/assets/img/hero-ship-1920.webp",
        "address": {"@type": "PostalAddress", "streetAddress": "Office No. 304, Al Murar", "addressLocality": "Dubai", "addressCountry": "AE"},
        "areaServed": ["United Arab Emirates", "Africa", "Europe"],
    }


def page(path, title, description, body, active="", extra_schema=None, hero_img=None, base=None):
    depth = path.count("/")
    b = base if base is not None else "../" * depth  # relative base
    nav = "".join(
        f'<li><a href="{b}{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>' for href, label in NAV
    )
    canonical = SITE + "/" + ("" if path == "index.html" else path)
    schemas = [org_schema()] + (extra_schema or [])
    schema_html = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    preload = f'<link rel="preload" as="image" href="{b}assets/img/{hero_img}-1920.webp" media="(min-width: 961px)"><link rel="preload" as="image" href="{b}assets/img/{hero_img}-960.webp" media="(max-width: 960px)">' if hero_img else ""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="POC Shipping">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/img/hero-ship-1920.webp">
  <meta name="theme-color" content="#0A1A2F">
  <link rel="icon" href="{b}assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
  {preload}
  <link rel="stylesheet" href="{b}assets/css/styles.css">
  {schema_html}
</head>
<body>
<header class="site-header">
  <nav class="container nav" aria-label="Main">
    <a class="logo" href="{b}index.html"><span class="logo-mark">{LOGO_SVG}</span><span>POC Shipping<small>Container Freight · Dubai</small></span></a>
    <button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="navLinks">&#9776;</button>
    <ul class="nav-links" id="navLinks">{nav}<li><a class="btn btn-primary" href="{b}quote.html">Get a Quote</a></li></ul>
  </nav>
</header>
<main>
{body.replace("{{B}}", b)}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="{b}index.html"><span class="logo-mark">{LOGO_SVG}</span><span>POC Shipping</span></a>
        <p style="margin-top:14px">Your point of contact for FCL &amp; LCL container shipping from the UAE to Africa, Europe and worldwide. Since {BIZ["since"]}.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{b}services.html#fcl">FCL — Full container</a></li>
          <li><a href="{b}services.html#lcl">LCL — Shared container</a></li>
          <li><a href="{b}services.html#reefer">Reefer containers</a></li>
          <li><a href="{b}services.html#docs">Documentation</a></li>
        </ul>
      </div>
      <div>
        <h4>Popular routes</h4>
        <ul>
          {"".join(f'<li><a href="{b}routes/{r["slug"]}.html">Jebel Ali → {r["port"].split(" (")[0]}</a></li>' for r in ROUTES[:5])}
          <li><a href="{b}routes.html">All routes</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></li>
          <li><a data-wa href="#">WhatsApp {BIZ["wa_display"]}</a></li>
          <li>{BIZ["address"]}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {BIZ["since"]}–<span data-year></span> POC Shipping. All rights reserved.</span>
      <span>Container shipping from UAE · Jebel Ali · Dubai</span>
    </div>
  </div>
</footer>
<a class="wa-float" data-wa href="#" aria-label="Chat on WhatsApp">{WA_SVG}</a>
<script src="{b}assets/js/script.js"></script>
</body>
</html>
"""
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return path


def hero_style(img):
    # Separate mobile / desktop images via inline media query
    return (f'<style>.hero-{img}{{background-image:url("{{{{B}}}}assets/img/{img}-960.webp")}}'
            f'@media(min-width:961px){{.hero-{img}{{background-image:url("{{{{B}}}}assets/img/{img}-1920.webp")}}}}</style>')


# ---------------------------------------------------------------- shared blocks
def quote_form(dest=""):
    dest_attr = f' data-dest="{escape(dest)}"' if dest else ""
    ctypes = ["20ft Standard", "40ft Standard", "40ft High Cube", "20ft Reefer", "40ft Reefer", "Open Top", "Flat Rack", "Not sure"]
    return f"""
<form class="quote-form" id="quoteForm" novalidate{dest_attr}>
  <h3>Request a container quote</h3>
  <p class="form-sub">Takes about 1 minute. We reply with a clear, itemised price.</p>

  <div class="fieldset-title">Shipment</div>
  <div class="field">
    <label>Shipment type <span class="req">*</span></label>
    <div class="seg" role="radiogroup">
      <label><input type="radio" name="shipment_type" value="FCL" checked><span>FCL — Full container</span></label>
      <label><input type="radio" name="shipment_type" value="LCL"><span>LCL — Shared container</span></label>
    </div>
  </div>
  <div class="form-row">
    <div class="field"><label for="origin">From (port / city) <span class="req">*</span></label><input id="origin" name="origin" value="Jebel Ali, UAE" required></div>
    <div class="field"><label for="destination">To (port / city, country) <span class="req">*</span></label><input id="destination" name="destination" placeholder="e.g. Mombasa, Kenya" required></div>
  </div>
  <div id="fclFields" class="form-row">
    <div class="field"><label for="container_type">Container type <span class="req">*</span></label>
      <select id="container_type" name="container_type" data-req>{"".join(f"<option>{c}</option>" for c in ctypes)}</select></div>
    <div class="field"><label for="container_qty">No. of containers <span class="req">*</span></label><input id="container_qty" name="container_qty" type="number" min="1" value="1" data-req></div>
  </div>
  <div id="lclFields" class="form-row hidden">
    <div class="field"><label for="packages">No. of packages / pallets <span class="req">*</span></label><input id="packages" name="packages" type="number" min="1" data-req></div>
    <div class="field"><label for="volume_cbm">Total volume (CBM) <span class="req">*</span></label><input id="volume_cbm" name="volume_cbm" type="number" min="0" step="0.01" placeholder="e.g. 4.5" data-req></div>
  </div>
  <div class="form-row">
    <div class="field"><label for="commodity">Commodity <span class="req">*</span></label><input id="commodity" name="commodity" placeholder="e.g. tiles, electronics, auto parts" required></div>
    <div class="field"><label for="weight_kg">Total weight (kg)</label><input id="weight_kg" name="weight_kg" type="number" min="0" placeholder="e.g. 18000"></div>
  </div>
  <div class="form-row three">
    <div class="field"><label for="service">Service</label>
      <select id="service" name="service"><option>Port to port</option><option>Door to port</option><option>Port to door</option><option>Door to door</option><option>Not sure</option></select></div>
    <div class="field"><label for="hazardous">Hazardous (DG)?</label>
      <select id="hazardous" name="hazardous"><option>No</option><option>Yes</option><option>Not sure</option></select></div>
    <div class="field"><label for="ready_date">Cargo ready date</label><input id="ready_date" name="ready_date" type="date"></div>
  </div>

  <div class="fieldset-title">Your details</div>
  <div class="form-row">
    <div class="field"><label for="name">Full name <span class="req">*</span></label><input id="name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="company">Company</label><input id="company" name="company" autocomplete="organization"></div>
  </div>
  <div class="form-row">
    <div class="field"><label for="email">Email <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="phone">Phone / WhatsApp <span class="req">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+971 …" required></div>
  </div>
  <div class="field"><label for="notes">Anything else?</label><textarea id="notes" name="notes" rows="3" placeholder="Special requirements, Incoterm, target price, etc."></textarea></div>
  <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">

  <div class="form-actions">
    <button class="btn btn-primary btn-block" type="submit">Get my quote</button>
  </div>
  <div id="formStatus" class="form-status hidden" role="status" aria-live="polite"></div>
  <p class="privacy">We only use your details to prepare your quote.</p>
</form>"""


def quote_section(dest="", heading="Get a competitive container quote", sub="Tell us what you're shipping. We compare rates across our carrier network and send you a clear, itemised quote — usually within a few hours on working days."):
    return f"""
<section class="section section-dark" id="quote">
  <div class="container quote-wrap">
    <div class="quote-side reveal">
      <span class="eyebrow">Free quote</span>
      <h2>{heading}</h2>
      <p style="color:#c6d3e2">{sub}</p>
      <ul>
        <li>Rates compared across multiple shipping lines</li>
        <li>Itemised: ocean freight, local charges, documentation</li>
        <li>FCL and LCL from Jebel Ali and other UAE ports</li>
        <li>One point of contact from booking to arrival</li>
      </ul>
      <p style="color:#c6d3e2">Prefer to chat? <a style="color:#fff" data-wa href="#">Message us on WhatsApp</a> or email <a style="color:#fff" href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>.</p>
    </div>
    <div class="reveal">{quote_form(dest)}</div>
  </div>
</section>"""


def cta_band(text="Have a shipment coming up?", sub="Send the details and get a quote today."):
    return f"""
<section class="cta-band">
  <div class="container">
    <div><h2>{text}</h2><p>{sub}</p></div>
    <a class="btn btn-primary" href="{{{{B}}}}quote.html">Get a free quote</a>
  </div>
</section>"""


def routes_grid(limit_link=True):
    regions = {}
    for r in ROUTES:
        regions.setdefault(r["region"], []).append(r)
    cards = []
    icons = {"East Africa": "globe", "West Africa": "globe", "Southern Africa": "globe", "Europe": "globe"}
    for region, rs in regions.items():
        items = "".join(
            f'<li><a href="{{{{B}}}}routes/{r["slug"]}.html">{r["port"].split(" (")[0]}, {r["country"]}</a><span class="tt">~{r["transit"]}</span></li>'
            for r in rs)
        extra = ", ".join(REGION_EXTRA.get(region, []))
        cards.append(f"""<div class="card route-group reveal"><h3><span class="icon" style="margin:0;width:36px;height:36px">{icon(icons[region])}</span>{region}</h3>
<ul class="route-list">{items}</ul><p class="note">Also: {extra} and more.</p></div>""")
    return f'<div class="grid grid-2">{"".join(cards)}</div>'


# ---------------------------------------------------------------- FAQ data
FAQS = [
    ("How quickly will I get a quote?", "Most quotes are sent within a few hours on working days. Quotes for special equipment (reefer, flat rack, hazardous cargo) or unusual destinations can take a little longer because we check space and rates with the shipping lines."),
    ("What's the difference between FCL and LCL?", "FCL (Full Container Load) means you book a whole 20ft or 40ft container for your cargo only. LCL (Less than Container Load) means your cargo shares a container with other shippers and you pay by volume (CBM). As a rough guide, LCL is usually cheaper for shipments under about 13–15 CBM; above that, a 20ft FCL is often better value."),
    ("What details do you need for a quote?", "Origin and destination, FCL or LCL, container type and quantity (or number of packages and total CBM for LCL), the commodity, approximate weight, cargo-ready date and whether you need pickup or delivery. Our quote form asks for exactly this."),
    ("What is included in the quote?", "Every quote is itemised so you can compare: ocean freight, origin charges in the UAE, documentation / bill of lading fees and any surcharges. Destination charges, duties and taxes are shown separately or excluded, depending on the service you choose. The validity date is stated on each quote."),
    ("Which countries do you ship to?", "Our main focus is container shipping from the UAE to East, West and Southern Africa and to Europe. We also quote for the Indian Subcontinent, the GCC and other destinations worldwide on request."),
    ("How long does shipping take?", "Typical port-to-port transit from Jebel Ali is around 6–18 days to East Africa, 25–35 days to West Africa and 25–40 days to Northern Europe. Exact times depend on the shipping line and routing; we confirm the transit time with every quote."),
    ("Which documents are needed?", "Usually a commercial invoice, packing list and the bill of lading we arrange. Many destinations also need country-specific certificates (for example KEBS PVoC for Kenya or SONCAP and Form M for Nigeria). We'll tell you what applies to your cargo and destination."),
    ("Can you ship hazardous or temperature-controlled cargo?", "Yes, on request. For hazardous (DG) cargo we need the MSDS and UN number. For reefer containers please share the required temperature. Availability depends on the shipping line and route."),
    ("Can you arrange cargo insurance?", "Yes, marine cargo insurance can be arranged through our partners. Just mention it in your enquiry."),
]

# ---------------------------------------------------------------- pages
def build():
    built = []

    # ---------- Home
    home = hero_style("hero-ship") + f"""
<section class="hero hero-hero-ship">
  <div class="container">
    <span class="eyebrow">Container shipping from Dubai since {BIZ["since"]}</span>
    <h1>Container shipping from the UAE to <em>Africa, Europe</em> &amp; worldwide</h1>
    <p class="lead">Competitive FCL &amp; LCL rates from Jebel Ali. Send your shipment details and get a clear, itemised quote — fast.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="#quote">Get a free quote</a>
      <a class="btn btn-outline" data-wa href="#">Chat on WhatsApp</a>
    </div>
    <ul class="hero-points"><li>20ft, 40ft, High Cube &amp; Reefer</li><li>Rates from multiple shipping lines</li><li>One point of contact, start to finish</li></ul>
  </div>
</section>

<section class="stats">
  <div class="container">
    <div class="stat"><strong>Since {BIZ["since"]}</strong><span>In the shipping business</span></div>
    <div class="stat"><strong>FCL &amp; LCL</strong><span>Full &amp; shared containers</span></div>
    <div class="stat"><strong>Africa · Europe</strong><span>Plus worldwide on request</span></div>
    <div class="stat"><strong>Fast quotes</strong><span>Usually within hours</span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">What we do</span>
      <h2>Ocean freight, handled end to end</h2>
      <p class="lead">From booking the container to delivering it at destination — we compare carriers, handle the paperwork and keep you updated.</p>
    </div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{icon("container")}</div><h3>FCL — Full Container Load</h3><p>20ft, 40ft and 40ft High Cube containers for your cargo only. Best for larger shipments.</p></div>
      <div class="card reveal"><div class="icon">{icon("boxes")}</div><h3>LCL — Shared Container</h3><p>Ship smaller volumes and pay only for the space you use. Ideal for traders and first orders.</p></div>
      <div class="card reveal"><div class="icon">{icon("snow")}</div><h3>Reefer &amp; Special Equipment</h3><p>Temperature-controlled, open top and flat rack containers for special cargo.</p></div>
      <div class="card reveal"><div class="icon">{icon("doc")}</div><h3>Documentation</h3><p>Bills of lading, certificates of origin and guidance on destination requirements.</p></div>
      <div class="card reveal"><div class="icon">{icon("truck")}</div><h3>Pickup &amp; Delivery</h3><p>Trucking from your warehouse in the UAE and door delivery at destination through partners.</p></div>
      <div class="card reveal"><div class="icon">{icon("shield")}</div><h3>Cargo Insurance</h3><p>Marine cargo insurance arranged on request for extra peace of mind.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Popular routes</span>
      <h2>Where we ship from Jebel Ali</h2>
      <p class="lead">Regular container sailings to key ports across Africa and Europe. Indicative port-to-port transit times shown.</p>
    </div>
    {routes_grid()}
    <p class="note">Transit times are indicative and vary by shipping line and routing. Don't see your port? <a href="#quote">Ask us</a> — we quote worldwide.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">How it works</span>
      <h2>From enquiry to delivery in 4 steps</h2>
    </div>
    <div class="grid grid-4 steps">
      <div class="step reveal"><h3>Send your details</h3><p>Fill the quote form or message us on WhatsApp with your shipment details.</p></div>
      <div class="step reveal"><h3>Get your quote</h3><p>We compare rates across shipping lines and send an itemised quote.</p></div>
      <div class="step reveal"><h3>Book &amp; load</h3><p>Confirm the quote. We book the space, arrange the container and handle the paperwork.</p></div>
      <div class="step reveal"><h3>Track to arrival</h3><p>We keep you updated until your container arrives at destination.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Why POC Shipping</span>
      <h2>Your point of contact in global shipping</h2>
    </div>
    <div class="grid grid-4">
      <div class="card reveal"><div class="icon">{icon("tag")}</div><h3>Competitive rates</h3><p>We work with multiple shipping lines to find you the best price for your route.</p></div>
      <div class="card reveal"><div class="icon">{icon("clock")}</div><h3>Quick response</h3><p>Clear quotes, usually within hours — not days.</p></div>
      <div class="card reveal"><div class="icon">{icon("user")}</div><h3>One contact</h3><p>A real person who knows your shipment, from booking to arrival.</p></div>
      <div class="card reveal"><div class="icon">{icon("shield")}</div><h3>Since {BIZ["since"]}</h3><p>Over a decade of experience in shipping from the UAE.</p></div>
    </div>
  </div>
</section>
""" + quote_section() + f"""
<section class="section">
  <div class="container" style="max-width:820px">
    <div class="section-head center reveal"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
    <div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQS[:4])}</div>
    <p style="text-align:center;margin-top:20px"><a href="{{{{B}}}}faq.html">See all questions →</a></p>
  </div>
</section>
"""
    built.append(page("index.html", "Container Shipping from UAE to Africa & Europe | POC Shipping Dubai",
                      "FCL & LCL container shipping from Jebel Ali, Dubai to Africa, Europe and worldwide. Competitive rates from multiple shipping lines — get a fast, itemised quote.",
                      home, "index.html", hero_img="hero-ship"))

    # ---------- Services
    def svc(id_, ic, title, text, points):
        lis = "".join(f"<li>{p}</li>" for p in points)
        return f'<div class="card reveal" id="{id_}"><div class="icon">{icon(ic)}</div><h3>{title}</h3><p>{text}</p><ul style="color:var(--muted);padding-left:1.1rem;margin:12px 0 0">{lis}</ul></div>'
    ctypes = [
        ("20ft", "Standard", "~33 CBM", "Up to ~25–28 t*", "Heavy cargo: tiles, steel, machinery"),
        ("40ft", "Standard", "~67 CBM", "Up to ~26–28 t*", "General cargo, furniture, appliances"),
        ("40ft HC", "High Cube", "~76 CBM", "Up to ~26–28 t*", "Light, bulky cargo needing extra height"),
        ("Reefer", "20ft / 40ft", "Temperature controlled", "Varies", "Food, pharma, perishables"),
    ]
    ct_html = "".join(f'<div class="card ctype reveal"><div class="size">{s}</div><div style="color:var(--muted)">{t}</div><dl><dt>Capacity</dt><dd>{c}</dd><dt>Payload</dt><dd>{w}</dd><dt>Best for</dt><dd>{u}</dd></dl></div>' for s, t, c, w, u in ctypes)
    services = hero_style("port-sunset") + f"""
<section class="hero page-hero hero-port-sunset">
  <div class="container">
    <span class="eyebrow">Services</span>
    <h1>Container freight services</h1>
    <p class="lead">Everything you need to move containers from the UAE — booked, documented and tracked by one team.</p>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2">
    {svc("fcl", "container", "FCL — Full Container Load", "Book a full 20ft, 40ft or 40ft High Cube container for your cargo only.", ["Rates compared across multiple shipping lines", "Weekly sailings from Jebel Ali to major ports", "Port-to-port or door-to-door"])}
    {svc("lcl", "boxes", "LCL — Less than Container Load", "Share container space and pay by volume (CBM). Ideal for smaller or trial shipments.", ["Pay only for the space you use", "Consolidation in the UAE", "Usually cheaper below ~13–15 CBM"])}
    {svc("reefer", "snow", "Reefer & special equipment", "Temperature-controlled reefers, open top and flat rack containers for cargo that doesn't fit the standard box.", ["Reefer: share required temperature", "Open top / flat rack for oversized cargo", "Hazardous (DG) cargo on request with MSDS"])}
    {svc("docs", "doc", "Documentation & compliance", "We arrange the bill of lading and help you prepare the right paperwork for your destination.", ["Bill of lading and shipping instructions", "Certificate of origin", "Guidance on PVoC, SONCAP and other destination rules"])}
    {svc("haulage", "truck", "Pickup & door delivery", "Container trucking from your warehouse or supplier in the UAE, and delivery at destination through our partners.", ["Pickup across the UAE", "Destination delivery on request", "Loading supervision on request"])}
    {svc("insurance", "shield", "Cargo insurance", "Protect your shipment against loss or damage with marine cargo insurance arranged through partners.", ["Quoted with your freight", "Based on cargo value", "Recommended for high-value goods"])}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Container guide</span><h2>Which container do I need?</h2><p class="lead">A quick guide. Not sure? Choose "Not sure" on the quote form and we'll recommend the right option.</p></div>
    <div class="grid grid-4">{ct_html}</div>
    <p class="note">*Approximate figures. Maximum payload depends on the shipping line, the container and road weight limits at origin and destination.</p>
  </div>
</section>
""" + quote_section()
    built.append(page("services.html", "FCL, LCL & Reefer Container Shipping Services | POC Shipping Dubai",
                      "FCL, LCL, reefer and special-equipment container shipping from Jebel Ali, Dubai, with documentation, pickup, delivery and cargo insurance.",
                      services, "services.html", hero_img="port-sunset"))

    # ---------- Routes hub
    routes = hero_style("hero-ship") + f"""
<section class="hero page-hero hero-hero-ship">
  <div class="container">
    <span class="eyebrow">Routes</span>
    <h1>Container shipping routes from Jebel Ali</h1>
    <p class="lead">We focus on Africa and Europe, and quote worldwide on request.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    {routes_grid()}
    <p class="note">Transit times are indicative port-to-port estimates and depend on the shipping line and routing (for example Suez or Cape of Good Hope for Europe). We confirm the transit time with every quote.</p>
  </div>
</section>
""" + cta_band("Shipping to a port not listed here?", "We quote worldwide — including India, the GCC, Asia and the Americas.")
    built.append(page("routes.html", "Container Shipping Routes from Jebel Ali to Africa & Europe | POC Shipping",
                      "Container shipping routes from Jebel Ali, Dubai to Mombasa, Dar es Salaam, Djibouti, Lagos, Tema, Durban, Rotterdam, Hamburg and more.",
                      routes, "routes.html", hero_img="hero-ship"))

    # ---------- Route pages
    for r in ROUTES:
        port_short = r["port"].split(" (")[0]
        dest = f"{port_short}, {r['country']}"
        others = [o for o in ROUTES if o["slug"] != r["slug"]][:4]
        body = hero_style("hero-ship") + f"""
<section class="hero page-hero hero-hero-ship">
  <div class="container">
    <div class="breadcrumb"><a href="{{{{B}}}}index.html">Home</a> / <a href="{{{{B}}}}routes.html">Routes</a> / {port_short}</div>
    <h1>Container shipping from Dubai (Jebel Ali) to {port_short}, {r["country"]}</h1>
    <p class="lead">FCL and LCL shipping to {r["port"]} with competitive rates from multiple shipping lines.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="#quote">Get a quote to {port_short}</a><a class="btn btn-outline" data-wa="Hi POC Shipping, I need a container quote from Jebel Ali to {escape(dest)}." href="#">WhatsApp us</a></div>
    <div class="facts">
      <div class="fact"><span>From</span><strong>Jebel Ali, UAE</strong></div>
      <div class="fact"><span>To</span><strong>{r["port"]}</strong></div>
      <div class="fact"><span>Transit (approx.)</span><strong>{r["transit"]}</strong></div>
      <div class="fact"><span>Options</span><strong>FCL · LCL · Reefer</strong></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2" style="align-items:start">
    <div class="prose reveal">
      <h2>Shipping to {r["country"]}</h2>
      <p>{port_short} is a key gateway for {r["gateway"]}. We ship 20ft, 40ft and 40ft High Cube containers, as well as shared LCL cargo, from Jebel Ali and other UAE ports.</p>
      <h3>Cargo we commonly ship on this route</h3>
      <ul>{"".join(f"<li>{c}</li>" for c in r["cargo"])}</ul>
      <p class="note">Transit time is an indicative port-to-port estimate. We confirm the sailing schedule and transit time with your quote.</p>
    </div>
    <div class="card reveal">
      <div class="icon">{icon("doc")}</div>
      <h3>Documents usually needed</h3>
      <ul style="color:var(--muted);padding-left:1.1rem">{"".join(f"<li>{d}</li>" for d in r["docs"])}</ul>
      <p style="margin-top:12px">Requirements depend on your cargo and can change. We'll confirm what applies when we quote, and your importer or clearing agent should confirm destination requirements.</p>
    </div>
  </div>
</section>
""" + quote_section(dest, heading=f"Get a quote: Jebel Ali → {port_short}") + f"""
<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><h2>Other popular routes</h2></div>
    <div class="grid grid-4">{"".join(f'<a class="card reveal" style="text-decoration:none" href="{{{{B}}}}routes/{o["slug"]}.html"><h3>Jebel Ali → {o["port"].split(" (")[0]}</h3><p>{o["country"]} · ~{o["transit"]}</p></a>' for o in others)}</div>
  </div>
</section>"""
        built.append(page(f"routes/{r['slug']}.html",
                          f"Container Shipping Dubai to {port_short}, {r['country']} | FCL & LCL | POC Shipping",
                          f"Container shipping from Jebel Ali, Dubai to {r['port']}, {r['country']}. FCL & LCL, approx. {r['transit']} transit. Get a competitive, itemised quote.",
                          body, "routes.html", hero_img="hero-ship"))

    # ---------- Quote page
    quote = quote_section(heading="Request a container shipping quote")
    built.append(page("quote.html", "Get a Container Shipping Quote | POC Shipping Dubai",
                      "Request a free FCL or LCL container shipping quote from Jebel Ali, Dubai to Africa, Europe and worldwide.",
                      quote, ""))

    # ---------- About
    about = hero_style("port-sunset") + f"""
<section class="hero page-hero hero-port-sunset">
  <div class="container">
    <span class="eyebrow">About us</span>
    <h1>Your point of contact in global shipping</h1>
    <p class="lead">POC Shipping helps traders and businesses move containers from the UAE — at competitive rates, with one person looking after every shipment.</p>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2" style="align-items:center">
    <div class="prose reveal">
      <h2>Since {BIZ["since"]}</h2>
      <p>POC Shipping was founded in Dubai in {BIZ["since"]} with a simple idea: make international shipping clear, affordable and personal. "POC" stands for <strong>Point of Contact</strong> — one person who knows your shipment from the first quote to final delivery.</p>
      <p>Today we focus on container shipping (FCL and LCL) from Jebel Ali to Africa, Europe and other destinations worldwide. By working with multiple shipping lines and trusted partners at origin and destination, we can compare options and offer competitive rates on every route.</p>
      <p>Our team works from Dubai with support from India, so enquiries get answered quickly.</p>
    </div>
    <img class="reveal" src="{{{{B}}}}assets/img/port-sunset-960.webp" alt="Container port at sunset" width="960" height="633" loading="lazy" style="border-radius:var(--radius);box-shadow:var(--shadow)">
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="section-head center reveal"><h2>What we stand for</h2></div>
    <div class="grid grid-4">
      <div class="card reveal"><div class="icon">{icon("tag")}</div><h3>Transparent pricing</h3><p>Itemised quotes, no hidden charges.</p></div>
      <div class="card reveal"><div class="icon">{icon("clock")}</div><h3>Speed</h3><p>Fast quotes and quick answers.</p></div>
      <div class="card reveal"><div class="icon">{icon("user")}</div><h3>Personal service</h3><p>One point of contact for every shipment.</p></div>
      <div class="card reveal"><div class="icon">{icon("globe")}</div><h3>Global network</h3><p>Shipping lines and partners worldwide.</p></div>
    </div>
  </div>
</section>
""" + cta_band()
    built.append(page("about.html", "About POC Shipping | Container Freight from Dubai since 2012",
                      "POC Shipping is a Dubai-based container freight company, in business since 2012, offering FCL & LCL shipping from the UAE to Africa, Europe and worldwide.",
                      about, "about.html", hero_img="port-sunset"))

    # ---------- FAQ
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    faq = f"""
<section class="hero page-hero" style="background:var(--navy)">
  <div class="container"><span class="eyebrow">FAQ</span><h1>Frequently asked questions</h1><p class="lead">Everything you need to know about shipping containers with us.</p></div>
</section>
<section class="section">
  <div class="container faq" style="max-width:820px">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQS)}</div>
</section>
""" + cta_band("Still have a question?", "Message us on WhatsApp or send your shipment details for a quote.")
    built.append(page("faq.html", "Container Shipping FAQ | POC Shipping Dubai",
                      "Answers about FCL vs LCL, quotes, transit times, documents and hazardous or reefer cargo when shipping containers from the UAE.",
                      faq, "faq.html", extra_schema=[faq_schema]))

    # ---------- Contact
    contact = f"""
<section class="hero page-hero" style="background:var(--navy)">
  <div class="container"><span class="eyebrow">Contact</span><h1>Talk to us</h1><p class="lead">For a quote, use the form below. For anything else, reach us on WhatsApp or email.</p></div>
</section>
<section class="section">
  <div class="container grid grid-2" style="align-items:start">
    <div class="card reveal">
      <ul class="contact-list">
        <li><span class="icon" style="margin:0">{icon("chat")}</span><div><strong>WhatsApp</strong><a data-wa href="#">{BIZ["wa_display"]}</a></div></li>
        <li><span class="icon" style="margin:0">{icon("mail")}</span><div><strong>Email</strong><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></div></li>
        <li><span class="icon" style="margin:0">{icon("pin")}</span><div><strong>Office</strong>{BIZ["address"]}</div></li>
        <li><span class="icon" style="margin:0">{icon("clock")}</span><div><strong>Working hours</strong>Mon–Sat, 9:00–18:00 (UAE time)</div></li>
      </ul>
    </div>
    <div class="reveal">
      <a class="btn btn-whatsapp btn-block" data-wa href="#" style="margin-bottom:12px">Chat on WhatsApp</a>
      <a class="btn btn-ghost btn-block" href="mailto:{BIZ["email"]}">Send an email</a>
    </div>
  </div>
</section>
""" + quote_section()
    built.append(page("contact.html", "Contact POC Shipping | Container Shipping Dubai",
                      "Contact POC Shipping in Dubai for FCL & LCL container shipping quotes. WhatsApp, email or use our quote form.",
                      contact, "contact.html"))

    # ---------- 404
    nf = """<section class="section"><div class="container" style="text-align:center;max-width:640px"><h1>Page not found</h1><p class="lead" style="margin:0 auto 24px">The page you're looking for has moved. Try the homepage or request a quote.</p><a class="btn btn-primary" href="/quote.html">Get a quote</a> <a class="btn btn-ghost" href="/">Home</a></div></section>"""
    page("404.html", "Page not found | POC Shipping", "Page not found.", nf, base="/")

    # ---------- sitemap + robots
    urls = "".join(f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc></url>" for p in built)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("Built:", len(built) + 1, "pages")


if __name__ == "__main__":
    build()
