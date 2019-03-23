# bysykkel

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

Place the API key in a text file called api-key.txt in your working directory.

If everything went smoothly, you should now be able to run the test case:

```
./bysykkel-status
```
