import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

#################### Dictionaries containing user data #########################
@pytest.fixture
def user_input():
    user_dict = {
        "email": "lemonred@gmail.com",
        "password": "pinco02831",
        "name_first": "Relain",
        "name_last": "Lemoney"
    }
    return user_dict

@pytest.fixture
def user2_input():
    user_dict = {
        "email": "WICKEDER@yahoo.org",
        "password": "pihello31",
        "name_first": "Relain",
        "name_last": "Lemoney"
    }
    return user_dict

@pytest.fixture
def user3_input():
    user_dict = {
        "email": "RenameLHC@yahoo.org",
        "password": "pidsgwg31",
        "name_first": "Cosmo",
        "name_last": "Kearns"
    }
    return user_dict

@pytest.fixture
def user4_input():
    user_dict = {
        "email": "repeatin-rifle@yahoo.org",
        "password": "123abc!@#",
        "name_first": "Brenden",
        "name_last": "Partridge"
    }
    return user_dict

@pytest.fixture
def invalid_user_input():
    user_dict = {
        "email": "blurose@gmail.com",
        "password": "kos",
        "name_first": "Ian",
        "name_last": "Sebastian"
    }
    return user_dict

@pytest.fixture
def channel_input():
    channel_dict = {
        "name":  "channelname",
        "is_public":  True,
    }
    return channel_dict

@pytest.fixture
def channel_input1():
    channel_dict = {
        "name":  "channelname1",
        "is_public":  False,
    }
    return channel_dict

@pytest.fixture
def channel_input2():
    channel_dict = {
        "name":  "channelname2",
        "is_public":  True,
    }
    return channel_dict

@pytest.fixture
def channel_input3():
    channel_dict = {
        "name":  "channelname3",
        "is_public":  False,
    }
    return channel_dict
