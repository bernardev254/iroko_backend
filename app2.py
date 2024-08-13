import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, jsonify

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of your spreadsheet.
SPREADSHEET_ID = "1626eTuIBWLlKEfjqSC_2BLSHMkdXrv_l8_Y7I7ycN4E"
SPREADSHEET_RANGE = "Sheet1!A1:E"

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
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

@app.route('/api/properties', methods=['GET'])
def get_properties():
    data = fetch_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

