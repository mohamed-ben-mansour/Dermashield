from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

# Paths to the credentials and token files
CREDENTIALS_FILE = "D:\\final_version\\gl_test\\version_sabaa\\final\\gl_version2.00\client_secret_628026813944-hh157k4s7f0qkglh1pno3f70ur0ouiqt.apps.googleusercontent.com.json"
TOKEN_FILE = 'token.json'

# Scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None

    # Load credentials from the token file if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials are available, prompt the user to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=8000)  # No need to specify `redirect_uri`

        # Save the credentials to the token file
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    print("Authentication successful!")

if __name__ == '__main__':
    main()
