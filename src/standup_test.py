import pytest
from auth import auth_login, auth_register, auth_logout
from channels import channels_create
from channel import channel_invite
from message import message_send, message_edit, message_remove
from error import AccessError, InputError
from standup import standup_start, standup_active, standup_send
from other import clear, search
from data import data
from user import user_profile
import time

"""
def test_simple_tests():
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)
    
    standup_start(user['token'], channel['channel_id'], 1)
    standup_send(user['token'], channel['channel_id'], "test")
    assert len(search(user['token'], "test")['messages']) == 0
    time.sleep(2)
    assert len(search(user['token'], "test")['messages']) == 1

def test_again():
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)
    
    standup_start(user['token'], channel['channel_id'], 1)
    assert standup_active(user['token'], channel['channel_id'])['is_active']

"""
############################ standup_start ##############################

def test_standup_start_invalid_inputs():
    '''
    Test basic error raising from invalid inputs
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    user2 = auth_register("test2@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)

    # Invalid token raises AccessError
    with pytest.raises(AccessError):
        standup_start("notToken", channel['channel_id'], 7)
    
    # Caller not in channel raises AccessError
    with pytest.raises(AccessError):
        standup_start(user2['token'], channel['channel_id'], 7)

    # Invalid channel_id raises InputError
    with pytest.raises(InputError):
        standup_start(user['token'], -1, 7)

    # Non-positive duration raises InputError
    with pytest.raises(InputError):
        standup_start(user['token'], channel['channel_id'], 0)

def test_standup_start_standup_already_active():
    '''
    Test error is raised when a standup is already active
    and another is called
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)

    standup_start(user['token'], channel['channel_id'], 2)

    with pytest.raises(InputError):
        standup_start(user['token'], channel['channel_id'], 2)
    time.sleep(3)

def test_standup_start_after_allowed_again():
    '''
    Test that after the first standup is over, another can start
    without errors
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)
    
    standup_start(user['token'], channel['channel_id'], 1)
    time.sleep(2)
    standup_start(user['token'], channel['channel_id'], 1)
    time.sleep(2)

def test_standup_start_standup_in_another_channel():
    '''
    Test that a standup can be started in another channel
    regardless of one started simultaneously in the first channel
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel1 = channels_create(user['token'], "Channel1", True)
    channel2 = channels_create(user['token'], "Channel2", True)

    standup_start(user['token'], channel1['channel_id'], 1)

    # This causes error
    with pytest.raises(InputError):
        standup_start(user['token'], channel1['channel_id'], 1)
    # While this works fine
    standup_start(user['token'], channel2['channel_id'], 1)
    
    assert standup_active(user['token'], channel1['channel_id'])
    assert standup_active(user['token'], channel2['channel_id'])
    
    time.sleep(2)

############################ standup_active ##############################
def test_standup_active_invalid_inputs():
    '''
    Test basic error raising from invalid inputs
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)

    # invalid token raises AccessError
    with pytest.raises(AccessError):
        standup_active("notToken", channel['channel_id'])

    # invalid channel_id raises InputError
    with pytest.raises(InputError):
        standup_active(user['token'], -1)

def test_standup_active_standup_active():
    '''
    Test that during the interval of an active standup, standup active returns true
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)
    
    start = standup_start(user['token'], channel['channel_id'], 1)
    check = standup_active(user['token'], channel['channel_id'])
    assert check['is_active'] == True
    assert check['time_finish'] == start['time_finish']
    
    time.sleep(2)

def test_standup_active_standup_not_active():
    '''
    Test that when a standup is not active standup active returns False, and None
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)

    check = standup_active(user['token'], channel['channel_id'])
    assert check['is_active'] == False
    assert check['time_finish'] == None

    standup_start(user['token'], channel['channel_id'], 1)
    time.sleep(2)

    check = standup_active(user['token'], channel['channel_id'])
    assert check['is_active'] == False
    assert check['time_finish'] == None

def test_standup_active_active_in_another_channel():
    '''
    Test that standup active returns false in one channel, if
    a standup is active in another (Channels should be independent)
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel1 = channels_create(user['token'], "Channel1", True)
    channel2 = channels_create(user['token'], "Channel2", True)
    
    standup_start(user['token'], channel1['channel_id'], 1)
    result1 = standup_active(user['token'], channel1['channel_id'])
    result2 = standup_active(user['token'], channel2['channel_id'])
    
    assert result1['is_active'] == True
    assert result2['is_active'] == False
    time.sleep(2)

############################ standup_send ##############################
def test_standup_send_invalid_token():
    '''
    Test basic error raising from invalid inputs
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    user2 = auth_register("test2@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)
    standup_start(user['token'], channel['channel_id'], 1)

    # User not in channel causes access error
    with pytest.raises(AccessError):
        standup_send(user2['token'], channel['channel_id'], "message")

    # invalid token raises AccessError
    with pytest.raises(AccessError):
        standup_send("notToken", channel['channel_id'], "message")

    # invalid channel_id raises InputError
    with pytest.raises(InputError):
        standup_send(user['token'], -1, "message")

    # message over 1000 characters long raises InputError
    message = "a" * 1001
    with pytest.raises(InputError):
        standup_send(user['token'], channel['channel_id'], message)
    time.sleep(2)

def test_standup_send_standup_not_active():
    '''
    Test that standup_send raises an InputError if called while a standup
    is not currently active
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)

    with pytest.raises(InputError):
        standup_send(user['token'], channel['channel_id'], "message")

def test_standup_send_single_message():
    '''
    Test that a single message collected during the standup period is sent afterwards
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)
    
    standup_start(user['token'], channel['channel_id'], 1)
    standup_send(user['token'], channel['channel_id'], "message")
    time.sleep(2)

    check = search(user['token'], "message")
    assert len(check['messages']) == 1
    assert check['messages'][0]['message'] == "firstnamelastname: message"

def test_standup_send_during_standup():
    '''
    Test that messages sent during the standup period are not actually sent
    untill after, and then, all as one message
    '''
    clear()
    user = auth_register("test@test.com", "password", "Firstname", "Lastname")
    channel = channels_create(user['token'], "Channel", True)
    
    standup_start(user['token'], channel['channel_id'], 1)

    standup_send(user['token'], channel['channel_id'], "message1")
    check = search(user['token'], "message1")
    assert len(check['messages']) == 0
    standup_send(user['token'], channel['channel_id'], "message2")
    check = search(user['token'], "message2")
    assert len(check['messages']) == 0
    time.sleep(4)
    check = search(user['token'], "message")
    assert len(check['messages']) == 1

    name = user_profile(user['token'], user['u_id'])['user']['handle_str']

    assert check['messages'][0]['message'] == name + ": message1" + '\n' + name + ": message2"
