import pytest
import requests
import json
import time

from http_fixtures import url

# Helpers
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

def join_channel(url, user, channel):
    # Add given user to given channel
    resp = requests.post(url + "channel/join", json = {"token": user['token'],
                                                       "channel_id": channel['channel_id']})
    result = json.loads(resp.text)
    assert result == {}
    return

# Actual Tests
def test_standup_start_failure(url):
    user = register_user(url, "test@test.com")
    channel = create_channel(url, user, "Channel", True)
    
    # Start a 1 second standup
    result = json.loads(requests.post(url + "standup/start", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'length': 1}).text)
    assert result['time_finish'] != None
    
    # Try start another right away
    result = json.loads(requests.post(url + "standup/start", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'length': 1}).text)
    assert result['code'] == 400
    # To ensure it doesn't last into the next test
    time.sleep(2)

def test_standup_start_success(url):
    user = register_user(url, "test@test.com")
    channel = create_channel(url, user, "Channel1", True)
    
    # Start a 1 second standup
    result = json.loads(requests.post(url + "standup/start", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'length': 1}).text)
    assert result['time_finish'] != None
    result = json.loads(requests.get(url + "standup/active", params = {'token': user['token'],
                                                                       'channel_id': channel['channel_id']}).text)
    assert result['is_active'] == True
    time.sleep(2)

def test_standup_active_failure(url):
    user = register_user(url, "test@test.com")
    channel = create_channel(url, user, "Channel1", True)
    
    # Start a 1 second standup
    result = json.loads(requests.post(url + "standup/start", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'length': 1}).text)
    assert result['time_finish'] != None
    
    # Check if standup active on channel that doesn't exist
    result = json.loads(requests.get(url + "standup/active", params = {'token': user['token'],
                                                                       'channel_id': 4}).text)
    assert result['code'] == 400

def test_standup_active_success(url):
    user = register_user(url, "test@test.com")
    channel = create_channel(url, user, "Channel1", True)
    
    # Start a 1 second standup
    result = json.loads(requests.post(url + "standup/start", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'length': 1}).text)
    assert result['time_finish'] != None
    
    # Check if standup active on channel that doesn't exist
    result = json.loads(requests.get(url + "standup/active", params = {'token': user['token'],
                                                                       'channel_id': channel['channel_id']}).text)
    assert result['is_active'] == True
    time.sleep(2)
    # Check again
    result = json.loads(requests.get(url + "standup/active", params = {'token': user['token'],
                                                                       'channel_id': channel['channel_id']}).text)
    assert result['is_active'] == False

def test_standup_send_failure(url):
    user = register_user(url, "test@test.com")
    channel = create_channel(url, user, "Channel1", True)
    
    # Send to a standup that hasn't started
    result = json.loads(requests.post(url + "standup/send", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'message': "test"}).text)
    assert result['code'] == 400

def test_standup_send_success(url):
    user = register_user(url, "test@test.com")
    channel = create_channel(url, user, "Channel1", True)
    
    # Start a 1 second standup
    result = json.loads(requests.post(url + "standup/start", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'length': 1}).text)
    assert result['time_finish'] != None
    
    # Send to the standup
    result = json.loads(requests.post(url + "standup/send", json = {'token': user['token'],
                                                          'channel_id': channel['channel_id'],
                                                          'message': "test"}).text)
    assert result == {}
    # Search for that message should return nothing for now
    result = json.loads(requests.get(url + "search", params = {'token': user['token'], 'query_str': "test"}).text)
    assert len(result['messages']) == 0
    time.sleep(2)
    
    # Search again
    result = json.loads(requests.get(url + "search", params = {'token': user['token'], 'query_str': "test"}).text)
    assert len(result['messages']) == 1
    time.sleep(2)

# Test that combines all the standup functionality
def test_all_standup_routes(url):
    # Prepare two users and two channels
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")
    channel1 = create_channel(url, user1, "Channel1", True)
    channel2 = create_channel(url, user2, "Channel2", True)
    
    # User2 tries to start a standup on channel1
    result = json.loads(requests.post(url + "standup/start", json = {'token': user2['token'],
                                                                     'channel_id': channel1['channel_id'],
                                                                     'length': 1}).text)
    assert result['code'] == 400
    
    # User 2 joins and tries again, but on both channels
    join_channel(url, user2, channel1)
    result = json.loads(requests.post(url + "standup/start", json = {'token': user2['token'],
                                                                     'channel_id': channel1['channel_id'],
                                                                     'length': 1}).text)
    assert result['time_finish'] != None
    result = json.loads(requests.post(url + "standup/start", json = {'token': user2['token'],
                                                                     'channel_id': channel2['channel_id'],
                                                                     'length': 1}).text)
    assert result['time_finish'] != None

    # Both users send messages to the standup
    result = json.loads(requests.post(url + "standup/send", json = {'token': user1['token'],
                                                          'channel_id': channel1['channel_id'],
                                                          'message': "first test"}).text)
    assert result == {}
    result = json.loads(requests.post(url + "standup/send", json = {'token': user2['token'],
                                                          'channel_id': channel1['channel_id'],
                                                          'message': "second test"}).text)
    assert result == {}
    result = json.loads(requests.post(url + "standup/send", json = {'token': user1['token'],
                                                          'channel_id': channel1['channel_id'],
                                                          'message': "third test"}).text)
    assert result == {}
    result = json.loads(requests.post(url + "standup/send", json = {'token': user2['token'],
                                                          'channel_id': channel2['channel_id'],
                                                          'message': "fourth test"}).text)
    assert result == {}
    
    # Message search shold return nothing for now, because standup active on both channels
    result = json.loads(requests.get(url + "standup/active", params = {'token': user1['token'],
                                                                       'channel_id': channel1['channel_id']}).text)
    assert result['is_active'] == True
    result = json.loads(requests.get(url + "standup/active", params = {'token': user2['token'],
                                                                       'channel_id': channel2['channel_id']}).text)
    assert result['is_active'] == True
    result = json.loads(requests.get(url + "search", params = {'token': user1['token'], 'query_str': "test"}).text)
    assert len(result['messages']) == 0
    time.sleep(2)
    # Message search should have one message now ,ordered correctly, and from the correct user, from channel1
    result = json.loads(requests.get(url + "standup/active", params = {'token': user1['token'],
                                                                       'channel_id': channel1['channel_id']}).text)
    assert result['is_active'] == False
    result = json.loads(requests.get(url + "search", params = {'token': user1['token'], 'query_str': "test"}).text)
    user1_profile = json.loads(requests.get(url + "user/profile", params = {'token': user1['token'], 'u_id': user1['u_id']}).text)
    user2_profile = json.loads(requests.get(url + "user/profile", params = {'token': user1['token'], 'u_id': user2['u_id']}).text)
    assert len(result['messages']) == 1
    assert result['messages'][0]['u_id'] == user2['u_id']
    assert result['messages'][0]['message'] == user1_profile['user']['handle_str'] + ": first test\n" + \
                                               user2_profile['user']['handle_str'] + ": second test\n" + \
                                               user1_profile['user']['handle_str'] + ": third test"

    # Channel 2 should also have a standup message with just user2 posting to it    
    result = json.loads(requests.get(url + "search", params = {'token': user2['token'], 'query_str': "fourth"}).text)
    assert len(result['messages']) == 1
    assert result['messages'][0]['message'] == user2_profile['user']['handle_str'] + ": fourth test"
    # But User1 should not be able to see it
    result = json.loads(requests.get(url + "search", params = {'token': user1['token'], 'query_str': "fourth"}).text)
    assert len(result['messages']) == 0
