__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import asyncio
import httpx
from . import PARTICLE_EVENT_URL


class Conical:

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
        self._token = token_session['access_token']
        response = httpx.get(PARTICLE_EVENT_URL + "?access_token=" + self._token).json()
        if len(response) == 0:
            raise NameError("Device not found")
        response = response[0]
        for item in self._STATIC:
            self.__dict__[item] = response[item]

    def _build_url(self, prop):
        URL = PARTICLE_EVENT_URL + '/' + self.id + '/' + prop + "?access_token=" + self._token
        return URL

    async def _execute_query(self, prop):
        URL = self._build_url(prop)
        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
        response = response.json()
        return response['result']

    async def _execute_func(self, func, value):
        URL = self._build_url(func)
        async with httpx.AsyncClient() as client:
            response = await client.post(URL, data={'value': value})
        return response.status_code == 200

    @property
    def temperature(self) -> _PROPS["temperature"][1]:
        return asyncio.run(self._execute_query(self._PROPS["temperature"][0]))

    @property
    def target_temperature(self) -> _PROPS["target"][1]:
        return asyncio.run(self._execute_query(self._PROPS["target"][0]))

    @property
    def heating(self) -> _PROPS["heating"][1]:
        return asyncio.run(self._execute_query(self._PROPS["heating"][0]))

    @property
    def cooling(self) -> _PROPS["cooling"][1]:
        return asyncio.run(self._execute_query(self._PROPS["cooling"][0]))

    def set_temperature(self, temp: int) -> bool:
        return asyncio.run(self._execute_func('setTarget', int(temp)))

    def _control_fermenting(self, value) -> bool:
        return asyncio.run(self._execute_func('controlFermenting', value))

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