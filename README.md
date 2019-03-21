# bysykkel
Kodeoppgave for aktuelle utviklere til Oslo Origo / Coding exam for job applicants for Oslo Origo 

## Installation

Although the underlying library is completely portable, the proof of concept code is designed to run on Python3 in a Linux or Unix environment (because it requires curses and an ANSI terminal).

virtualenv and pip are required. On a Debian/Ubuntu machine, run

```
apt-get install python3-pip virtualenv
```

To initialize the environment, issue the following commands in the working directory:

```
virtualenv -p python3 env
. env/bin/activate
pip install -r requirements.txt
```

If everything went smoothly, you should now be able to run the test case:

```
python ./pysykkel_print.py
```
