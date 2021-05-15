""" Http tests focused on functions in channel.py """
import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import urllib
from data import data

from error import InputError, AccessError
from http_fixtures import url, user_input,user3_input, user4_input
from http_fixtures import channel_input, channel_input1, invalid_user_input

######################## One fail and one success case for each function  #################################
# simple success case for channel_invite
def test_channel_invite_success(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json=channel_input).json()
    input_data = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['u_id']
    }
    r = requests.post(f'{url}channel/invite', json = input_data).json()
    assert r == {}

    # test using channel details
    details = requests.get(f'{url}channel/details', params = input_data).json()

    expected_output = [
                {'u_id': 0, "name_first": 'Relain', "name_last": 'Lemoney', 'profile_img_url': ""},
                {'u_id': 1, 'name_first': 'Brenden', 'name_last': 'Partridge', 'profile_img_url': ""}
    ]
    assert details['all_members'] == expected_output

# simple fail case for channel_invite
def test_channel_invite_fail(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()

    invalid_input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user['u_id']
    }
    r = requests.post(f'{url}channel/invite', json = invalid_input_data)
    assert r.status_code == 400

# simple success case for channel_details
def test_channel_details_success(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()

    input_data = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
    }

    output = requests.get(f'{url}channel/details', params = input_data).json()

    assert output["owner_members"][0]["name_first"] == "Relain"
    assert output["owner_members"][0]["name_last"] == "Lemoney"


# simple fail case for channel_details
def test_channel_details_fail(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()

    invalid_input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }

    output = requests.get(f'{url}channel/details', params = invalid_input_data)
    assert output.status_code == 400

# simple success case for channel_leave
def test_channel_leave_success(url, user_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()

    input_data = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
    }

    requests.post(f'{url}channel/leave', json = input_data).json()
    # last user leaves so errors when calling channel details cause the
    # channel dont exist no more
    r = requests.get(f'{url}channel/details', params = input_data)
    assert r.status_code == 400

# simple fail case for channel_leave
def test_channel_leave_fail(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()

    invalid_input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }

    r = requests.post(f'{url}channel/leave', json = invalid_input_data)
    assert r.status_code == 400

# simple success case for channel_join
def test_channel_join_success(url, user_input, channel_input, user4_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data).json()
    assert r == {}

    details = requests.get(f'{url}channel/details', params = input_data).json()
    assert details['name'] == "channelname"
    assert details['owner_members'] == [
        {'u_id': 0, 'name_first': 'Relain', 'name_last': 'Lemoney', 'profile_img_url': ""}
    ]
    assert details['all_members'] == [
        {'u_id': 0, 'name_first': 'Relain', 'name_last': 'Lemoney', 'profile_img_url': ""},
        {'u_id': 1, 'name_first': 'Brenden', 'name_last': 'Partridge', 'profile_img_url': ""}
    ]

# simple fail case for channel_join
def test_channel_join_fail(url, user_input, user4_input, channel_input1, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input1.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input1).json()
    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data)
    assert r.status_code == 400

# simple success case for channel_addowner
def test_channel_addowner_success(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data).json()
    input_data2 = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['u_id']
    }
    r = requests.post(f'{url}channel/addowner', json = input_data2).json()
    assert r == {}
    details = requests.get(f'{url}channel/details', params = input_data).json()

    assert details['owner_members'] == [
        {'u_id': 0, 'name_first': 'Relain', 'name_last': 'Lemoney', 'profile_img_url': ""},
        {'u_id': 1, 'name_first': 'Brenden', 'name_last': 'Partridge', 'profile_img_url': ""}
    ]

# simple fail case for channel_addowner
def test_channel_addowner_fail(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data).json()
    input_data2 = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user['u_id']
    }
    r = requests.post(f'{url}channel/addowner', json = input_data2)
    assert r.status_code == 400

# simple success case for channel_removeowner
def test_channel_removeowner_success(url, user_input, user4_input, user3_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()
    user2 = requests.post(f'{url}auth/register', json = user3_input).json()
    # fix this

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data).json()

    input_data2 = {
        "token": user2['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data2).json()

    input_data3 = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['u_id']
    }
    requests.post(f'{url}channel/addowner', json = input_data3).json()

    input_data4 = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user2['u_id']
    }
    requests.post(f'{url}channel/addowner', json = input_data4).json()

    input_data5 = {
        "token": user2['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['u_id']
    }
    r = requests.post(f'{url}channel/removeowner', json = input_data5).json()
    assert r == {}
    details = requests.get(f'{url}channel/details', params = input_data2).json()

    assert details['owner_members'] == [
        {"u_id": 0, "name_first": "Relain", "name_last": "Lemoney", 'profile_img_url': ""},
        {"u_id": 2, "name_first": "Cosmo", "name_last": "Kearns", 'profile_img_url': ""}
        ]

# simple fail case for channel_removeowner
def test_channel_removeowner_fail(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data).json()
    input_data2 = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['u_id']
    }
    r = requests.post(f'{url}channel/removeowner', json = input_data2)
    assert r.status_code == 400

# simple success case for channel_messages
def test_channel_messages_success(url, user_input, channel_input, channel_input1):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()

    channel_input1.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input1).json()

    input_data = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "start": 0
    }

    message = requests.get(f'{url}channel/messages', params = input_data).json()

    assert message == { "messages": [],
                        "start": 0,
                        "end": -1
                      }

# simple fail case for channel_messages(token, channel_id, start)
def test_channel_messages_fail(url, user_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()

    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "start": 0
    }

    r = requests.get(f'{url}channel/messages', params = input_data)
    assert r.status_code == 400

######################## One large test for channel file #################################
def test_channel_full(url, user_input, user3_input, user4_input, channel_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user1 = requests.post(f'{url}auth/register', json = user4_input).json()
    user2 = requests.post(f'{url}auth/register', json = user3_input).json()

    channel_input.update({"token": user['token']})
    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    input_data = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/join', json = input_data).json()
    input_data2 = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['u_id']
    }
    requests.post(f'{url}channel/addowner', json = input_data2).json()

    input_data3 = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user2['u_id']
    }
    r = requests.post(f'{url}channel/invite', json = input_data3).json()
    assert r == {}

    input_data4 = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['u_id']
    }
    r = requests.post(f'{url}channel/removeowner', json = input_data4)

    input_data5 = {
        "token": user2['token'],
        "channel_id": channel['channel_id'],
    }
    r = requests.post(f'{url}channel/leave', json = input_data)

    input_data6 = {
        "token": user['token'],
        "channel_id": channel['channel_id'],
        "start": 0
    }
    message = requests.get(f'{url}channel/messages', params = input_data6).json()

    assert message == { "messages": [],
                        "start": 0,
                        "end": -1
                      }

    details = requests.get(f'{url}channel/details', params = input_data5).json()
    assert details['owner_members'] == [
        {"u_id": 0, "name_first": "Relain", "name_last": "Lemoney", 'profile_img_url': ""}
        ]

    assert details['all_members'] == [
        {"u_id": 0, "name_first": "Relain", "name_last": "Lemoney", 'profile_img_url': ""},
        {"u_id": 2, "name_first": "Cosmo", "name_last": "Kearns", 'profile_img_url': ""}
        ]
