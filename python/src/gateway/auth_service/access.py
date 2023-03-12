import os, requests
from dotenv import load_dotenv

load_dotenv(".env")

def login(request):
    auth = request.headers.get("Authorization")
    if not auth:
        return None,("missing credentials",401)

    basicAuth = (auth.username,auth.password)
    response = requests.post(
        f"http://{os.environ['AUTH_SVC_ADDRESS']}/login",
        auth = basicAuth
    )  

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
