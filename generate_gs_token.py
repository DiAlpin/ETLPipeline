import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1US3Wslww8r3HIz56-FXMZFMAVdBG7HH8_vylGaqjtjY"
SAMPLE_RANGE_NAME = "dump!A2"
cwd = os.getcwd()


def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        rf"{cwd}/.credentials.json", SCOPES
        )
    creds = flow.run_local_server(port=3000)

    with open(rf"{cwd}/.token.json", "w") as token:
        token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        value_data = [['plm'], ['plm332'], ['plm3']]

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                valueInputOption="USER_ENTERED", body={'values': value_data}
                )
            .execute()
        )

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
