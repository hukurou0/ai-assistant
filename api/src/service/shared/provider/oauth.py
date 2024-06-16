from pydantic import BaseModel

import requests

class OAuthProvider(BaseModel):
  async def fetch_userinfo(self, access_token:str) -> dict:
    response = requests.get(
    'https://www.googleapis.com/oauth2/v1/userinfo',
    params={'alt': 'json', 'access_token': access_token}
    )
    return response.json()