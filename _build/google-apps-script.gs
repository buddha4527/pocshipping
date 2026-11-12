/**
 * POC Shipping — enquiry receiver (Google Apps Script)
 * Saves each website quote request to this Google Sheet and emails it.
 * Setup steps: see SETUP-ENQUIRIES.md in the repo.
 */

const NOTIFY_EMAIL = 'sales@pocshipping.com';   // where new enquiries are emailed
const SHEET_NAME = 'Enquiries';

const COLUMNS = [
  'submitted_at', 'reference', 'status', 'shipment_type', 'origin', 'destination',
  'container_type', 'container_qty', 'packages', 'volume_cbm', 'weight_kg', 'commodity',
  'hazardous', 'service', 'ready_date', 'name', 'company', 'email', 'phone', 'notes', 'page'
];

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.website) return ok_(); // spam trap

  const sheet = getSheet_();
  p.status = 'New';
  sheet.appendRow(COLUMNS.map(c => p[c] || ''));

  const isLcl = p.shipment_type === 'LCL';
  const cargo = isLcl
    ? `${p.packages || '?'} packages, ${p.volume_cbm || '?'} CBM`
    : `${p.container_qty || '?'} x ${p.container_type || '?'}`;

  const subject = `New quote request ${p.reference}: ${p.origin} → ${p.destination} (${p.shipment_type}, ${cargo})`;
  const body = COLUMNS.filter(c => p[c]).map(c => `${c.replace(/_/g, ' ')}: ${p[c]}`).join('\n');

  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    replyTo: p.email || NOTIFY_EMAIL,
    subject: subject,
    body: body + '\n\nReply to this email to answer the customer directly.'
  });

  return ok_();
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(COLUMNS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
  }
  return sh;
}

function ok_() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
}

/** Run once from the editor to test: creates a sample row and email. */
function testEnquiry() {
  doPost({ parameter: {
    submitted_at: new Date().toISOString(), reference: 'POC-TEST', shipment_type: 'FCL',
    origin: 'Jebel Ali, UAE', destination: 'Mombasa, Kenya', container_type: '40ft High Cube',
    container_qty: '1', commodity: 'Tiles', weight_kg: '24000', name: 'Test Customer',
    email: NOTIFY_EMAIL, phone: '+971000000', page: '/test'
  }});
}
