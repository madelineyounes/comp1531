""" Http tests focused on functions in auth.py """
import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import urllib

from error import InputError, AccessError
from http_fixtures import url, user_input, user2_input, user3_input, user4_input, invalid_user_input

######################## One fail and one success case for each function  #################################

# simple success case for auth_register
def test_auth_register_success(url, user_input):
    requests.delete(f'{url}clear')
    r = requests.post(f'{url}auth/register', json = user_input)
    user = r.json()
    assert user['u_id'] == 0
    assert user['token'] is not None

# simple fail case for auth_register
def test_auth_register_fail(url, invalid_user_input):
    requests.delete(f'{url}clear')
    r = requests.post(f'{url}auth/register', json = invalid_user_input)
    assert r.status_code == 400

# simple success case for auth_logout
def test_auth_logout_success(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    result = requests.post(f'{url}auth/logout', json = {"token": user['token']}).json()
    assert result['is_success']

# simple fail case for auth_logout
def test_auth_logout_fail(url, user_input):
    requests.delete(f'{url}clear')
    requests.post(f'{url}auth/register', json = user_input)
    result = requests.post(f'{url}auth/logout', json = {"token": "invalidToken"}).json()
    assert not result['is_success']

# simple success case for auth_login
def test_auth_login_success(url, user_input):
    requests.delete(f'{url}clear')
    user = requests.post(f'{url}auth/register', json = user_input).json()
    requests.post(f'{url}auth/logout', json = {"token": user['token']})
    data = {
        "email": user_input["email"],
        "password": user_input["password"]
    }
    result = requests.post(f'{url}auth/login', json = data).json()
    assert result['u_id'] == 0
    assert result['token'] is not None

# simple fail case for auth_login
def test_auth_login_fail(url, user_input):
    requests.delete(f'{url}clear')
    data = {
        "email": "notcorrectformat"
    }
    r = requests.post(f'{url}auth/passwordreset/request', json = data)
    assert r.status_code == 400

# simple success case for auth_passwordreset_request
def test_auth_passwordreset_request_sucess(url):
    requests.delete(f'{url}clear')
    data = {
        "email": "madeline.younes@gmail.com",
        "password": "pihello31",
        "name_first": "Madeline",
        "name_last": "Younes"
    }
    requests.post(f'{url}auth/register', json = data)
    r = requests.post(f'{url}auth/passwordreset/request', json=data).json()
    assert r == {}

# simple fail case for auth_passwordreset_request
def test_auth_passwordreset_request_fail(url):
    requests.delete(f'{url}clear')
    r = requests.post(f'{url}auth/passwordreset/request', json = {"email": "notcorrectformat"})
    assert r.status_code == 400

""" This is labelled as a success case, but the token field sent is empty
    I think it should be a fail case
# simple success case for auth_passwordreset_reset
def test_auth__passwordreset_reset_fail(url, user_input):
    requests.delete(f'{url}clear')
    r = requests.post(f'{url}/auth/passwordreset/reset', json = {"reset_code": "", "new_password": "testPassword"}).json()
    assert r == {}
"""

# simple fail case for auth_passwordreset_reset
def test_auth_passwordreset_reset_fail(url, user_input):
    requests.delete(f'{url}clear')
    r = requests.post(f'{url}/auth/passwordreset/reset', json = {"reset_code": "notcorrectcode", "new_password": "testPassword"})
    assert r.status_code == 400

######################## One large test for auth file #################################

def test_auth_full(url, user_input, user2_input, user3_input, user4_input):
    user = requests.post(f'{url}auth/register', json = user_input).json()
    user2 = requests.post(f'{url}auth/register', json = user2_input).json()
    assert user['u_id'] == 0
    assert user2['u_id'] == 1

    result = requests.post(f'{url}auth/logout', json = {"token": user2['token']}).json()
    assert result['is_success']

    user3 = requests.post(f'{url}auth/register', json = user3_input).json()
    user4 = requests.post(f'{url}auth/register', json = user4_input).json()
    assert user3['u_id'] == 2
    assert user4['u_id'] == 3

    result = requests.post(f'{url}auth/logout', json = {"token": user3['token']}).json()
    assert result['is_success']
    result = requests.post(f'{url}auth/logout', json = {"token": user['token']}).json()
    assert result['is_success']

    data = {
        "email": user_input["email"],
        "password": user_input["password"]
    }
    result = requests.post(f'{url}auth/login', json = data).json()
    assert result['u_id'] == 0
    assert result['token'] is not None

    data = {
        "email": user2_input["email"],
        "password": user2_input["password"]
    }
    result = requests.post(f'{url}auth/login', json = data).json()
    assert result['u_id'] == 1
    assert result['token'] is not None

    data = {
        "email": user3_input["email"],
        "password": user3_input["password"]
    }
    result = requests.post(f'{url}auth/login', json = data).json()
    assert result['u_id'] == 2
    assert result['token'] is not None
