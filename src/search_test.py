""" Whitebox testing of search function until message_send is finished """
from data import data
from auth import auth_register, auth_login
from channel import channel_invite, channel_join, channel_addowner
from channels import channels_create
from message import message_send, message_remove, message_edit
from error import AccessError
from datetime import timezone, datetime
from other import search, clear

import pytest

######################## Tests focused on search #################################

def test_search_single_channel_single_message_single_return():
    """
    Tests that given a single channel that the user is a member of, and a valid token,
    a message is returned from the search function
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "channel", True)

    # Forcing a message into channel['channel_messages']['messages']
    message_send(user['token'], channel['channel_id'], "message string")

    # Calling a search with the query string "message"
    result = search(user['token'], "message")
    del result['messages'][0]['time_created']
    assert result['messages'] == [{'message_id': 0, 'u_id': user['u_id'], 'message': "message string", 'is_pinned': False, 'reacts': []}]


def test_search_single_channel_single_message_single_return_strange_input():
    """
    Tests that given a single channel that the user is a member of, and a valid token,
    a message containing non-english characters is returned from the search function
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "channel", True)

    # Forcing a message into channel['channel_messages']['messages']
    message_send(user['token'], channel['channel_id'], "message $$$4%%")

    # Calling a search with the query string "$$$4%%"
    result = search(user['token'], "$$$4%%")
    del result['messages'][0]['time_created']
    assert result['messages'] == [{'message_id': 0, 'u_id': user['u_id'], 'message': "message $$$4%%", 'is_pinned': False, 'reacts': []}]


def test_search_query_partway_through_string():
    """
    Tests that given a single channel that the user is a member of, and a valid token,
    a message where the query is not its own separate word, still works
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "channel", True)

    # Forcing a message into channel['channel_messages']['messages']
    message_send(user['token'], channel['channel_id'], "testtestquerytest test word")

    # Calling a search with the query string "query"
    result = search(user['token'], "query")
    del result['messages'][0]['time_created']
    assert result['messages'] == [{'message_id': 0, 'u_id': user['u_id'], 'message': "testtestquerytest test word", 'is_pinned': False, 'reacts': []}]


def test_search_single_channel_single_message_no_match():
    """
    Tests that given a single channel that the user is a member of, and a valid token,
    an empty list is returned if no match is found
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "channel", True)

    # Forcing a message into channel['channel_messages']['messages']
    message_send(user['token'], channel['channel_id'], "message $$$4%%")

    # Calling a search with the query string "none"
    result = search(user['token'], "none")
    assert result['messages'] == []


def test_search_no_channels():
    """
    Tests that given a single channel that the user is a member of, and a valid token,
    an empty list is returned if user is not in any channels
    """
    clear()
    # Registering a user
    user = auth_register("test@test.com", "password", "firstName", "lastName")

    # Calling a search with the query string "none"
    result = search(user['token'], "none")
    assert result['messages'] == []


def test_search_single_channel_multiple_messages_single_return():
    """
    Tests that given a channel that the user is a member of, and a valid token,
    a message can be matched from multiple messages
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "channel", True)

    # Forcing messages into channel['channel_messages']['messages']
    message_send(user['token'], channel['channel_id'],"message string")
    message_send(user['token'], channel['channel_id'],"message int")
    message_send(user['token'], channel['channel_id'],"message bool")

    # Calling a search with the query string "bool"
    result = search(user['token'], "bool")
    del result['messages'][0]['time_created']
    assert result['messages'] == [{'message_id': 2, 'u_id': user['u_id'], 'message': "message bool", 'is_pinned': False, 'reacts': []}]

def test_search_multiple_channels_single_return():
    """
    Tests that given a channel the user is a member of, and a valid token,
    a message can be matched from across multiple channels
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel1 = channels_create(user['token'], "channel1", True)
    channel2 = channels_create(user['token'], "channel2", True)
    channel3 = channels_create(user['token'], "channel3", True)

    # Forcing messages into channel['channel_messages']['messages']
    message_send(user['token'], channel1['channel_id'],"message string")
    message_send(user['token'], channel2['channel_id'],"message int")
    message_send(user['token'], channel3['channel_id'],"message bool")

    # Calling a search with the query string "bool"
    result = search(user['token'], "bool")
    del result['messages'][0]['time_created']
    assert result['messages'] == [{'message_id': 2, 'u_id': user['u_id'], 'message': "message bool", 'is_pinned': False, 'reacts': []}]


def test_search_single_channel_multiple_returns():
    """
    Tests that given a channel the user is a member of, and a valid token,
    all matching messages can be matched from a list of messages
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "channe1", True)

    # Forcing messages into channel['channel_messages']['messages']
    message_send(user['token'], channel['channel_id'],"message string")
    message_send(user['token'], channel['channel_id'],"message int")
    message_send(user['token'], channel['channel_id'],"message bool")

    # calling a search with the query string "message"
    result = search(user['token'], "message")
    assert len(result['messages']) == 3

def test_search_invalid_token():
    """
    Tests that given a single channel that the user is a member of, and an invalid token,
    raises an Access Error
    """
    clear()
    # Registering a user and creating a channel
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "channel", True)

    # Forcing a message into channel['channel_messages']['messages']
    message_send(user['token'], channel['channel_id'], "message string")

    # Calling a search with invalid token
    with pytest.raises(AccessError):
        search(-1, "message")


######################## BLACKBOX Tests focused on search #################################

def test_search_multiple_channels_no_match():
    """
    Test that given several channels the user is part of (both public and private channels),
    No messages is returned when there is not a single match
    """
    clear()
    # Register user and create channels
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "Public_channel", True)
    channel2 = channels_create(user['token'], "Private_channel", False)
    channel3 = channels_create(user['token'], "Test_channel", True)

    # Send some messages in each channel
    message_send(user['token'], channel['channel_id'], 'Who are you?')
    message_send(user['token'], channel['channel_id'], 'What is your favorite color?')
    message_send(user['token'], channel2['channel_id'], 'What is your name')
    message_send(user['token'], channel2['channel_id'], 'Whose pen is this?')
    message_send(user['token'], channel3['channel_id'], '9 + 10 = 21')
    message_send(user['token'], channel3['channel_id'], 'Peek a boo')

    # Calling search for the user with an irrelevant query string
    result = search(user['token'], "Ketchup")
    assert result['messages'] == []

def test_search_other_members():
    """
    Test that given messages sent by other user in the channel,
    Messages can returned by search when a relevant query string is given.
    """
    clear()
    # Register users
    user = auth_register("test1@test.com", "Reanxdi920", "Anesthesia", "Rory")
    user2 = auth_register("test2@test.com", "Ascniw101", "Pennicilin", "Mirin")
    user3 = auth_register("test3@test.com", "Cpasmc20", "Borgeis", "Filin")

    # Create a channel and let users join
    channel = channels_create(user['token'], "Public_channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages (A conversation between 2 members)
    message_send(user2['token'], channel['channel_id'], 'Hello there')
    message_send(user3['token'], channel['channel_id'], 'Wassup')
    msg3 = message_send(user2['token'], channel['channel_id'], 'Who is the owner?')
    message_send(user3['token'], channel['channel_id'], 'Not me')

    # Calling search for user with the query string 'owner'
    result = search(user['token'], "owner")
    assert result['messages'][0]['message_id'] == msg3['message_id']
    assert result['messages'][0]['u_id'] == user2['u_id']
    assert result['messages'][0]['message'] == "Who is the owner?"

def test_search_edited_message():
    """
    Test that given a message that has been edited,
    The previous message will not be returned by search
    """
    clear()
    # Register user and create channels
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "Public_channel", True)

    # Send some messages in each channel
    msg1 = message_send(user['token'], channel['channel_id'], 'first!!')
    message_send(user['token'], channel['channel_id'], 'Anybody there?')
    msg3 = message_send(user['token'], channel['channel_id'], 'Guess I am the first one here')
    # Edit the messages
    message_edit(user['token'], msg1['message_id'], 'Message no longer available')
    message_edit(user['token'], msg3['message_id'], 'Beep beep')

    # Calling search for the user with the query string first
    result = search(user['token'], "first")
    assert result['messages'] == []

def test_search_removed_message():
    """
    Test that given several messages that has been removed,
    The messages should not be returned by search if given a query string from those messages
    """
    clear()
    # Register user and create channels
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    channel = channels_create(user['token'], "Public_channel", True)

    # Send some messages in each channel
    msg1 = message_send(user['token'], channel['channel_id'], 'lol')
    msg2 = message_send(user['token'], channel['channel_id'], 'lol')
    msg3 = message_send(user['token'], channel['channel_id'], 'lol')
    # Remove the messages
    message_remove(user['token'], msg1['message_id'])
    message_remove(user['token'], msg2['message_id'])
    message_remove(user['token'], msg3['message_id'])

    # Calling search for the user with the query string lol
    result = search(user['token'], "lol")
    assert result['messages'] == []

def test_search_user_not_in_channel():
    """
    Test that given a valid token and query string,
    the search function doesn't return a message if its in a
    channel that the caller is not a member of
    """
    clear()
    # Register user and create channels
    user1 = auth_register("test@test.com", "password", "firstName", "lastName")
    user2 = auth_register("test2@test.com", "password", "firstName2", "lastName2")
    channel1 = channels_create(user1['token'], "Public_channel", True)
    channel2 = channels_create(user2['token'], "Public_channel1", True)

    message_send(user1['token'], channel1['channel_id'], 'Here')
    message_send(user2['token'], channel2['channel_id'], 'But not here')

    result = search(user2['token'], "not")
    del result['messages'][0]['time_created']

    assert result['messages'] == [{
        'message_id': 1,
        'u_id': user2['u_id'],
        'message': "But not here",
        'reacts': [],
        'is_pinned': False
        }]
