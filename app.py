from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# === YOUR APP CONFIGURATION ===
CLIENT_ID = '35111166170'
CLIENT_SECRET = '27256412654709c1ffc1db3953ad87da'
REDIRECT_URI = 'https://facbook-auth-2d80156279a4.herokuapp.com/oauth/callback'

@app.route('/')
def home():
    # Facebook Login URL for Instagram Graph API
    auth_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth?"
        f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&"
        f"scope=instagram_basic,pages_show_list,pages_read_engagement&response_type=code"
    )
    return f'<h2>Login with Instagram</h2><a href="{auth_url}">Login</a>'

@app.route('/oauth/callback')
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code provided."

    token_url = 'https://graph.facebook.com/v19.0/oauth/access_token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    response = requests.get(token_url, params=params)
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        return f"<h3>Access Token:</h3><p>{access_token}</p>"
    else:
        return f"<h3>Error getting token:</h3><pre>{data}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
