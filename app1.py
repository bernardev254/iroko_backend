import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify
# Use the credentials to create a client to interact with the Google Drive API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet

sheet = client.open("properties").sheet1

# Fetch all records
def fetch_data():
    data = sheet.get_all_records()
    return data

# Create a Flask app
app = Flask(__name__)

@app.route('/api/properties', methods=['GET'])
def get_properties():
    try:
        data = fetch_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

