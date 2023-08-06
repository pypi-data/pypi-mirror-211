from urllib.parse import urlparse, parse_qs

from .utils import generate_random_token, generate_code_challenge

from .abstract.client import HttpClient
from .abstract.typings import AuthTokenResponse


class Auth:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

        self._req = HttpClient()
        self._code_verifier = generate_random_token()
        self._state = self._get_state()

        self.auth_token = self._auth_token()

    def get_access_token(self) -> str:
        return self.auth_token.access_token

    def get_token_expires(self):
        return self.auth_token.expires_in

    def _get_state(self) -> str:
        url = 'https://auth0.openai.com/authorize'
        params = {
            'client_id': 'pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh',
            'audience': 'https://api.openai.com/v1',
            'redirect_uri': 'com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback',
            'scope': 'openid email profile offline_access model.request model.read organization.read offline',
            'response_type': 'code',
            'code_challenge': f'{generate_code_challenge(self._code_verifier)}',
            'code_challenge_method': 'S256',
            'prompt': 'login'
        }

        response = self._req.get(url, params=params, allow_redirects=True)

        if response.ok:
            response_url_params = parse_qs(urlparse(response.url).query)
            return response_url_params['state'][0]

    def _identifier(self) -> None:
        url = 'https://auth0.openai.com/u/login/identifier'
        params = {'state': self._state}
        json_data = {
            'state': self._state,
            'username': self.email,
            'action': 'default',
            'is-brave': 'false',
            'js-available': 'true',
            'webauthn-available': 'true',
            'webauthn-platform-available': 'false',
        }

        self._req.post(url, json=json_data, params=params,
                       allow_redirects=False)

    def _login_password(self) -> str:
        url = 'https://auth0.openai.com/u/login/password'
        params = {'state': self._state}
        json_data = {
            'state': self._state,
            'username': self.email,
            'password': self.password,
            'action': 'default',
        }

        response = self._req.post(
            url, params=params, json=json_data, allow_redirects=False)

        if response.status_code == 302:
            location = response.headers['Location']

        response = self._req.get(
            f'https://auth0.openai.com{location}', allow_redirects=False)

        if response.status_code == 302:
            return response.headers['Location']

    def _auth_token(self) -> AuthTokenResponse:
        self._identifier()

        location = self._login_password()

        param_code = parse_qs(urlparse(location).query)['code'][0]

        url = 'https://auth0.openai.com/oauth/token'
        json_data = {
            'code': param_code,
            'code_verifier': self._code_verifier,
            'grant_type': 'authorization_code',
            'client_id': 'pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh',
            'redirect_uri': 'com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback'
        }

        response = self._req.post(
            url, json=json_data, allow_redirects=False)

        if response.status_code == 200:
            return AuthTokenResponse(**response.json())
