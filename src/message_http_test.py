import pytest
import requests
import json
import urllib
import time

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

def test_message_send_success(url):
    '''
    Test that the message send path works
    '''
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")

    channel = create_channel(url, user1, "Channel1", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "test message"})
    message = json.loads(resp.text)
    assert message['message_id'] == 0

def test_message_send_error(url):
    '''
    Test that the message send path correctly raises access error
    '''
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")

    channel = create_channel(url, user1, "Channel1", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user2['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "test message"})
    # Check that this failed
    message = json.loads(resp.text)
    assert message['code'] == 400

def test_message_edit_success(url):
    '''
    Test that the message edit path is accessed correctly
    '''
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")

    channel = create_channel(url, user1, "Channel1", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "test message"})
    message = json.loads(resp.text)
    assert message['message_id'] == 0

    # Edit the message
    resp = requests.put(url + "message/edit", json = {"token": user1['token'],
                                              "message_id": message['message_id'],
                                              "message": "no message"})
    message = json.loads(resp.text)
    assert message == {}

    # Search for 'test' should find nothing
    resp = requests.get(url + "search?token=" + urllib.parse.quote_plus(user1['token']) + "&query_str=test")
    messages = json.loads(resp.text)
    assert messages['messages'] == []

    # Search using "no" should find the newly edited message
    resp = requests.get(f"{url}search", params = {'token': user1['token'], 'query_str': 'no'})
    messages = resp.json()
    assert len(messages) == 1
    assert messages['messages'][0]['message'] == 'no message'

def test_message_edit_error(url):
    '''
    Test that the message edit path returns access error correctly
    '''
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")

    channel = create_channel(url, user1, "Channel1", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "test message"})
    message = json.loads(resp.text)
    assert message['message_id'] == 0

    # Edit the message
    resp = requests.put(url + "message/edit", json = {"token": user2['token'],
                                              "message_id": message['message_id'],
                                              "message": "no message"})
    message = json.loads(resp.text)
    assert message['code'] == 400

def test_message_remove_success(url):
    '''
    Test that the message remove path is accessed correctly
    '''
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")

    channel = create_channel(url, user1, "Channel1", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "test message"})
    message = json.loads(resp.text)
    assert message['message_id'] == 0

    # Remove the message
    resp = requests.delete(url + "message/remove", json = {"token": user1['token'], "message_id": message['message_id']})
    message = json.loads(resp.text)
    print(message)
    assert message == {}

    # Search for 'test' should find nothing
    resp = requests.get(url + "search?token=" + urllib.parse.quote_plus(user1['token']) + "&query_str=test")
    messages = json.loads(resp.text)
    assert messages['messages'] == []

def test_message_remove_error(url):
    '''
    Test that the message remove path raises AccessErrors correctly
    '''
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")

    channel = create_channel(url, user1, "Channel1", True)

    # Send a message
    resp = requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel['channel_id'],
                                                       "message": "test message"})
    message = json.loads(resp.text)
    assert message['message_id'] == 0

    # Try making user2 remove the message
    resp = requests.delete(url + "message/remove", json = {"token": user2['token'], "message_id": message['message_id']})
    message = json.loads(resp.text)
    assert message['code'] == 400

def test_message_sendlater_error(url):
    """
    Test that the message sendlater path can raise errors correctly
    """
    requests.delete(url + "clear")
    # Register users and create a channel by user1
    user1 = register_user(url, "test@test.com")
    channel = create_channel(url, user1, "Test channel", True)
    cur_time = int(time.time())

    # Tries sending in a time in the past (10 seconds in the past)
    inval_time = cur_time - 10
    sendlater_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': "Hey hey",
        'time_sent': inval_time
    }
    resp = requests.post(f"{url}message/sendlater", json = sendlater_in)
    # Check that an error is raised
    server_response = resp.json()
    assert server_response['code'] == 400

def test_message_sendlater_success(url):
    """
    Test that the message sendlater path works like it should be
    """
    requests.delete(url + "clear")
    # Register users and create a channel by user1
    user1 = register_user(url, "test@test.com")
    channel = create_channel(url, user1, "Test channel", True)
    cur_time = int(time.time())

    # Tries sending a message 1 second in the future
    new_time = cur_time + 1
    sendlater_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': "Listen listen",
        'time_sent': new_time
    }
    requests.post(f"{url}message/sendlater", json = sendlater_in)

    # No messages should be in the server yet as 1 second has yet to pass
    messages_in = {'token': user1['token'], 'channel_id': channel['channel_id'], 'start': 0}
    msg_resp = requests.get(f"{url}channel/messages", params = messages_in).json()
    assert msg_resp['start'] == 0
    assert msg_resp['end'] == -1
    assert len(msg_resp['messages']) == 0

    time.sleep(2)
    # Checks again after 2 seconds have passed
    messages_in = {'token': user1['token'], 'channel_id': channel['channel_id'], 'start': 0}
    msg_resp = requests.get(f"{url}channel/messages", params = messages_in).json()
    assert msg_resp['start'] == 0
    assert msg_resp['end'] == -1
    assert len(msg_resp['messages']) == 1
    assert msg_resp['messages'][0]['message'] == 'Listen listen'

def test_message_react_error(url):
    """
    Test that the message react path can raise errors correctly
    """
    requests.delete(url + "clear")
    # Register users and create a channel by user1
    user1 = register_user(url, "test@test.com")

    # Tries reacting to an inexistent message, error should be raised
    react_in = {'token': user1['token'], 'message_id': 101, 'react_id': 1}
    resp = requests.post(f"{url}message/react", json = react_in)
    # Check that an error is raised
    server_response = resp.json()
    assert server_response['code'] == 400

def test_message_react_success(url):
    """
    Tests that the message react path works as it should be (returns an empty dictionary)
    """
    requests.delete(url + "clear")
    # Register users and create a channel by user1
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")
    channel = create_channel(url, user1, "Test Channel", True)
    # User2 joins the channel
    req = requests.post(f"{url}channel/join", json = {'token': user2['token'], 'channel_id': channel['channel_id']})
    assert req.json() == {}

    # Send a message to the channel
    send_in = {'token': user1['token'], 'channel_id': channel['channel_id'], 'message': "Hello..?"}
    msg = requests.post(f"{url}message/send", json = send_in).json()

    # User2 reacts to the message
    react_in = {'token': user2['token'], 'message_id': msg['message_id'], 'react_id': 1}
    resp = requests.post(f"{url}message/react", json = react_in)
    # Check if message_react returned an empty dictionary
    server_response = resp.json()
    assert server_response == {}

    # Check using channel_messages if react is in the data
    messages_in = {'token': user1['token'], 'channel_id': channel['channel_id'], 'start': 0}
    msg_resp = requests.get(f"{url}channel/messages", params = messages_in).json()
    assert msg_resp['start'] == 0
    assert msg_resp['end'] == -1
    assert msg_resp['messages'][0]['message'] == 'Hello..?'
    assert msg_resp['messages'][0]['reacts'][0]['react_id'] == 1
    assert msg_resp['messages'][0]['reacts'][0]['u_ids'] == [user2['u_id']]
    assert len(msg_resp['messages'][0]['reacts'][0]['u_ids']) == 1

def test_message_unreact_error(url):
    """
    Test that the message unreact path can raise errors correctly
    """
    requests.delete(url + "clear")
    # Register users and create a channel by user1
    user1 = register_user(url, "test@test.com")

    # Tries unreacting to an inexistent message, error should be raised
    unreact_in = {'token': user1['token'], 'message_id': 101, 'react_id': 1}
    resp = requests.post(f"{url}message/unreact", json = unreact_in)
    # Check that an error is raised
    server_response = resp.json()
    assert server_response['code'] == 400

def test_message_unreact_success(url):
    """
    Tests that the message unreact path works as it should be (returns an empty dictionary)
    """
    requests.delete(url + "clear")
    # Register users and create a channel by user1
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")
    channel = create_channel(url, user1, "Test Channel", True)
    # User2 joins the channel
    req = requests.post(f"{url}channel/join", json = {'token': user2['token'], 'channel_id': channel['channel_id']})
    assert req.json() == {}

    # Send a message to the channel
    send_in = {'token': user1['token'], 'channel_id': channel['channel_id'], 'message': "Hello..?"}
    msg = requests.post(f"{url}message/send", json = send_in).json()

    # User2 reacts then unreacts to the message
    react_in = {'token': user2['token'], 'message_id': msg['message_id'], 'react_id': 1}
    requests.post(f"{url}message/react", json = react_in)
    resp = requests.post(f"{url}message/unreact", json = react_in)
    # Check if message_unreact returned an empty dictionary
    server_response = resp.json()
    assert server_response == {}

    # Check using channel_messages if there are no reacts in the data
    messages_in = {'token': user1['token'], 'channel_id': channel['channel_id'], 'start': 0}
    msg_resp = requests.get(f"{url}channel/messages", params = messages_in).json()
    assert msg_resp['start'] == 0
    assert msg_resp['end'] == -1
    assert msg_resp['messages'][0]['message'] == 'Hello..?'
    assert len(msg_resp['messages'][0]['reacts']) == 0

def test_message_pin_error(url):
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    create_channel(url, user1, "Channel1", True)
    r = requests.post(url + "message/pin", json = {"token": user1['token'], "message_id": 65})
    assert r.status_code == 400

def test_message_pin_success(url):
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    channel = create_channel(url, user1, "Channel1", True)
    data = {"token": user1['token'], "channel_id": channel['channel_id'], "message": "test message"}
    msg = requests.post(url + "message/send", json = data).json()
    requests.post(url + "message/pin", json = {"token": user1['token'], "message_id": msg['message_id']})
    input_data = {"token": user1['token'], "channel_id": channel['channel_id'], "start": 0}
    messages = requests.get(f'{url}channel/messages', params = input_data).json()
    assert messages["messages"][msg['message_id']]["is_pinned"] == True

def test_message_unpin_error(url):
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    channel = create_channel(url, user1, "Channel1", True)
    data = {"token": user1['token'], "channel_id": channel['channel_id'], "message": "test message"}
    msg = requests.post(url + "message/send", json = data).json()
    r = requests.post(url + "message/unpin", json = {"token": user1['token'], "message_id": msg['message_id']})
    assert r.status_code == 400

def test_message_unpin_success(url):
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    channel = create_channel(url, user1, "Channel1", True)
    data = {"token": user1['token'], "channel_id": channel['channel_id'], "message": "test message"}
    msg = requests.post(url + "message/send", json = data).json()
    # pin the message
    requests.post(url + "message/pin", json = {"token": user1['token'], "message_id": msg['message_id']})
    input_data = {"token": user1['token'], "channel_id": channel['channel_id'], "start": 0}
    messages = requests.get(f'{url}channel/messages', params = input_data).json()
    assert messages["messages"][msg['message_id']]["is_pinned"] == True
    # unpin the message
    requests.post(url + "message/unpin", json = {"token": user1['token'], "message_id": msg['message_id']})
    input_data = {"token": user1['token'], "channel_id": channel['channel_id'], "start": 0}
    messages = requests.get(f'{url}channel/messages', params = input_data).json()
    assert messages["messages"][msg['message_id']]["is_pinned"] == False

def test_all_message_functions(url):
    '''
    Tests that all functions in message.py work alright together
    '''
    requests.delete(url + "clear")
    user1 = register_user(url, "test@test.com")
    user2 = register_user(url, "test2@test.com")

    channel1 = create_channel(url, user1, "Channel1", True)
    channel2 = create_channel(url, user2, "Channel1", True)

    # User1 tries sending a message to channel2
    result = json.loads(requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel2['channel_id'],
                                                       "message": "failed message"}).text)
    assert result['code'] == 400

    # User1 actually sends to channel1
    user1_message = json.loads(requests.post(url + "message/send", json = {"token": user1['token'],
                                                       "channel_id": channel1['channel_id'],
                                                       "message": "user1 message"}).text)
    assert user1_message['message_id'] == 0

    # User 2 tries to send to channel1 and fails
    result = json.loads(requests.post(url + "message/send", json = {'token': user2['token'],
                                                                   'channel_id': channel1['channel_id'],
                                                                   'message': "fail"}).text)
    assert result['code'] == 400

    # User 2 joins channel1 and tries again
    result = json.loads(requests.post(url + "channel/join", json = {'token': user2['token'], 'channel_id': channel1['channel_id']}).text)
    assert result == {}
    user2_message = json.loads(requests.post(url + "message/send", json = {'token': user2['token'],
                                                                   'channel_id': channel1['channel_id'],
                                                                   'message': "fail"}).text)
    assert user2_message['message_id'] == 1

    # User 2 tries to edit message from user 1 and fails
    result = json.loads(requests.put(url + "message/edit", json = {'token': user2['token'],
                                                                   'message_id': user1_message['message_id'],
                                                                   'message': "Hijacked"}).text)
    assert result['code'] == 400

    # user 1 pins their message
    requests.post(url + "message/pin", json = {"token": user1['token'], "message_id": user1_message['message_id']})

    # User 1 instead edits user 2's message, then removes its own message
    result = json.loads(requests.put(url + "message/edit", json = {'token': user1['token'],
                                                                   'message_id': user2_message['message_id'],
                                                                   'message': "Reverse Card"}).text)
    assert result == {}
    result = json.loads(requests.delete(url + "message/remove", json = {'token': user1['token'],
                                                                       'message_id': user1_message['message_id']}).text)
    assert result == {}

    # User2 should at least be able to edit his own message
    result = json.loads(requests.put(url + "message/edit", json = {'token': user2['token'],
                                                                   'message_id': user2_message['message_id'],
                                                                   'message': "I am humbled"}).text)
    assert result == {}

    # User2 tries to react to the already deleted user1's message and fails
    react_in = {'token': user2['token'], 'message_id': user1_message['message_id'], 'react_id': 1}
    result = requests.post(f"{url}message/react", json = react_in).json()
    assert result['code'] == 400

    # User2 and User1 reacts to user2's message
    react_in = {'token': user2['token'], 'message_id': user2_message['message_id'], 'react_id': 1}
    result = requests.post(f"{url}message/react", json = react_in).json()
    assert result == {}
    react_in = {'token': user1['token'], 'message_id': user2_message['message_id'], 'react_id': 1}
    result = requests.post(f"{url}message/react", json = react_in).json()
    assert result == {}
    # Check using channel_messages that the reacts are successful
    messages_in = {"token": user1['token'], "channel_id": channel1['channel_id'], "start": 0}
    messages = requests.get(f'{url}channel/messages', params = messages_in).json()
    assert messages['start'] == 0
    assert messages['end'] == -1
    assert len(messages['messages']) == 1
    assert len(messages['messages'][0]['reacts']) == 1
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert messages['messages'][0]['reacts'][0]['is_this_user_reacted'] == True
    # There should be 2 reacts in the message
    assert messages['messages'][0]['reacts'][0]['u_ids'][0] == user2['u_id']
    assert messages['messages'][0]['reacts'][0]['u_ids'][1] == user1['u_id']
    assert len(messages['messages'][0]['reacts'][0]['u_ids']) == 2

    # User2 unreacts to his own message
    unreact_in = {'token': user2['token'], 'message_id': user2_message['message_id'], 'react_id': 1}
    result = requests.post(f"{url}message/unreact", json = unreact_in).json()
    assert result == {}
    # Check using channel_messages that the unreact is successful
    messages_in = {"token": user2['token'], "channel_id": channel1['channel_id'], "start": 0}
    messages = requests.get(f'{url}channel/messages', params = messages_in).json()
    assert messages['start'] == 0
    assert messages['end'] == -1
    assert len(messages['messages']) == 1
    assert len(messages['messages'][0]['reacts']) == 1
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert messages['messages'][0]['reacts'][0]['is_this_user_reacted'] == False
    # There should be only 1 react left in the message
    assert messages['messages'][0]['reacts'][0]['u_ids'][0] == user1['u_id']
    assert len(messages['messages'][0]['reacts'][0]['u_ids']) == 1

    # pin 2 messages
    data = {"token": user1['token'], "channel_id": channel1['channel_id'], "message": "test message"}
    msg1 = requests.post(url + "message/send", json = data).json()
    requests.post(url + "message/pin", json = {"token": user1['token'], "message_id": msg1['message_id']})
    data = {"token": user1['token'], "channel_id": channel1['channel_id'], "message": "test message 2"}
    msg2 = requests.post(url + "message/send", json = data).json()
    requests.post(url + "message/pin", json = {"token": user1['token'], "message_id": msg2['message_id']})

    input_data = {"token": user1['token'], "channel_id": channel1['channel_id'], "start": 0}
    messages = requests.get(f'{url}channel/messages', params = input_data).json()

    check_id = [message['message_id'] for message in messages["messages"]]
    msg1_index = check_id.index(msg1['message_id'])
    msg2_index = check_id.index(msg2['message_id'])
    
    print(messages['messages'])

    assert messages["messages"][msg1_index]["is_pinned"] == True
    assert messages["messages"][msg2_index]["is_pinned"] == True

    # unpin one message
    requests.post(url + "message/unpin", json = {"token": user1['token'], "message_id": msg1['message_id']})
    input_data = {"token": user1['token'], "channel_id": channel1['channel_id'], "start": 0}
    messages = requests.get(f'{url}channel/messages', params = input_data).json()
    assert messages["messages"][msg1_index]["is_pinned"] == False

    messages = json.loads(requests.get(url + "search", params = {'token': user2['token'], 'query_str': "humbled"}).text)
    assert len(messages['messages']) == 1
    assert messages['messages'][0]['message_id'] == user2_message['message_id']

    # Sends one new message 3 seconds in the future by user1
    cur_time = int(time.time())
    new_time = cur_time + 3
    sendlater_in = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': "Last message",
        'time_sent': new_time
    }
    requests.post(f"{url}message/sendlater", json = sendlater_in)
    # There should still be 3 messages in the server now as 3 seconds has yet to pass
    messages_in = {'token': user1['token'], 'channel_id': channel1['channel_id'], 'start': 0}
    msg_resp = requests.get(f"{url}channel/messages", params = messages_in).json()
    assert msg_resp['start'] == 0
    assert msg_resp['end'] == -1
    assert len(msg_resp['messages']) == 3

    time.sleep(4)
    # Checks again after 3.5 seconds have passed
    messages_in = {'token': user1['token'], 'channel_id': channel1['channel_id'], 'start': 0}
    msg_resp = requests.get(f"{url}channel/messages", params = messages_in).json()
    assert msg_resp['start'] == 0
    assert msg_resp['end'] == -1
    assert len(msg_resp['messages']) == 4
    assert msg_resp['messages'][0]['message'] == 'Last message'

    # Message_sendlater should raise an error if we call it using the same time as before
    # since that time should have passed and is now in the past
    resp = requests.post(f"{url}message/sendlater", json = sendlater_in)
    server_response = resp.json()
    assert server_response['code'] == 400
