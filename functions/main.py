# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_functions.params import StringParam
from firebase_admin import initialize_app
from oura_ring import OuraClient
from datetime import date, timedelta
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

initialize_app()

OURA_PAT = StringParam("OURA_PERSONAL_ACCESS_TOKEN")


@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response(f'OURA_VARIABLE={OURA_PAT.value}')

@https_fn.on_request()
def fetch_oura_data(req: https_fn.Request) -> https_fn.Response:
    oura_client = OuraClient(OURA_PAT.value)

    enddate = date.today()
    startdate = enddate - timedelta(days=7)

    raw_sleep_data = oura_client.get_sleep_periods(start_date=str(startdate), end_date=str(enddate))
    sleep_data = [extract_sleep_fields(data) for data in raw_sleep_data]

    return https_fn.Response(f'{sleep_data}')

TEST_SPREADSHEET_ID = '1KfyNKP6GU0WeAsRwPXewHqRc6iE5SRdhQnjtfzE0rrE'
TEST_RANGE = 'A2:C5'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


@https_fn.on_request()
def write_to_sheets(req: https_fn.Request) -> https_fn.Response:
    creds = ServiceAccountCredentials.from_json_keyfile_name("oura-ring-data-relay-4b853eae714b.json", SCOPES)
    # creds = Credentials.from_authorized_user_info("oura-ring-data-relay-4b853eae714b.json", SCOPES)
    client = build("sheets", "v4", credentials=creds)
    sheets = client.spreadsheets()

    result = (
        sheets.values()
        .get(spreadsheetId=TEST_SPREADSHEET_ID, range=TEST_RANGE)
        .execute()
    )

    values = result.get("values", [])
    return https_fn.Response(f'{values}')


def extract_sleep_fields(sleep_data: dict[str, any]) -> dict[str, any]:
    return {
        'id': sleep_data['id'],
        'day': sleep_data['day'],
        'bedtime_start': sleep_data['bedtime_start'],
        'bedtime_end': sleep_data['bedtime_end'],
        'time_in_bed': sleep_data['time_in_bed'],
        'total_sleep_duration': sleep_data['total_sleep_duration'],
        'rem_sleep_duration': sleep_data['rem_sleep_duration'],
        'deep_sleep_duration': sleep_data['deep_sleep_duration'],
        'light_sleep_duration': sleep_data['light_sleep_duration'],
        'awake_time': sleep_data['awake_time'],
        'efficiency': sleep_data['efficiency'],
    }