from flask import Flask, request
import requests

app = Flask(__name__)

REDIRECT_URI = 'https://facbook-auth-2d80156279a4.herokuapp.com/oauth/callback'

@app.route('/')
def home():
    type_ = request.args.get('type', '')
    scope = request.args.get('scope', '')

    if type_ == 'insta':
        client_id = '528499633685543'
    elif type_ == 'fb':
        client_id = '35111166170'
    else:
        return "Error: Invalid type. Use '?type=insta' or '?type=fb'."

    auth_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth?"
        f"client_id={client_id}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&state={type_}"
    )

    return f'<h2>Login with {type_.upper()}</h2><a href="{auth_url}"><button>Connect with scope: {scope}</button></a>'

@app.route('/oauth/callback')
def oauth_callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if not code or not state:
        return "Error: Missing code or state."

    if state == 'insta':
        client_id = '528499633685543'
        client_secret = 'c5a8debd316b5a621602af8010663c96'
    elif state == 'fb':
        client_id = '35111166170'
        client_secret = '27256412654709c1ffc1db3953ad87da'
    else:
        return "Error: Unknown state."

    token_url = 'https://graph.facebook.com/v19.0/oauth/access_token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    response = requests.get(token_url, params=params)
    data = response.json()

    if 'access_token' in data:
        return f"<h3>✅ Access Token:</h3><p>{data['access_token']}</p>"
    else:
        return f"<h3>❌ Error getting token:</h3><pre>{data}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
