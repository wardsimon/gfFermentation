__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import json
import requests
from .controller import get_device
from . import GRAINFATHER_AUTH_URL, GRAINFATHER_TOKENS_URL, PARTICLE_EVENT_URL


class Grainfather:
    def __init__(self, username=None, password=None, token=None):
        self._auth_token = token
        self._username = username
        self._password = password
        if not token:
            self.authenticate(username, password)
        else:
            self._controllers = self.update_controllers()

    def authenticate(self, username, password):
        self._username = username
        self._password = password
        gf_session = self._authentication(username, password)
        self._auth_token = gf_session['api_token']
        self._controllers = self.update_controllers()

    def update_controllers(self):
        particle_sessions = self._getParticleTokens(self._auth_token)
        controllers = []
        for session in particle_sessions:
            try:
                controllers.append(get_device(session))
            except NameError:
                pass
        return controllers

    @property
    def controllers(self):
        return self._controllers

    @staticmethod
    def _authentication(username, password):
        """
        Authenticate with Grainfather
        """
        data = {
            "email": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(GRAINFATHER_AUTH_URL, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Authentication failed")

    @staticmethod
    def _getParticleTokens(token):
        """
        Get the particle token
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        }
        response = requests.get(GRAINFATHER_TOKENS_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                raise Exception("No particle token found")
            return data
        else:
            raise Exception("Failed to get particle token")

    def reauthenticate(self, conical):
        """
        Reauthenticate with Particle.io
        :param conical: Which device to reauthenticate
        :return:
        """
        try:
            token_session = self._getParticleTokens(self._auth_token)
        except Exception:
            self.authenticate(self._username, self._password)
            token_session = self._getParticleTokens(self._auth_token)
        for token in token_session:
            response = requests.get(PARTICLE_EVENT_URL + "?access_token=" + token).json()
            if response['id'] == conical.id:
                conical._token = token['access_token']

