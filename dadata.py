import json
import requests


class New:

    def __init__(self, token, secret=None):
        self.token = 'Token ' + str(token)
        if secret:
            self.secret = str(secret)
        self.sp = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/'
        self.cp = 'https://cleaner.dadata.ru/api/v1/clean/'

    def sask(self, fnc):
        fnc['headers']['Content-Type'] = 'application/json'
        fnc['headers']['Accept'] = 'application/json'
        fnc['headers']['Authorization'] = self.token
        return requests.post(fnc['url'], data=json.dumps(fnc['data']), headers=fnc['headers'])

    def suggest(self, query, code, props=None, filts=None):
        body = {
            'url': self.sp + 'suggest/' + str(code),
            'data': {'query': query}
        }
        if isinstance(props, dict):
            for p in props:
                body['data'][p] = props[p]
        if isinstance(filts, dict):
            body['data']['filters'] = [filts]
        return self.sask(body).json()

    def findById(self, query, code, props=None):
        body = {
            'url': self.sp + 'findById/' + str(code),
            'data': {'query': query}
        }
        if isinstance(props, dict):
            for p in props:
                body['data'][p] = props[p]
        return self.sask(body).json()

    def geolocate(self, lat, lon, props=None):
        body = {
            'url': self.sp + 'geolocate/address',
            'data': {'lon': str(lon), 'lat': str(lat)}
        }
        if isinstance(props, dict):
            for p in props:
                body['data'][p] = props[p]
        return self.sask(body).json()

    def findAffiliated(self, query, props=None):
        body = {
            'url': self.sp + 'findAffiliated/party',
            'data': {'query': query}
        }
        if isinstance(props, dict):
            for p in props:
                body['data'][p] = props[p]
        return self.sask(body).json()

    def iplocate(self, query):
        headers = {
            "Authorization": self.token,
            "Accept": "application/json"
        }
        res = requests.get(
            self.sp + 'iplocate/address?ip=' + str(query),
            headers=headers
        )
        return res.json()

    def clean(self, query, code):
        body = {
            'headers': {'X-Secret': self.secret}
        }
        if isinstance(query, list) and isinstance(code, list):
            body['data'] = {
                'structure': code,
                'data': [query]
            }
            body['url'] = self.cp
        else:
            body['url'] = self.cp + str(code)
            body['data'] = [query]
        return self.sask(body).json()
