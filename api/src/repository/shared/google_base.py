import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from dotenv import load_dotenv

load_dotenv()

class GoogleBase():
  
  def get_cred(self, user):
    creds = Credentials(
      token=user.access_token,
      refresh_token=user.refresh_token,
      token_uri="https://oauth2.googleapis.com/token",
      client_id=os.getenv("GOOGLE_CLIENT_ID"),
      client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )
    return creds