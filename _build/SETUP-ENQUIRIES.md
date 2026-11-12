# Saving website enquiries to Google Sheets + email

Until this is set up, the quote form sends enquiries **by WhatsApp** (to +91 94007 76671).
After setup, every enquiry is **saved in a Google Sheet** and **emailed to sales@pocshipping.com**. The customer still gets a button to send it on WhatsApp too.

Setup takes about 10 minutes and is free.

## 1. Create the Sheet
1. Go to <https://sheets.new> (signed in to the Google account that should own the enquiries).
2. Name it **POC Shipping – Enquiries**.

## 2. Add the script
1. In the Sheet: **Extensions → Apps Script**.
2. Delete what's there and paste everything from `google-apps-script.gs` (in this `_build` folder).
3. If enquiries should go to a different email, change `NOTIFY_EMAIL` at the top.
4. Click **Save**.
5. Choose `testEnquiry` in the function dropdown and click **Run**. Approve the permissions when asked.
   Check that an **Enquiries** tab with a test row appeared and that a test email arrived.

## 3. Publish it as a web app
1. **Deploy → New deployment** → gear icon → **Web app**.
2. *Execute as:* **Me**. *Who has access:* **Anyone**.
3. Click **Deploy** and copy the **Web app URL** (it ends in `/exec`).

## 4. Connect the website
1. Open `assets/js/script.js`.
2. Paste the URL between the quotes on this line:
   ```js
   const ENQUIRY_ENDPOINT = 'https://script.google.com/macros/s/XXXX/exec';
   ```
3. Commit the change. Submit a test enquiry on the live site and check the Sheet and inbox.

## Using the Sheet
- The `status` column starts as **New**. Change it to *Quoted*, *Won*, *Lost* as you go — this becomes your sales pipeline.
- Later we can add: automatic quote drafts from a rate sheet + margin, and follow-up reminders.

## Changing the WhatsApp number
Edit `WHATSAPP_NUMBER` at the top of `assets/js/script.js` (digits only, with country code).
To change the number shown on pages, edit `BIZ` in `_build/build.py` and run `python3 _build/build.py`.
