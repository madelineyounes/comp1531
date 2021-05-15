import pytest
import requests
import json
import urllib

from http_fixtures import url


def register_user(url, email):
    # Use the auth/register route to register a user
    registered = requests.post(url + 'auth/register', json = {"email": email, "password": "password",
                                                              "name_first": "test", "name_last": "test"})
    # Convert result from JSON to python dictionary and check it exists
    user = json.loads(registered.text)
    assert user is not None
    return user

def create_channel(url, user, name, public):
    # Create channel
    resp = requests.post(url + "channels/create", json = {"token": user['token'],
                                                          "name": name,
                                                          "is_public": public})
    channel = json.loads(resp.text)
    assert channel['channel_id'] != None
    return channel


def test_clear_and_users_all_success(url):
    '''
    Test success of users_all path
    '''
    requests.delete(url + "clear")
    user = register_user(url, "test@test.com")

    # Check that a user was created and users_all returns it
    resp = requests.get(url + 'users/all', params={'token': user['token']})
    users_all = json.loads(resp.text)
    assert users_all['users'] == [{'u_id': user['u_id'],
                                   'email': "test@test.com",
                                   'name_first': "test",
                                   'name_last': "test",
                                   'handle_str': "testtest",
                                   'profile_img_url': ""}]
    # Clear the data file
    requests.delete(url + "clear")
    # Check that the user is gone (invalid token when accessing anything)
    resp = requests.get(url + 'users/all', params={'token': user['token']})
    users_all = json.loads(resp.text)
    assert users_all['code'] == 400

def test_users_all_error(url):
    '''
    Test success of users_all path
    '''
    requests.delete(url + "clear")

    resp = requests.get(url + 'users/all', params={'token': "not valid"})
    users_all = json.loads(resp.text)
    print(users_all)
    assert users_all['code'] == 400

def test_admin_permission_change_success_error(url):
    '''
    Test that admin is able to change their permission
    '''
    requests.delete(url + "clear")

    user1 = register_user(url, "test@test.com")

    user2 = register_user(url, "test2@test.com")

    # Check that user2 cannot demote user1
    resp = requests.post(url + "admin/userpermission/change", json = {"token": user2['token'],
                                                                     "u_id": user1['u_id'], "permission_id": 2})
    result = json.loads(resp.text)
    assert result['code'] == 400

    # Have user1 promote user2
    resp = requests.post(url + "admin/userpermission/change", json = {"token": user1['token'],
                                                                     "u_id": user2['u_id'], "permission_id": 1})

    # Check that user2 can now demote user1
    requests.post(url + "admin/userpermission/change", json = {"token": user2['token'],
                                                                     "u_id": user1['u_id'], "permission_id": 2})

    # User1 should now be unable to demote user2
    resp = requests.post(url + "admin/userpermission/change", json = {"token": user1['token'],
                                                                     "u_id": user2['u_id'], "permission_id": 2})
    result = json.loads(resp.text)
    assert result['code'] == 400

def test_search_success(url):
    '''
    Test that search path is called correctly
    '''
    requests.delete(url + "clear")

    user1 = register_user(url, "test@test.com")

    # Create channel
    channel = create_channel(url, user1, "channel", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "My time has come."})
    message = json.loads(resp.text)
    assert message['message_id'] == 0

    # Search for the query string "time"
    resp = requests.get(url + "search?token=" + urllib.parse.quote_plus(user1['token']) + "&query_str=time")
    result = json.loads(resp.text)
    assert result['messages'][0]['message'] == "My time has come."

def test_search_failure(url):
    '''
    Test that the search path raises errors correctly
    '''
    requests.delete(url + "clear")

    user1 = register_user(url, "test@test.com")

    # Create channel
    channel = create_channel(url, user1, "channel", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "My time has come."})
    message = json.loads(resp.text)
    assert message['message_id'] == 0

    # Search for the query string "time", but an invalid token
    resp = requests.get(url + "search?token=" + "invalidtoken" + "&query_str=time")
    result = json.loads(resp.text)
    assert result['code'] == 400

# Test for all routes that use other functions
def test_all_other_functions(url):
    requests.delete(url + "clear")
    # Register two users
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")

    # Create a channel from each user
    channel2 = create_channel(url, user2, "channel2", True)
    channel1 = create_channel(url, user1, "channel1", True)

    # User1 gives admin permissions to user2, then user2 should be able to join as owner
    result = json.loads(requests.post(url + "admin/userpermission/change", json = {"token": user1['token'],
                                                                     "u_id": user2['u_id'], "permission_id": 1}).text)
    assert result == {}

    # User2 joins user1's channel
    result = json.loads(requests.post(url + "channel/join", json = {"token": user2['token'],
                                                         "channel_id": channel1['channel_id']}).text)
    assert result == {}


    # Both users send messages to channel1
    result = json.loads(requests.post(url + "message/send", json = {"token": user2['token'],
                                                       "channel_id": channel1['channel_id'],
                                                       "message": "message from user2"}).text)
    assert result['message_id'] == 0

    user1_message = json.loads(requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel1['channel_id'],
                                                       "message": "message from user1"}).text)
    assert user1_message['message_id'] == 1

    # User2 sends a message on its own channel
    user2_message = json.loads(requests.post(url + "message/send", json = {"token": user2['token'],
                                                       "channel_id": channel2['channel_id'],
                                                       "message": "message to myself"}).text)
    assert user2_message['message_id'] == 2

    # User1 uses search with 'message' and finds two messages
    messages = json.loads(requests.get(url + "search", params = {'token': user1['token'], 'query_str': "message"}).text)
    assert len(messages['messages']) == 2

    # User2 searches for the same thing and finds 3 messages
    messages = json.loads(requests.get(url + "search", params = {'token': user2['token'], 'query_str': "message"}).text)
    assert len(messages['messages']) == 3

    # User2 is an owner and should be able to delete messages from channel1
    result = json.loads(requests.delete(url + "message/remove", json = {'token': user2['token'],
                                                                        'message_id': user1_message['message_id']}).text)
    assert result == {}
    # User1 uses search with 'message' and finds one message
    messages = json.loads(requests.get(url + "search", params = {'token': user1['token'], 'query_str': "message"}).text)
    assert len(messages['messages']) == 1

    # User 2 should be able to demote user1, so user1 joins channel2 as a normal user
    result = json.loads(requests.post(url + "admin/userpermission/change", json = {"token": user2['token'],
                                                                     "u_id": user1['u_id'], "permission_id": 2}).text)
    assert result == {}

    result = json.loads(requests.post(url + "channel/join", json = {"token": user1['token'],
                                                         "channel_id": channel2['channel_id']}).text)
    assert result == {}

    # User1 should be unable to remove messages here because of his new permission
    result = json.loads(requests.delete(url + "message/remove", json = {'token': user1['token'],
                                                                        'message_id': user2_message['message_id']}).text)
    assert result['code'] == 400
