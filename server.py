from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import datetime
import logging

# Optional Google Sheets support
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GS_AVAILABLE = True
except Exception:
    GS_AVAILABLE = False

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

CSV_FILE = 'bookings.csv'
GS_CREDENTIALS_FILE = 'gs_credentials.json'  # put service account JSON here
GS_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp','name','phone','email','date','time','guests','notes'])

# Normalize sheet ID from full URL if user set full link
if GS_SHEET_ID and '/d/' in GS_SHEET_ID:
    parts = GS_SHEET_ID.split('/d/')[-1].split('/')
    GS_SHEET_ID = parts[0]
    logging.info('Parsed Google Sheet ID from full URL.')

# Try to initialize Google Sheets client if possible
gs_sheet = None
if GS_AVAILABLE and os.path.exists(GS_CREDENTIALS_FILE) and GS_SHEET_ID:
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
        creds = Credentials.from_service_account_file(GS_CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        gs_sheet = client.open_by_key(GS_SHEET_ID).sheet1
        logging.info('Google Sheets integration enabled.')
    except Exception:
        gs_sheet = None
        logging.exception('Google Sheets init failed')
else:
    if not GS_AVAILABLE:
        logging.info('gspread not installed; Google Sheets disabled.')
    elif not os.path.exists(GS_CREDENTIALS_FILE):
        logging.info('Google credentials not found (%s); Google Sheets disabled.', GS_CREDENTIALS_FILE)
    elif not GS_SHEET_ID:
        logging.info('GOOGLE_SHEET_ID env var not set; Google Sheets disabled.')


@app.route('/bookings', methods=['POST'])
def bookings():
    data = request.get_json() or {}
    ts = datetime.datetime.utcnow().isoformat()
    row = [
        ts,
        data.get('name',''),
        data.get('phone',''),
        data.get('email',''),
        data.get('date',''),
        data.get('time',''),
        data.get('guests',''),
        data.get('notes','')
    ]
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    except Exception as e:
        logging.exception('Failed to write CSV')
        return jsonify({'error': str(e)}), 500

    # Append to Google Sheet if available
    if gs_sheet:
        try:
            gs_sheet.append_row(row, value_input_option='USER_ENTERED')
        except Exception:
            logging.exception('Failed to append row to Google Sheet')

    return jsonify({'status':'ok'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
