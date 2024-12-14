# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_functions.params import StringParam
from firebase_admin import initialize_app

initialize_app()

OURA_API_KEY = StringParam("OURA_API_KEY")


@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response(f'OURA_VARIABLE={OURA_API_KEY.value}')