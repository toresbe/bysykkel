try:
    import requests
except ImportError:
    print('Pysykkel depends on requests. Try "pip install --user requests"?')
    raise

class PysykkelHTTPError(Exception):
    pass

class PysykkelJSONError(Exception):
    pass

class Pysykkel:
    base_url = 'https://oslobysykkel.no/api/v1'

    def __init__(self):
        try:
            with open('api-key.txt', 'r') as api_key_file:
                api_key = api_key_file.read().strip()
                assert len(api_key) == 32
        except OSError as e:
            raise OSError('Could not open API key file: ' + str(e))
        except AssertionError:
            print('Unexpected length of API key, expected 32 bytes')

        self.headers = {'Client-Identifier': api_key}

    ### Obtain the JSON data of GET on base_url + location as a dictionary.
    ### Raises PysykkelHTTPError if the HTTP request fails,
    ### Raises PysykkelJSONError if the JSON data could not be decoded
    def _get_json(self, location):
        try:
            data = requests.get(self.base_url + location, headers=self.headers)
            data.raise_for_status()
            return data.json()
        except ValueError:
            raise PysykkelJSONError('Received invalid JSON from Bysykkel API while trying to fetch ' + location)
        except requests.exceptions.HTTPError as e:
            raise PysykkelHTTPError('Got HTTP error while requesting from Bysykkel API (' + location + '): ' + str(e))

    ### Return a list of all stations in the system, including availability data
    @property
    def stations(self):
        station_data = self._get_json('/stations')['stations']
        availability_data = self._get_json('/stations/availability')['stations']

        # Munge the dict into a list of (id, availability_dict) tuples
        availability_list = [(a['id'], a['availability']) for a in availability_data]

        # Merge availability and station data. If availability data for a given station
        # is not accessible, it will simply be omitted
        for station in station_data:
            station['availability'] = [item for item in availability_list if item[0] == station['id']][0][1]

        return station_data

    ### Return a dict with a list of closed stations, and a boolean value
    ### saying whether all stations are closed.
    @property
    def status(self):
        a = requests.get(self.base_url + '/status', headers=self.headers).json()
        return a['status']

    @property
    def all_stations_closed(self):
        return self.status['all_stations_closed']
