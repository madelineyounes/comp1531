import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import urllib

from error import InputError, AccessError
from http_fixtures import url, user_input, user2_input, user3_input
from http_fixtures import channel_input, channel_input1, channel_input2

######################## One fail and one success case for each function  #################################

# Simple success test
def test_user_profile_success(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    resp = requests.get(f'{url}user/profile', params=user).json()
    assert resp['user'] == {
        "u_id" : user['u_id'],
        "email" : user_input["email"],
        "name_first" : user_input["name_first"],
        "name_last" : user_input["name_last"],
        "handle_str" : "relainlemoney",
        "profile_img_url": ""
    }

# fail test as token should be invalid after logging out
def test_user_profile_fail(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    requests.post(f'{url}auth/logout', json = {"token": user['token']})
    r = requests.get(f'{url}user/profile', params=user)
    assert r.status_code == 400

# test checking if http wrap of setname works
def test_user_profile_setname_success(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    data = {"token": user['token'], "name_first": "Steve", "name_last": "Potato"}
    requests.put(f'{url}user/profile/setname', json = data)
    u_prof = requests.get(f'{url}user/profile', params=user).json()
    assert u_prof['user']['name_first'] == 'Steve'
    assert u_prof['user']['name_last'] == 'Potato'

# setname will fail when given no input for name
def test_user_profile_setname_fail(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    data = {"token": user['token'], "name_first": "", "name_last": "Potato"}
    r = requests.put(f'{url}user/profile/setname', json = data)
    assert r.status_code == 400

# test checking if http wrap of setemail works
def test_user_profile_setemail_success(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    data = {"token": user['token'], "email": "OliveS@mail.com"}
    requests.put(f'{url}user/profile/setemail', json = data)
    u_prof = requests.get(f'{url}user/profile', params=user).json()
    assert u_prof['user']['email'] == 'OliveS@mail.com'

# setmail fails with a invalid email
def test_user_profile_setemail_fail(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    data = {"token": user['token'], "email": "invalid.com"}
    r = requests.put(f'{url}user/profile/setemail', json = data)
    assert r.status_code == 400

# test checking if http wrap of sethandle works
def test_user_profile_sethandle_success(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    data = {"token": user['token'], "handle_str": "monkey"}
    requests.put(f'{url}user/profile/sethandle', json = data)
    u_prof = requests.get(f'{url}user/profile', params=user).json()
    assert u_prof['user']['handle_str'] == 'monkey'

# hanle is 21 characters so should fail
def test_user_profile_sethandle_fail(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    data = {"token": user['token'], "handle_str": "AvatarKorroRavaishere"}
    r = requests.put(f'{url}user/profile/sethandle', json = data)
    assert r.status_code == 400

######################## One large test for user file #################################

# Integration test for all the above functions
def test_user_full(url, user_input, user2_input, user3_input, channel_input, channel_input1, channel_input2):
    requests.delete(f'{url}clear')

    user = requests.post(f'{url}auth/register', json = user_input).json()
    user2 = requests.post(f'{url}auth/register', json = user2_input).json()
    user3 = requests.post(f'{url}auth/register', json = user3_input).json()

    # change all the details of both users
    data_name = {"token": user['token'], "name_first": "bill", "name_last": "monkey"}
    requests.put(f'{url}user/profile/setname', json = data_name)

    data_name2 = {"token": user2['token'], "name_first": "hayy", "name_last": "mann"}
    requests.put(f'{url}user/profile/setname', json = data_name2)

    data_email = {"token": user['token'], "email": "FriedChicken@mail.com"}
    requests.put(f'{url}user/profile/setemail', json = data_email)

    data_email2 = {"token": user2['token'], "email": "goatsAreTheBest@mail.com"}
    requests.put(f'{url}user/profile/setemail', json = data_email2)

    data_handle = {"token": user['token'], "handle_str": "you_wanna_pizza_me!"}
    requests.put(f'{url}user/profile/sethandle', json = data_handle)

    data_handle2 = {"token": user2['token'], "handle_str": "riddles"}
    requests.put(f'{url}user/profile/sethandle', json = data_handle2)

    channel_input.update({"token": user3['token']})
    channel_input1.update({"token": user['token']})
    channel_input2.update({"token": user2['token']})

    requests.post(f'{url}channels/create', json = channel_input).json()
    channel1 = requests.post(f'{url}channels/create', json = channel_input1).json()
    channel2 = requests.post(f'{url}channels/create', json = channel_input2).json()

    input_data1 = {
        "token": user['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user3['u_id']
    }
    input_data2 = {
        "token": user2['token'],
        "channel_id": channel2['channel_id'],
        "u_id": user['u_id']
    }

    requests.post(f'{url}channel/invite', json = input_data1).json()
    requests.post(f'{url}channel/invite', json = input_data2).json()

    input_data = {
        "token":user3["token"],
        "img_url":"https://s3.amazonaws.com/spectrumnews-web-assets/wp-content/uploads/2018/11/13154625/20181112-SHANK3monkey-844.jpg",
        "x_start": 0,
        "y_start": 0,
        "x_end": 800,
        "y_end": 500
    }
    requests.post(f'{url}user/profile/uploadphoto', json = input_data)

    # user check
    resp = requests.get(f'{url}user/profile', params=user).json()
    assert resp['user'] == {
        "u_id" : user['u_id'],
        "email" : "FriedChicken@mail.com",
        "name_first" : "bill",
        "name_last" : "monkey",
        "handle_str" : "you_wanna_pizza_me!",
        "profile_img_url": ""
    }

    # user2 check
    resp1 = requests.get(f'{url}user/profile', params=user2).json()
    assert resp1['user'] == {
        "u_id" : user2['u_id'],
        "email" : "goatsAreTheBest@mail.com",
        "name_first" : "hayy",
        "name_last" : "mann",
        "handle_str" : "riddles",
        "profile_img_url": ""
    }

    resp3 = requests.get(f'{url}user/profile', params=user3).json()
    assert resp3['user']["profile_img_url"] != ""
