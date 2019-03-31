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
    base_url = 'https://gbfs.urbansharing.com/oslobysykkel.no'

    def __init__(self):
        try:
            with open('client-identifier.txt', 'r') as client_id_file:
                client_id = client_id_file.read().strip()
        except OSError as e:
            raise OSError('Could not open client ID file: ' + str(e))

        self.headers = {'Client-Identifier': client_id}

    def _get_json(self, location):
        """Obtain the JSON data of GET on base_url + location as a dictionary.
        Raises PysykkelHTTPError if the HTTP request fails,
        Raises PysykkelJSONError if the JSON data could not be decoded"""
        try:
            data = requests.get(self.base_url + location, headers=self.headers)
            data.raise_for_status()
            return data.json()
        except ValueError:
            raise PysykkelJSONError('Received invalid JSON from Bysykkel API while trying to fetch ' + location)
        except requests.exceptions.HTTPError as e:
            raise PysykkelHTTPError('Got HTTP error while requesting from Bysykkel API (' + location + '): ' + str(e))

    @property
    def stations(self):
        """Return a list of all stations in the system, including availability data"""
        station_data = self._get_json('/station_information.json')['data']['stations']
        availability_data = self._get_json('/station_status.json')['data']['stations']

        # Munge the dict into a list of (id, availability_dict) tuples
        availability_list = [(a['station_id'], a) for a in availability_data]

        # Merge availability and station data. If availability data for a given station
        # is not accessible, it will simply be omitted
        for station in station_data:
            station['availability'] = [item for item in availability_list if item[0] == station['station_id']][0][1]

        return station_data

    @property
    def status(self):
        """ Return a dict with a list of closed stations, and a boolean value
        saying whether all stations are closed."""
        a = requests.get(self.base_url + '/status', headers=self.headers).json()
        return a['status']

    @property
    def all_stations_closed(self):
        return self.status['all_stations_closed']
