# pysykkel

![Screenshot](/screenshot.png)

## Installation

Although the underlying library that fetches from the API is completely portable, the proof of concept display code is designed to run on Python3 in a Linux or Unix environment (because it requires curses and an ANSI terminal).

### Using pip

On a Debian/Ubuntu machine, run

```
apt-get install python3-pip virtualenv
```

To initialize the environment using pip, issue the following commands in the working directory:

```
virtualenv -p python3 env
. env/bin/activate
pip install -r requirements.txt
```

## Usage

The API requests that the Client-Identifier header be supplied, with the organization name, a dash, followed by the application name, eg. 'acme-publicdisplay'.

As shipped the client-identifier is 'pysykkel-development'; if you intend to use this library to generate a lot of requests, please change this for everyone's benefit by passing a more descriptive string to the constructor..

### Terminal dumper
If everything went smoothly, you should now be able to run the test case:

```
./bysykkel-status
```

### REST service

Another example of how the pysykkel library might be useful is this Twisted-based web service which will accept latitude and longitude as GET parameters, and return JSON data on station availability, sorted by distance from your supplied coordinates.

```
./nearest-station-server
```

The server answers on port 8080.

To run unit tests inside the virtualenv, do
```
python -m twisted.trial ./nearest-station-server
```
