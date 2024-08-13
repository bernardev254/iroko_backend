import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of your spreadsheet.
SPREADSHEET_ID = "1626eTuIBWLlKEfjqSC_2BLSHMkdXrv_l8_Y7I7ycN4E"
SPREADSHEET_RANGE = "B1:D2"

def get_credentials():
    creds = service_account.Credentials.from_service_account_file(
        "/etc/secrets/credentials.json", scopes=SCOPES
    )
    return creds

def fetch_data():
    creds = get_credentials()
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=SPREADSHEET_RANGE)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            return []
        return values
    except HttpError as err:
        print(err)
        return []

# Create a Flask app
app = Flask(__name__)
@cross_origin(origins='*',methods=['GET','OPTIONS',])
@app.route('/api/properties', methods=['GET'])
def get_properties():
    data = fetch_data()
    print("Data fetched from Google Sheets:", data)  # Add logging to check the response
    headers = data[0]
    rows = data[1:]
    processed_data = []
    for row in rows:
            obj = {headers[i]: row[i] for i in range(len(headers))}
            processed_data.append(obj)
    response = make_response(jsonify(processed_data))
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline';"
    return response
    

if __name__ == '__main__':
    app.run(debug=True)

