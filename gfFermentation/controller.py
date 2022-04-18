__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import requests
from . import PARTICLE_EVENT_URL


class GenericController:

    _STATIC = {'name',  'id'}
    _DYNAMIC = {'online', 'status'}
    _PROPS = {
        "temperature": ('temp', float),
        "target":  ('targetTemp', float),
        "heating":  ('heatStatus', bool),
        "cooling":  ('coolStatus',  bool),
    }
    _FUNC = ['setHeat', 'setCool', 'setTarget', 'highActivity', 'dlFirmware',
             'startSession', 'manageMode', 'controlFermenting', 'settingControl']

    def __init__(self,  token_session):
        self._status = None
        self._online = None
        self._token = token_session['access_token']
        self._refresh_token = token_session['refresh_token']
        self._update_vars()

    @property
    def is_online(self) -> bool:
        self._update_vars()
        return self._online

    def _update_vars(self):
        response = requests.get(PARTICLE_EVENT_URL + "?access_token=" + self._token).json()
        if len(response) == 0:
            raise NameError("Device not found")
        response = response[0]
        for item in self._STATIC:
            self.__dict__[item] = response[item]
        for item in self._DYNAMIC:
            setattr(self, "_" + item, response[item])

    def _build_url(self, prop):
        URL = PARTICLE_EVENT_URL + '/' + self.id + '/' + prop + "?access_token=" + self._token
        return URL

    def _execute_query(self, prop):
        if not self.is_online:
            return None
        URL = self._build_url(prop)
        try:
            response = requests.get(URL).json()
        except (requests.ReadTimeout, requests.ConnectTimeout):
            return None
        # response = response.json()
        return response['result']

    def _execute_func(self, func, value):
        if not self.is_online:
            raise TimeoutError(f"Device \"{self.name}\" is not online")
        URL = self._build_url(func)
        response = requests.post(URL, data={'value': value})
        return response.status_code == 200

    @property
    def online(self):
        self._update_vars()
        return self._online

    @property
    def status(self) -> str:
        self._update_vars()
        return self._status

    @property
    def temperature(self) -> _PROPS["temperature"][1]:
        return self._execute_query(self._PROPS["temperature"][0])

    @property
    def target_temperature(self) -> _PROPS["target"][1]:
        return self._execute_query(self._PROPS["target"][0])

    @property
    def heating(self) -> _PROPS["heating"][1]:
        return self._execute_query(self._PROPS["heating"][0])

    @property
    def cooling(self) -> _PROPS["cooling"][1]:
        return self._execute_query(self._PROPS["cooling"][0])

    def set_temperature(self, temp: int) -> bool:
        return self._execute_func('setTarget', int(temp))

    def _control_fermenting(self, value) -> bool:
        return self._execute_func('controlFermenting', value)

    def resume_fermenting(self) -> bool:
        return self._control_fermenting(1)

    def pause_fermenting(self) -> bool:
        return self._control_fermenting(0)

    def set_heat_and_cool(self) -> bool:
        return self._control_fermenting(2)

    def set_heat_only(self) -> bool:
        return self._control_fermenting(3)

    def set_cool_only(self) -> bool:
        return self._control_fermenting(4)

    def __repr__(self):
        s = f"{self.__class__.__name__} \"{self.name}\": "
        if self._online:
            s += f"{self.temperature:.2f}°C, SP - {self.target_temperature:.2f}°C"
            if self.heating:
                s += ", Status -  Heating"
            elif self.cooling:
                s += ", Status - Cooling"
            else:
                s += ", Status - Idle"
        else:
            s += "Status - Offline"
        return s


class Conical(GenericController):
    _product_id: int = 7822


class GCA(GenericController):
    _product_id: int = 8892


IDS = {
    Conical._product_id: Conical,
    GCA._product_id: GCA
}


def get_device(token_session):
    token = token_session["access_token"]
    response = requests.get(PARTICLE_EVENT_URL + "?access_token=" + token).json()
    if len(response) == 0:
        raise NameError("Device not found")
    response = response[0]
    product_id = response['product_id']
    if product_id in IDS:
        return IDS[product_id](token_session)
    else:
        raise NameError("Device not a known controller type")
