from flask import Flask, request
import requests

app = Flask(__name__)

CLIENT_ID = '35111166170'
CLIENT_SECRET = '27256412654709c1ffc1db3953ad87da'
REDIRECT_URI = 'https://facbook-auth-2d80156279a4.herokuapp.com/oauth/callback'

@app.route('/')
def home():
    scope = request.args.get('scope', '')
    auth_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth?"
        f"client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&state=custom_value"
    )
    return f'<h2>Login with Instagram</h2><a href="{auth_url}"><button>Connect with scope: {scope}</button></a>'

@app.route('/oauth/callback')
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code provided."

    print("Received code:", code)

    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    response = requests.get('https://graph.facebook.com/v19.0/oauth/access_token', params=params)
    data = response.json()

    if 'access_token' in data:
        return f"<h3>✅ Access Token:</h3><p>{data['access_token']}</p>"
    else:
        return f"<h3>❌ Error getting token:</h3><pre>{data}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
