__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import requests
from .grainfather import PARTICLE_EVENT_URL


class Conical:

    _STATIC = {'name',  'id'}
    _DYNAMIC = {'online', 'status'}
    _PROPS = {
        "temperature": ('temp', float),
        "target":  ('targetTemp', float),
        "heating":  ('heatStatus', bool),
        "cooling":  ('coolStatus',  bool),
    }
    _FUNC = ['setHeat', 'setCool', 'setTarget', 'highActivity', 'dlFirmware', 'startSession', 'manageMode', 'controlFermenting', 'settingControl']

    def __init__(self,  token_session):
        self._token = token_session['access_token']
        response = requests.get(PARTICLE_EVENT_URL + "?access_token=" + self._token).json()
        if len(response) == 0:
            raise NameError("Device not found")
        response = response[0]
        for item in self._STATIC:
            self.__dict__[item] = response[item]

    def _build_query(self, prop):
        URL = PARTICLE_EVENT_URL + '/' + self.id + '/' + prop + "?access_token=" + self._token
        response = requests.get(URL).json()
        return response['result']

    def _execute_func(self, func, value):
        URL = PARTICLE_EVENT_URL + '/' + self.id + '/' + func + "?access_token=" + self._token
        response = requests.post(URL, data={'value':value})
        return response.status_code == 200

    @property
    def temperature(self) -> _PROPS["temperature"][1]:
        return self._build_query(self._PROPS["temperature"][0])

    @property
    def target_temperature(self) -> _PROPS["target"][1]:
        return self._build_query(self._PROPS["target"][0])

    @property
    def heating(self) -> _PROPS["heating"][1]:
        return self._build_query(self._PROPS["heating"][0])

    @property
    def cooling(self) -> _PROPS["cooling"][1]:
        return self._build_query(self._PROPS["cooling"][0])

    def set_temperature(self, temp: int) -> bool:
        return self._execute_func('setTarget', int(temp))

    def control_fermenting(self, value) -> bool:
        return self._execute_func('controlFermenting', int(value))
