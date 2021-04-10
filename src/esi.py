import http.client
import json
from conf.config import esi as esiconf


class esi:
    endpoints = {
        'ids' : { 'uri': '/latest/universe/ids/?datasource=tranquility&language=de', 'type': 'POST' }, 
        'names' : { 'uri': '/latest/universe/names/?datasource=tranquility&language=de', 'type': 'POST' },
        'market' : { 'uri': '/latest/markets/{region}/orders/?datasource=tranquility&language=de&order_type={order_type}&page={page}&type_id={type_id}', 'type': 'GET' },
        'route': { 'uri': '/latest/route/{start}/{end}/?datasource=tranquility&language=de', 'type': 'GET' },
        'region': { 'uri': '/latest/universe/regions/{region}/?datasource=tranquility&language=de', 'type': 'GET' },
        'constellation': { 'uri': '/latest/universe/constellations/{constellation}/?datasource=tranquility&language=de', 'type': 'GET' },
        'system': { 'uri': '/latest/universe/systems/{system}/?datasource=tranquility&language=de', 'type': 'GET' },
    }

    headers = { 'Content-Type' : 'application/json', 'Accept': 'application/json',  'Accept-Language': 'de' }
    connection = None
        

    def request(self, endpoint, param, data=''):
        ep = self.endpoints[endpoint]
        request_string = ep['uri'].format(**param)
        
        self.connection.request(ep['type'], request_string, data, self.headers)

        response = self.connection.getresponse()
        result = response.read().decode()
        return result
    
    def connect(self):
        self.connection = http.client.HTTPSConnection(esiconf.server)

