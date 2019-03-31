import requests
import time
from twisted.trial import unittest

class PysykkelError(Exception):
    pass

class PysykkelHTTPError(PysykkelError):
    pass

class PysykkelJSONError(PysykkelError):
    pass

class PysykkelTest(unittest.TestCase):
    def test_raises_json_error_on_invalid_json(self):
        p = Pysykkel()
        p.base_url = 'http://google.com/?'
        with self.assertRaises(PysykkelJSONError):
            stations = p.stations

    def test_raises_http_error_on_invalid_url(self):
        p = Pysykkel()
        p.base_url = 'http://this is certainly not a valid url'
        with self.assertRaises(PysykkelHTTPError):
            stations = p.stations

    def test_returns_list_of_dicts(self):
        p = Pysykkel()
        stations = p.stations
        self.assertIsInstance(stations, list)
        for station in stations:
            self.assertIsInstance(station, dict)

    def test_uses_cache(self):
        p = Pysykkel()
        self.assertEquals(p._cache_expired('/station_information.json'), True)
        p._query_api('/station_information.json')
        self.assertEquals(p._cache_expired('/station_information.json'), False)
        p.base_url = '' # this does not invalidate the cache but if the next line
                        # does not halt and catch fire that means it went to 
                        # cache
        p._query_api('/station_information.json')

class Pysykkel:
    base_url = 'https://gbfs.urbansharing.com/oslobysykkel.no'

    def __init__(self, client_id = 'pysykkel-development'):
        """Please supply a client_id if you yourself are planning to use this in any 
        context where you'd be generating a non-trivial amount of traffic."""
        self.headers = {'Client-Identifier': client_id}
        self._ttl = None
        self._resource_caches = {}

    def _get_json(self, location):
        """Obtain the JSON data of GET on base_url + location as a dictionary.
        Raises PysykkelHTTPError if the HTTP request fails,
        Raises PysykkelJSONError if the JSON data could not be decoded"""
        try:
            data = requests.get(self.base_url + location, headers=self.headers)
            data.raise_for_status()
            result = data.json()
            self._resource_caches[location] = result
            return result
        except ValueError:
            raise PysykkelJSONError('Received invalid JSON from Bysykkel API while trying to fetch ' + location)
        except requests.exceptions.RequestException as e:
            raise PysykkelHTTPError('Got HTTP error while requesting from Bysykkel API (' + location + '): ' + str(e))

    def _cache_expired(self, resource):
        """Returns true if the given resource is cached and that cache is not stale 
        (based on TTL value inside the cache)"""
        resource_cache = self._resource_caches.get(resource, None)

        if resource_cache == None:
            return True

        if (resource_cache['ttl'] + resource_cache['last_updated']) > time.time():
            return True
            
        return False

    def _query_api(self, resource):
        """Fetches data from API, or from cache if it is not stale."""
        if self._cache_expired(resource):
            return self._get_json(resource)
        else:
            return self._resource_caches[resource]

    @property
    def stations(self):
        """Return a list of all stations in the system, including availability data"""
        station_data = self._query_api('/station_information.json')['data']['stations']
        availability_data = self._query_api('/station_status.json')['data']['stations']

        # Munge the dict into a list of (id, availability_dict) tuples
        availability_list = [(a['station_id'], a) for a in availability_data]

        # Merge availability and station data. If availability data for a given station
        # is not accessible, it will simply be omitted
        for station in station_data:
            station['availability'] = [item for item in availability_list if item[0] == station['station_id']][0][1]
            del station['availability']['station_id'] # butter on pork, as we say

        return station_data
