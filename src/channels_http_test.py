""" http tests focused on functions in channels.py """
import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import urllib

from error import InputError, AccessError
from http_fixtures import url, user_input, user3_input, user4_input, channel_input
from http_fixtures import channel_input1, channel_input2, channel_input3, invalid_user_input

######################## One fail and one success case for each function  #################################
# simple success case for channels_list
def test_channels_list_success(url, user_input, user3_input, channel_input,
                               channel_input1, channel_input2, channel_input3):
    requests.delete(f'{url}clear')
    user1 = requests.post(f'{url}auth/register', json = user_input).json()
    user2 = requests.post(f'{url}auth/register', json = user3_input).json()

    channel_input.update({"token": user1['token']})
    channel_input1.update({"token": user1['token']})
    channel_input2.update({"token": user1['token']})
    channel_input3.update({"token": user1['token']})

    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    channel1 = requests.post(f'{url}channels/create', json = channel_input1).json()
    channel2 = requests.post(f'{url}channels/create', json = channel_input2).json()
    channel3 = requests.post(f'{url}channels/create', json = channel_input3).json()

    output1 = requests.get(f'{url}channels/list', params={"token": user1['token']}).json()
    output2 = requests.get(f'{url}channels/list', params={"token": user2['token']}).json()

    check_list = [channel['channel_id'] for channel in output1['channels']]
    expected_output =   [channel['channel_id'], channel1['channel_id'],
                         channel2['channel_id'], channel3['channel_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output
    assert output2 == {'channels': []}

# simple fail case for channels_list
def test_channels_list_fail(url, user_input, invalid_user_input, channel_input,
                               channel_input1, channel_input2, channel_input3):
    requests.delete(f'{url}clear')
    user1 = requests.post(f'{url}auth/register', json = user_input).json()
    user2 = requests.post(f'{url}auth/register', json = invalid_user_input).json()

    channel_input.update({"token": user1['token']})
    channel_input1.update({"token": user1['token']})
    channel_input2.update({"token": user1['token']})
    channel_input3.update({"token": user1['token']})

    r = requests.get(f'{url}channels/list', params=user2)
    assert r.status_code == 400

# simple sucess case for channels_listall
def test_channels_listall_success(url, user_input, user3_input, user4_input, channel_input,
                      channel_input1, channel_input2, channel_input3):
    requests.delete(f'{url}clear')
    user1 = requests.post(f'{url}auth/register', json = user_input).json()
    user2 = requests.post(f'{url}auth/register', json = user3_input).json()
    user3 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user1['token']})
    channel_input1.update({"token": user1['token']})
    channel_input2.update({"token": user2['token']})
    channel_input3.update({"token": user2['token']})

    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    channel1 = requests.post(f'{url}channels/create', json = channel_input1).json()
    channel2 = requests.post(f'{url}channels/create', json = channel_input2).json()
    channel3 = requests.post(f'{url}channels/create', json = channel_input3).json()

    input_data1 = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user3['u_id']
    }
    input_data2 = {
        "token": user2['token'],
        "channel_id": channel['channel_id'],
        "u_id": user3['u_id']
    }

    requests.post(f'{url}channel/invite', json = input_data1).json()
    requests.post(f'{url}channel/invite', json = input_data2).json()

    output1 = requests.get(f'{url}channels/listall', params={"token": user1['token']}).json()
    output2 = requests.get(f'{url}channels/listall', params={"token": user2['token']}).json()

    check_list = [channel['channel_id'] for channel in output1['channels']]
    expected_output =   [channel['channel_id'], channel1['channel_id'],
                         channel2['channel_id'], channel3['channel_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output

    check_list = [channel['channel_id'] for channel in output2['channels']]
    expected_output =   [channel['channel_id'], channel1['channel_id'],
                         channel2['channel_id'], channel3['channel_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output


# simple fail case for channels_listall
def test_channels_listall_fail(url, user_input, user3_input, user4_input, channel_input,
                      channel_input1, channel_input2, channel_input3):
        requests.delete(f'{url}clear')
        user1 = requests.post(f'{url}auth/register', json = user_input).json()
        user2 = requests.post(f'{url}auth/register', json = user3_input).json()
        user3 = requests.post(f'{url}auth/register', json = user4_input).json()

        channel_input.update({"token": user1['token']})
        channel_input1.update({"token": user1['token']})
        channel_input2.update({"token": user2['token']})
        channel_input3.update({"token": user2['token']})

        channel = requests.post(f'{url}channels/create', json = channel_input).json()

        input_data1 = {
            "token": user1['token'],
            "channel_id": channel['channel_id'],
            "user_id": user2['u_id']
        }
        input_data2 = {
            "token": user1['token'],
            "channel_id": channel['channel_id'],
            "user_id": user3['u_id']
        }
        input_data3 = {
            "token": user2['token'],
            "channel_id": channel['channel_id'],
            "user_id": user1['u_id']
        }
        input_data4 = {
            "token": user2['token'],
            "channel_id": channel['channel_id'],
            "user_id": user3['u_id']
        }
        requests.post(f'{url}channel/invite', json = input_data1).json()
        requests.post(f'{url}channel/invite', json = input_data2).json()
        requests.post(f'{url}channel/invite', json = input_data3).json()
        requests.post(f'{url}channel/invite', json = input_data4).json()

        r = requests.get(f'{url}channels/listall', json = user1['token'])
        assert r.status_code == 400

# simple sucess case for channels_create
def test_channels_create_success(url, user_input, channel_input):
    requests.delete(f'{url}clear')
    user1 = requests.post(f'{url}auth/register', json = user_input).json()

    channel_input.update({"token": user1['token']})
    output = requests.post(f'{url}channels/create', json = channel_input).json()
    assert output is not None
    assert output['channel_id'] is not None
    assert isinstance(output['channel_id'], int)

# simple fail case for channels_create
def test_channels_create_fail(url, user_input):
    requests.delete(f'{url}clear')
    user1 = requests.post(f'{url}auth/register', json = user_input).json()
    channel_data = {
                        "token": user1['token'],
                        "name": "anamethatistoolongbutlowercase",
                        "is_public":  True,
                    }
    r = requests.post(f'{url}channels/create', json = channel_data)
    assert r.status_code == 400

######################## One large test for all the channels functions  #################################

def test_channels_all(url, user_input, user3_input, user4_input, channel_input,
                      channel_input1, channel_input2, channel_input3):
    requests.delete(f'{url}clear')
    user1 = requests.post(f'{url}auth/register', json = user_input).json()
    user2 = requests.post(f'{url}auth/register', json = user3_input).json()
    user3 = requests.post(f'{url}auth/register', json = user4_input).json()

    channel_input.update({"token": user1['token']})
    channel_input1.update({"token": user1['token']})
    channel_input2.update({"token": user2['token']})
    channel_input3.update({"token": user2['token']})

    channel = requests.post(f'{url}channels/create', json = channel_input).json()
    channel1 = requests.post(f'{url}channels/create', json = channel_input1).json()
    channel2 = requests.post(f'{url}channels/create', json = channel_input2).json()
    channel3 = requests.post(f'{url}channels/create', json = channel_input3).json()

    assert channel is not None
    assert channel['channel_id'] is not None
    assert isinstance(channel['channel_id'], int)

    # test channels/list

    output1 = requests.get(f'{url}channels/list', params = {"token": user1['token']}).json()
    output2 = requests.get(f'{url}channels/list', params = {"token": user2['token']}).json()
    expected_output1 = [channel['channel_id'], channel1['channel_id']]
    expected_output2 = [channel2['channel_id'], channel3['channel_id']]

    check_list1 = [channel['channel_id'] for channel in output1['channels']]
    check_list2 = [channel['channel_id'] for channel in output2['channels']]

    check_list1.sort()
    expected_output1.sort()
    check_list2.sort()
    expected_output2.sort()

    assert check_list1 == expected_output1
    assert check_list2 == expected_output2

    # check listall
    input_data1 = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "user_id": user2['u_id']
    }
    input_data2 = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "user_id": user3['u_id']
    }
    input_data3 = {
        "token": user2['token'],
        "channel_id": channel['channel_id'],
        "user_id": user1['u_id']
    }
    input_data4 = {
        "token": user2['token'],
        "channel_id": channel['channel_id'],
        "user_id": user3['u_id']
    }
    requests.post(f'{url}channel/invite', json = input_data1).json()
    requests.post(f'{url}channel/invite', json = input_data2).json()
    requests.post(f'{url}channel/invite', json = input_data3).json()
    requests.post(f'{url}channel/invite', json = input_data4).json()

    output1 = requests.get(f'{url}channels/listall', params = {"token": user1['token']}).json()
    output2 = requests.get(f'{url}channels/listall', params = {"token": user2['token']}).json()

    check_list = [channel['channel_id'] for channel in output1['channels']]
    expected_output =   [channel['channel_id'], channel1['channel_id'],
                         channel2['channel_id'], channel3['channel_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output

    check_list = [channel['channel_id'] for channel in output2['channels']]
    expected_output =   [channel['channel_id'], channel1['channel_id'],
                         channel2['channel_id'], channel3['channel_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output
