import json
import requests


class DaData:

    def __init__(self, token, secret=None):
        self.token = 'Token ' + str(token)
        if secret:
            self.secret = str(secret)

    def ask(self, uri, data):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token
        }
        return requests.post(uri, data=json.dumps(data), headers=headers)

    def suggest(self, query, code, count=10):
        data = {
            'query': query,
            'count': count
        }
        return self.ask('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/' + str(code), data).json()

    def findById(self, query, code):
        data = {
            "query": query
        }
        return self.ask('https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/' + str(code), data).json()

    def geolocate(self, lat, lon, count=10, rad=100, lang='ru'):
        data = {
            'lon': str(lon),
            'lat': str(lat),
            'count': count,
            'radius_meters': str(rad),
            'language': str(lang)
        }
        return self.ask('https://suggestions.dadata.ru/suggestions/api/4_1/rs/geolocate/address', data).json()

    def findAffiliated(self, query, count=10):
        data = {
            'query': str(query),
            'count': str(count)
        }
        return self.ask('https://suggestions.dadata.ru/suggestions/api/4_1/rs/findAffiliated/party', data).json()

    def iplocate(self, query):
        headers = {
            "Authorization": self.token,
            "Accept": "application/json"
        }
        res = requests.get(
            'https://suggestions.dadata.ru/suggestions/api/4_1/rs/iplocate/address?ip=' + str(query),
            headers=headers
        )
        return res.json()

    def clean(self, query, code):
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "X-Secret": self.secret
        }
        res = requests.post(
            'https://cleaner.dadata.ru/api/v1/clean/' + str(code),
            data=json.dumps([query]),
            headers=headers
        )
        return res.json()
