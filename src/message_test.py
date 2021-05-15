import pytest
import time
from auth import auth_register, auth_logout
from channel import channel_messages, channel_join
from channels import channels_create
from message import find_react_id_index, message_send, message_remove, message_edit, message_sendlater, message_react, message_unreact, message_pin, message_unpin
from error import AccessError, InputError
from other import clear
from data import data

####################### Tests for helper functions #####################
def test_find_react_id_index_empty_list():
    assert find_react_id_index([], 1) == -1

def test_find_react_id_index_valid_list():
    reacts_list = [
            {
            'react_id': 0,
            'u_ids': [0],
            'is_this_user_reacted': True
        },
        {
            'react_id': 1,
            'u_ids': [0, 1, 2],
            'is_this_user_reacted': True
        },
        {
            'react_id': 2,
            'u_ids': [0, 1],
            'is_this_user_reacted': True
        }
    ]
    assert find_react_id_index(reacts_list, 2) == 2

####################### Tests for message_send function #####################

def test_message_send_invalid_message_length():
    '''
    Input:
        Message_send is given an invalid message (length of characters > 1000)

    Output:
        message_send should raise an InputError
    '''
    clear()
    invalid_msg = 'a' * 1001
    user = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')
    channel = channels_create(user['token'], "Test_Channel", True)

    with pytest.raises(InputError):
        message_send(user['token'], channel['channel_id'], invalid_msg)

def test_message_send_empty_message():
    '''
    Input:
        Message_send is given an empty message ('')

    Output:
        message_send should raise an InputError
    '''
    clear()
    invalid_msg = ''
    user = auth_register('jimmykelly@gmail.com', 'Meo02MnKlej', 'Jimmy', 'Kelly')
    channel = channels_create(user['token'], "Test_Channel", True)

    with pytest.raises(InputError):
        message_send(user['token'], channel['channel_id'], invalid_msg)

def test_message_send_invalid_channel():
    '''
    Input:
        A channel_id that the user is not part of

    Output:
        message_send should raise an AccessError
    '''
    clear()
    user = auth_register('canoeboon@gmail.com', 'Moenal02MnKlej', 'Canoe', 'Boon')
    user2 = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')
    channel = channels_create(user['token'], "Test_Channel", False)

    with pytest.raises(InputError):
        message_send(user['token'], 1004, 'Roses are red')
    with pytest.raises(AccessError):
        message_send(user2['token'], channel['channel_id'], 'Violets are blue')

def test_message_send_invalid_token():
    '''
    Input:
        Invalid token

    Output:
        message_send should raise an AccessError
    '''
    clear()
    user = auth_register('bananamilk@gmail.com', 'kdaidK120m', 'Milk', 'Banana')
    channel = channels_create(user['token'], "Test_Channel", False)
    # Invalidates token by logging out
    auth_logout(user['token'])

    with pytest.raises(AccessError):
        message_send(user['token'], channel['channel_id'], 'Error detected beep beep')

def test_message_send_simple_line():
    '''
    Input:
        valid token, channel and a simple line saying 'Hello World'

    Output:
        message_send should not raise error
        channel_messages should return a {messages[0]['messages'] = 'Hello World', 0, -1}
    '''
    clear()
    user = auth_register('camprex@gmail.com', 'aidKdamc0m', 'Camp', 'Rex')
    channel = channels_create(user['token'], "Test_Channel", True)

    # Send a message and check if its in the channel
    message_send(user['token'], channel['channel_id'], "Hello World")
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "Hello World"
    assert check_message['messages'][0]['time_created'] is not None
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_send_multiple_lines():
    '''
    Input:
        valid token, channel and multiple lines by the same user in the channel

    Output:
        message_send should not raise error
        channel_messages should return the appropriate list of messages, start = 0 and end = -1
    '''
    clear()
    user = auth_register('peanutcoal@gmail.com', 'aidKdamc0m', 'Peanut', 'Coal')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages and check if its in the channel
    message_send(user['token'], channel['channel_id'], "This is the first line")
    message_send(user['token'], channel['channel_id'], "This is the second line")
    message_send(user['token'], channel['channel_id'], "This is the third line")
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][2]['message'] == "This is the first line"
    assert check_message['messages'][1]['message'] == "This is the second line"
    assert check_message['messages'][0]['message'] == "This is the third line"
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_send_multiple_users():
    '''
    Input:
        valid token, channel and 3 users sending different messages in the same channel

    Output:
        message_send should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('red@gmail.com', 'Mcansdews', 'Red', 'One')
    user2 = auth_register('red2@gmail.com', 'Msncasckw021', 'Red', 'Two')
    user3 = auth_register('red3@gmail.com', 'Kiacsnis120', 'Red', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages and check if its in the channel
    message_send(user['token'], channel['channel_id'], "I am Red One")
    message_send(user2['token'], channel['channel_id'], "I am Red Two")
    message_send(user3['token'], channel['channel_id'], "I am Red Three")
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][2]['message'] == "I am Red One"
    assert check_message['messages'][1]['message'] == "I am Red Two"
    assert check_message['messages'][0]['message'] == "I am Red Three"
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_send_multiple_channel():
    '''
    Input:
        valid token, multiple channels, single lines of word

    Output:
        message_send should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('greengiant@gmail.com', 'P0isncasmd28', 'Gian', 'Green')
    channel = channels_create(user['token'], "Test_Channel", False)
    channel2 = channels_create(user['token'], "Test_Channel2", False)
    channel3 = channels_create(user['token'], "Test_Channel3", False)

    # Send some messages
    message_send(user['token'], channel['channel_id'], "This is my first channel")
    message_send(user['token'], channel2['channel_id'], "This is my second channel")
    message_send(user['token'], channel3['channel_id'], "This is my third channel")
    # Check if its in the appropriate channel
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    check_message2 = channel_messages(user['token'], channel2['channel_id'], 0)
    check_message3 = channel_messages(user['token'], channel3['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "This is my first channel"
    assert check_message2['messages'][0]['message'] == "This is my second channel"
    assert check_message3['messages'][0]['message'] == "This is my third channel"
    # message_id check
    assert check_message['messages'][0]['message_id'] == 0
    assert check_message2['messages'][0]['message_id'] == 1
    assert check_message3['messages'][0]['message_id'] == 2

def test_message_send_spam():
    '''
    Input:
        valid token, single channel, multiple lines of same string

    Output:
        message_send should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('pineapplepizza@gmail.com', 'Kscai<W01', 'Pineapple', 'Pizzeria')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages and check if its in the channel
    message_send(user['token'], channel['channel_id'], "LOL")
    message_send(user['token'], channel['channel_id'], "LOL")
    message_send(user['token'], channel['channel_id'], "LOL")
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][2]['message'] == "LOL"
    assert check_message['messages'][1]['message'] == "LOL"
    assert check_message['messages'][0]['message'] == "LOL"
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_send_same_lines():
    '''
    Input:
        multiple tokens, single channel, same string

    Output:
        message_send should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('blue@gmail.com', 'Mcansdews', 'One', 'Blue')
    user2 = auth_register('blue2@gmail.com', 'Msncasckw021', 'Two', 'Blue')
    user3 = auth_register('blue3@gmail.com', 'Kiacsnis120', 'Three', 'Blue')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages and check if its in the channel
    message_send(user['token'], channel['channel_id'], "I am blue da ba dee")
    message_send(user2['token'], channel['channel_id'], "I am blue da ba dee")
    message_send(user3['token'], channel['channel_id'], "I am blue da ba dee")
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][2]['message'] == "I am blue da ba dee"
    assert check_message['messages'][1]['message'] == "I am blue da ba dee"
    assert check_message['messages'][0]['message'] == "I am blue da ba dee"
    assert check_message['start'] == 0
    assert check_message['end'] == -1

####################### Tests for message_remove function #####################

def test_message_remove_invalid_message():
    '''
    Input:
        Message_remove is given an invalid message_id (message_id does not exist)

    Output:
        message_remove should raise an InputError
    '''
    clear()
    user = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')

    # Try removing a nonexistent message
    with pytest.raises(InputError):
        message_remove(user['token'], 12002)

def test_message_remove_twice():
    '''
    Input:
        Message_remove is given a message_id which no longer exists due to removing it once previously

    Output:
        message_remove should raise an InputError
    '''
    clear()
    user = auth_register('jimmykelly@gmail.com', 'Meo02MnKlej', 'Jimmy', 'Kelly')
    channel = channels_create(user['token'], "Test_Channel", True)

    msg = message_send(user['token'], channel['channel_id'], "Remove me")
    message_remove(user['token'], msg['message_id'])
    # Try removing the same message again
    with pytest.raises(InputError):
        message_remove(user['token'], msg['message_id'])

def test_message_remove_unauthorised_member():
    '''
    Input:
        A token from a member (not Owner) and
        A message_id which contains a message sent by another member

    Output:
        message_remove should raise an AccessError
    '''
    clear()
    user = auth_register('red@gmail.com', 'Mcansdews', 'Red', 'One')
    user2 = auth_register('red2@gmail.com', 'Msncasckw021', 'Red', 'Two')
    user3 = auth_register('red3@gmail.com', 'Kiacsnis120', 'Red', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # user2 (member) tries to remove a message sent by user3 (member)
    msg = message_send(user3['token'], channel['channel_id'], 'Cannot Delet This!!!')
    with pytest.raises(AccessError):
        message_remove(user2['token'], msg['message_id'])

def test_message_remove_not_owner():
    '''
    Input:
        A token from a member (not Owner) and
        A message_id which contains a message sent by an owner of the channel

    Output:
        message_remove should raise an AccessError
    '''
    clear()
    user = auth_register('kangthur@gmail.com', 'Ma00ca', 'King', 'Arthur')
    user2 = auth_register('memelin@gmail.com', 'ascmsi22', 'Mage', 'Merlin')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])

    # user2 (member) tries to remove a message sent by user (owner)
    msg = message_send(user['token'], channel['channel_id'], 'You dont have the power!!!')
    with pytest.raises(AccessError):
        message_remove(user2['token'], msg['message_id'])

def test_message_remove_invalid_token():
    '''
    Input:
        Invalid token

    Output:
        message_remove should raise an AccessError
    '''
    clear()
    user = auth_register('bananamilk@gmail.com', 'kdaidK120m', 'Milk', 'Banana')
    channel = channels_create(user['token'], "Test_Channel", False)
    msg = message_send(user['token'], channel['channel_id'], 'SOS')
    # Invalidates token by logging out
    auth_logout(user['token'])

    with pytest.raises(AccessError):
        message_remove(user['token'], msg['message_id'])

def test_message_remove_single_line():
    '''
    Input:
        valid token and a message_id containing a single line saying 'Goodbye World'

    Output:
        message_remove should not raise error
        channel_messages should return a {messages[0]['messages'] = 'Hello World', 0, -1},
        after deleting the "Goodbye World" message
    '''
    clear()
    user = auth_register('camprex@gmail.com', 'aidKdamc0m', 'Camp', 'Rex')
    channel = channels_create(user['token'], "Test_Channel", True)

    # Send two messages and remove the latter
    message_send(user['token'], channel['channel_id'], "Hello World")
    msg = message_send(user['token'], channel['channel_id'], "Goodbye World")
    message_remove(user['token'], msg['message_id'])
    # Check using channel_messages
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "Hello World"
    assert check_message['start'] == 0
    assert check_message['end'] == -1
    # Check that the message list contains only 1 message
    assert len(check_message['messages']) == 1

def test_message_remove_multiple_lines():
    '''
    Input:
        valid token and multiple lines by the same user in the channel

    Output:
        message_remove should not raise error
        channel_messages should return an empty list of messages
    '''
    clear()
    user = auth_register('peanutcoal@gmail.com', 'aidKdamc0m', 'Peanut', 'Coal')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages and remove said messages
    msg = message_send(user['token'], channel['channel_id'], "This is the first line")
    msg2 =message_send(user['token'], channel['channel_id'], "This is the second line")
    msg3 = message_send(user['token'], channel['channel_id'], "This is the third line")
    message_remove(user['token'], msg['message_id'])
    message_remove(user['token'], msg2['message_id'])
    message_remove(user['token'], msg3['message_id'])
    # CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 0
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_remove_multiple_users():
    '''
    Description:
        Remove different messages by 3 different users in the same channel consecutively

    Output:
        message_remove should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('targ1@gmail.com', 'LAwksgt21', 'Target', 'One')
    user2 = auth_register('targ2@gmail.com', 'Fiasnc210', 'Target', 'Two')
    user3 = auth_register('targ3@gmail.com', 'Fibscn101', 'Target', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages and remove it consecutively
    msg = message_send(user['token'], channel['channel_id'], "I am Number ONE")
    message_remove(user['token'], msg['message_id'])
    msg2 = message_send(user2['token'], channel['channel_id'], "I am Number TWO")
    message_remove(user2['token'], msg2['message_id'])
    msg3 = message_send(user3['token'], channel['channel_id'], "I am Number THREE")
    message_remove(user3['token'], msg3['message_id'])
    # CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 0
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_remove_owner_channel():
    '''
    Input:
        Owner forcefully removes messages sent by other members in the channel

    Output:
        message_remove should not raise any errors
        check results using channel_messages
    '''
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    user2 = auth_register('carp2@gmail.com', 'kvsIWw021', 'Goldin', 'Carp')
    user3 = auth_register('carp3@gmail.com', 'Ocpaasnc20', 'Giant', 'Carp')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages and owner removes all the messages by the members
    message_send(user['token'], channel['channel_id'], "I am the one")
    msg1 = message_send(user2['token'], channel['channel_id'], "Try deleting this")
    msg2 = message_send(user3['token'], channel['channel_id'], "Can you delete this?")
    message_remove(user['token'], msg1['message_id'])
    message_remove(user['token'], msg2['message_id'])

    # Check
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "I am the one"
    assert len(check_message['messages']) == 1

def test_message_remove_multiple_channel():
    '''
    Input:
        valid token and message_id from multiple channels

    Output:
        message_remove should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('greengiant@gmail.com', 'P0isncasmd28', 'Gian', 'Green')
    channel = channels_create(user['token'], "Test_Channel", False)
    channel2 = channels_create(user['token'], "Test_Channel2", False)
    channel3 = channels_create(user['token'], "Test_Channel3", False)

    # Send some messages
    msg = message_send(user['token'], channel['channel_id'], "This is my first channel")
    msg2 = message_send(user['token'], channel2['channel_id'], "This is my second channel")
    msg3 = message_send(user['token'], channel3['channel_id'], "This is my third channel")
    # Remove ALL the messages in the other channels
    message_remove(user['token'], msg['message_id'])
    message_remove(user['token'], msg2['message_id'])
    message_remove(user['token'], msg3['message_id'])

    # CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    check_message2 = channel_messages(user['token'], channel2['channel_id'], 0)
    check_message3 = channel_messages(user['token'], channel3['channel_id'], 0)
    assert len(check_message['messages']) == 0
    assert len(check_message2['messages']) == 0
    assert len(check_message3['messages']) == 0

def test_message_remove_middle():
    '''
    Input:
        valid token and message_id of the message in the middle of the chat

    Output:
        message_remove should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('pineapplepizza@gmail.com', 'Kscai<W01', 'Pineapple', 'Pizzeria')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages and remove 'SECOND!!'
    message_send(user['token'], channel['channel_id'], "FIRST!!!")
    msg = message_send(user['token'], channel['channel_id'], "SECOND!!")
    message_send(user['token'], channel['channel_id'], "THIRD!")
    message_remove(user['token'], msg['message_id'])

    #CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 2
    assert check_message['messages'][1]['message'] == "FIRST!!!"
    assert check_message['messages'][0]['message'] == "THIRD!"

####################### Tests for message_edit function #####################

def test_message_edit_invalid_message():
    '''
    Input:
        message_edit is given an invalid message_id (message_id does not exist)

    Output:
        message_edit should raise an InputError
    '''
    clear()
    user = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')
    channels_create(user['token'], "Test_Channel", True)

    # Try editing a nonexistent message
    with pytest.raises(InputError):
        message_edit(user['token'], 12002, 'Filet Mignon')
    with pytest.raises(InputError):
        message_edit(user['token'], 1, 'Raspberry pie')
    with pytest.raises(InputError):
        message_edit(user['token'], 0, 'Rosemary')

def test_message_edit_unauthorised_member():
    '''
    Input:
        A token from a member (not Owner) and
        A message_id which contains a message sent by another member

    Output:
        message_edit should raise an AccessError
    '''
    clear()
    user = auth_register('red@gmail.com', 'Mcansdews', 'Red', 'One')
    user2 = auth_register('red2@gmail.com', 'Msncasckw021', 'Red', 'Two')
    user3 = auth_register('red3@gmail.com', 'Kiacsnis120', 'Red', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # user2 (member) tries to edit a message sent by user3 (member)
    msg = message_send(user3['token'], channel['channel_id'], 'Cannot Delet This!!!')
    with pytest.raises(AccessError):
        message_edit(user2['token'], msg['message_id'], 'This is mine now....')

def test_message_edit_not_owner():
    '''
    Input:
        A token from a member (not Owner) and
        A message_id which contains a message sent by an owner of the channel

    Output:
        message_edit should raise an AccessError
    '''
    clear()
    user = auth_register('kangthur@gmail.com', 'Ma00ca', 'King', 'Arthur')
    user2 = auth_register('memelin@gmail.com', 'ascmsi22', 'Mage', 'Merlin')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])

    # user2 (member) tries to edit a message sent by user (owner)
    msg = message_send(user['token'], channel['channel_id'], 'You dont have the power!!!')
    with pytest.raises(AccessError):
        message_edit(user2['token'], msg['message_id'], "Nooooo")

def test_message_edit_invalid_token():
    '''
    Input:
        Invalid token

    Output:
        message_edit should raise an AccessError
    '''
    clear()
    user = auth_register('bananamilk@gmail.com', 'kdaidK120m', 'Milk', 'Banana')
    channel = channels_create(user['token'], "Test_Channel", False)
    msg = message_send(user['token'], channel['channel_id'], 'Help?')
    # Invalidates token by logging out
    auth_logout(user['token'])

    with pytest.raises(AccessError):
        message_edit(user['token'], msg['message_id'], "SOS?")

def test_message_edit_simple():
    '''
    Input:
        valid token, valid message_id, 'Goodbye World'

    Output:
        message_edit should not raise error
        channel_messages is used to check returned result
    '''
    clear()
    user = auth_register('camprex@gmail.com', 'aidKdamc0m', 'Camp', 'Rex')
    channel = channels_create(user['token'], "Test_Channel", True)

    # Send a message and check
    msg = message_send(user['token'], channel['channel_id'], "Hello World")
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "Hello World"
    assert check_message['messages'][0]['message_id'] == 0
    assert len(check_message['messages']) == 1

    # Edit the message and check again
    message_edit(user['token'], msg['message_id'], 'Goodbye World')
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "Goodbye World"
    assert check_message['messages'][0]['message_id'] == 0
    assert len(check_message['messages']) == 1

def test_message_edit_multiple_lines():
    '''
    Description:
        Edits several messages sent by the same user and check the edited message

    Output:
        message_edit should not raise error
    '''
    clear()
    user = auth_register('peanutcoal@gmail.com', 'aidKdamc0m', 'Peanut', 'Coal')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages and proceeds to edit them
    msg = message_send(user['token'], channel['channel_id'], "This is the first line")
    message_edit(user['token'], msg['message_id'], 'Three')
    msg = message_send(user['token'], channel['channel_id'], "This is the second line")
    message_edit(user['token'], msg['message_id'], 'Two')
    msg = message_send(user['token'], channel['channel_id'], "This is the third line")
    message_edit(user['token'], msg['message_id'], 'One')

    # CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 3
    assert check_message['messages'][2]['message'] == 'Three'
    assert check_message['messages'][1]['message'] == 'Two'
    assert check_message['messages'][0]['message'] == 'One'

def test_message_edit_empty_strings():
    '''
    Input:
        valid token, valid message_id and an empty string ('')

    Output:
        message should be removed from the channel,
        so channel_messages should not have any messages
    '''
    clear()
    user = auth_register('Lemonly@gmail.com', 'Arcadai011', 'Lemon', 'Cola')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages and proceeds and edit the middle message with an empty string
    msg = message_send(user['token'], channel['channel_id'], "This is the first line")
    msg2 = message_send(user['token'], channel['channel_id'], "This is the second line")
    msg3 = message_send(user['token'], channel['channel_id'], "This is the third line")
    message_edit(user['token'], msg2['message_id'], '')
    # CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 2
    assert check_message['messages'][1]['message'] == 'This is the first line'
    assert check_message['messages'][0]['message'] == 'This is the third line'

    # Edit all the other messages with an empty string
    message_edit(user['token'], msg['message_id'], '')
    message_edit(user['token'], msg3['message_id'], '')
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 0
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_edit_multiple_users():
    '''
    Description:
        Edit different messages by 3 different users in the same channel consecutively

    Output:
        message_edit should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('targ1@gmail.com', 'LAwksgt21', 'Target', 'One')
    user2 = auth_register('targ2@gmail.com', 'Fiasnc210', 'Target', 'Two')
    user3 = auth_register('targ3@gmail.com', 'Fibscn101', 'Target', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages and edit it consecutively
    msg = message_send(user['token'], channel['channel_id'], "I am Number ONE")
    message_edit(user['token'], msg['message_id'], 'First?')
    msg = message_send(user2['token'], channel['channel_id'], "I am Number TWO")
    message_edit(user2['token'], msg['message_id'], 'Second?')
    msg = message_send(user3['token'], channel['channel_id'], "I am Number THREE")
    message_edit(user3['token'], msg['message_id'], 'Third?')
    # CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 3
    assert check_message['messages'][2]['message'] == 'First?'
    assert check_message['messages'][1]['message'] == 'Second?'
    assert check_message['messages'][0]['message'] == 'Third?'

def test_message_edit_owner_channel():
    '''
    Input:
        Owner forcefully edits messages sent by other members in the channel

    Output:
        message_edit should not raise any errors
        check results using channel_messages
    '''
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    user2 = auth_register('carp2@gmail.com', 'kvsIWw021', 'Goldin', 'Carp')
    user3 = auth_register('carp3@gmail.com', 'Ocpaasnc20', 'Giant', 'Carp')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages and owner edit all the messages by the members
    message_send(user['token'], channel['channel_id'], "I am the one")
    msg1 = message_send(user2['token'], channel['channel_id'], "I am the owner")
    msg2 = message_send(user3['token'], channel['channel_id'], "Clearly I am the owner")
    message_edit(user['token'], msg1['message_id'], '[Message Redacted]')
    message_edit(user['token'], msg2['message_id'], '[Message Redacted]')

    #CHECK
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert len(check_message['messages']) == 3
    assert check_message['messages'][2]['message'] == "I am the one"
    assert check_message['messages'][1]['message'] == "[Message Redacted]"
    assert check_message['messages'][0]['message'] == "[Message Redacted]"

####################### Tests for message_sendlater function #####################
def test_message_sendlater_inexistent_channel():
    '''
    Input:
        A channel_id that does not exist in the system (invalid channel_id)
    Output:
        message_sendlater should raise an InputError if channel does not exist
    '''
    clear()
    user = auth_register('canoeboon@gmail.com', 'Moenal02MnKlej', 'Canoe', 'Boon')
    user2 = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')

    cur_time = int(time.time())
    with pytest.raises(InputError):
        message_sendlater(user['token'], 1004, 'Roses are red', cur_time)
    with pytest.raises(InputError):
        message_sendlater(user2['token'], 202, 'Violets are blue', cur_time)

def test_message_sendlater_invalid_message_length():
    '''
    Input:
        Message_sendlater is given an invalid message
        (length of characters > 1000 and length of characters == 0)
    Output:
        message_sendlater should raise an InputError
    '''
    clear()
    invalid_msg = 'a' * 1001
    user = auth_register('bluerex@gmail.com', 'kaneKlej', 'Blue', 'Rex')
    channel = channels_create(user['token'], "Test_Channel", True)

    cur_time = int(time.time())
    with pytest.raises(InputError):
        message_sendlater(user['token'], channel['channel_id'], invalid_msg, cur_time)
    with pytest.raises(InputError):
        message_sendlater(user['token'], channel['channel_id'], '', cur_time)

def test_message_sendlater_invalid_time():
    '''
    Input:
        Invalid time_sent (time is in the past)
    Output:
        message_sendlater should raise an InputError
    '''
    clear()
    user = auth_register('canoeboon@gmail.com', 'Moenal02MnKlej', 'Canoe', 'Boon')
    channel = channels_create(user['token'], "Test_Channel", False)

    cur_time = int(time.time())
    # This is the utc timestamp for Thu Dec 27 15:49:29 2018
    invalid_time = 1545925769.9618232

    with pytest.raises(InputError):
        message_sendlater(user['token'], channel['channel_id'], 'Let me in!!!', cur_time - 10)
    with pytest.raises(InputError):
        message_sendlater(user['token'], channel['channel_id'], 'Let me in!!!', cur_time - 100)
    with pytest.raises(InputError):
        message_sendlater(user['token'], channel['channel_id'], 'Let me in!!!', invalid_time)

def test_message_sendlater_not_channel_member():
    '''
    Input:
        A channel_id that the user is not a part of
    Output:
        message_sendlater should raise an AccessError if user is not member of the channel
    '''
    clear()
    user = auth_register('canoeboon@gmail.com', 'Moenal02MnKlej', 'Canoe', 'Boon')
    user2 = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')
    channel = channels_create(user['token'], "Test_Channel", False)

    cur_time = int(time.time())
    with pytest.raises(AccessError):
        message_sendlater(user2['token'], channel['channel_id'], 'Let me in!!!', cur_time)

def test_message_sendlater_invalid_token():
    '''
    Input:
        Invalid token
    Output:
        message_sendlater should raise an AccessError
    '''
    clear()
    user = auth_register('bananamilk@gmail.com', 'kdaidK120m', 'Milk', 'Banana')
    channel = channels_create(user['token'], "Test_Channel", False)
    # Invalidates token by logging out
    auth_logout(user['token'])

    cur_time = int(time.time())
    with pytest.raises(AccessError):
        message_sendlater(user['token'], channel['channel_id'], 'Error', cur_time)

### Success cases ###
def test_message_sendlater_simple_line():
    '''
    Input:
        valid token, channel and a simple line saying 'Hello World'
    Output:
        message_sendlater should not raise error
        channel_messages should return a messages[0]['messages'] = 'Hello World'
        after 3 seconds
    '''
    clear()
    user = auth_register('camprex@gmail.com', 'aidKdamc0m', 'Camp', 'Rex')
    channel = channels_create(user['token'], "Test_Channel", True)

    # Send a message 3 seconds later after current time
    next_time = int(time.time()) + 3
    message_sendlater(user['token'], channel['channel_id'], "Hello World", next_time)

    # Check the message after 3.5 seconds have passed
    time.sleep(3.5)
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message_id'] == 0
    assert check_message['messages'][0]['message'] == "Hello World"
    assert check_message['messages'][0]['time_created'] == next_time
    assert check_message['start'] == 0
    assert check_message['end'] == -1

def test_message_sendlater_multiple_lines():
    '''
    Input:
        valid token, channel and multiple lines by the same user in the channel
    Output:
        message_sendlater should not raise error
        channel_messages should return the appropriate list of messages
    '''
    clear()
    user = auth_register('peanutcoal@gmail.com', 'aidKdamc0m', 'Peanut', 'Coal')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages
    # message_id should be in the order message_sendlater is called
    cur_time = int(time.time())
    msg1 = message_sendlater(user['token'], channel['channel_id'], "This is the second line", cur_time + 2)
    msg2 = message_sendlater(user['token'], channel['channel_id'], "This is the third line", cur_time + 3)
    msg3 = message_sendlater(user['token'], channel['channel_id'], "This is the first line", cur_time + 1)
    assert msg1['message_id'] == 0
    assert msg2['message_id'] == 1
    assert msg3['message_id'] == 2

    # Check messages after 4 seconds
    time.sleep(4)
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][2]['message'] == "This is the first line"
    assert check_message['messages'][1]['message'] == "This is the second line"
    assert check_message['messages'][0]['message'] == "This is the third line"
    assert check_message['messages'][2]['time_created'] == cur_time + 1
    assert check_message['messages'][1]['time_created'] == cur_time + 2
    assert check_message['messages'][0]['time_created'] == cur_time + 3

def test_message_sendlater_multiple_users():
    '''
    Input:
        valid token, channel and 3 users sending different messages in the same channel
    Output:
        message_sendlater should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('red@gmail.com', 'Mcansdews', 'Red', 'One')
    user2 = auth_register('red2@gmail.com', 'Msncasckw021', 'Red', 'Two')
    user3 = auth_register('red3@gmail.com', 'Kiacsnis120', 'Red', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send some messages in the future
    cur_time = int(time.time())
    message_sendlater(user['token'], channel['channel_id'], "I am Red One", cur_time + 1)
    message_sendlater(user2['token'], channel['channel_id'], "I am Red Two", cur_time + 2)
    message_sendlater(user3['token'], channel['channel_id'], "I am Red Three", cur_time + 3)

    time.sleep(3.5)
    # Check messages after 3.5 seconds
    # will not work if its set to 3 seconds
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][2]['message'] == "I am Red One"
    assert check_message['messages'][1]['message'] == "I am Red Two"
    assert check_message['messages'][0]['message'] == "I am Red Three"
    assert check_message['messages'][2]['time_created'] == cur_time + 1
    assert check_message['messages'][1]['time_created'] == cur_time + 2
    assert check_message['messages'][0]['time_created'] == cur_time + 3

def test_message_sendlater_multiple_channel():
    '''
    Input:
        valid token, multiple channels, single lines of word
    Output:
        message_sendlater should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('greengiant@gmail.com', 'P0isncasmd28', 'Gian', 'Green')
    channel = channels_create(user['token'], "Test_Channel", False)
    channel2 = channels_create(user['token'], "Test_Channel2", False)
    channel3 = channels_create(user['token'], "Test_Channel3", False)

    # Send some messages later in the channel
    cur_time = int(time.time())
    message_sendlater(user['token'], channel['channel_id'], "This is my first channel", cur_time)
    message_sendlater(user['token'], channel2['channel_id'], "This is my second channel", cur_time + 1)
    message_sendlater(user['token'], channel3['channel_id'], "This is my third channel", cur_time)

    # Check if its in the appropriate channel after 1 second
    time.sleep(1.5)
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    check_message2 = channel_messages(user['token'], channel2['channel_id'], 0)
    check_message3 = channel_messages(user['token'], channel3['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "This is my first channel"
    assert check_message2['messages'][0]['message'] == "This is my second channel"
    assert check_message3['messages'][0]['message'] == "This is my third channel"
    assert check_message['messages'][0]['message_id'] == 0
    assert check_message2['messages'][0]['message_id'] == 1
    assert check_message3['messages'][0]['message_id'] == 2
    assert check_message['messages'][0]['time_created'] == cur_time
    assert check_message2['messages'][0]['time_created'] == cur_time + 1
    assert check_message3['messages'][0]['time_created'] == cur_time

def test_message_sendlater_multiple_same_time():
    '''
    Input:
        valid token, multiple channels, multiple lines of word sent on the same time
    Output:
        message_sendlater should not raise error
        check results using channel_messages
    '''
    clear()
    user = auth_register('peanutcoal@gmail.com', 'aidKdamc0m', 'Peanut', 'Coal')
    channel = channels_create(user['token'], "Test_Channel", False)

    # Send some messages with the same time
    same_time = int(time.time()) + 1
    msg1 = message_sendlater(user['token'], channel['channel_id'], "This is the first line", same_time)
    msg2 = message_sendlater(user['token'], channel['channel_id'], "This is the second line", same_time)
    msg3 = message_sendlater(user['token'], channel['channel_id'], "This is the third line", same_time)

    # Check
    time.sleep(3)
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][2]['message'] == "This is the first line"
    assert check_message['messages'][1]['message'] == "This is the second line"
    assert check_message['messages'][0]['message'] == "This is the third line"
    assert check_message['messages'][2]['time_created'] == same_time
    assert check_message['messages'][1]['time_created'] == same_time
    assert check_message['messages'][0]['time_created'] == same_time
    assert msg1['message_id'] == 0
    assert msg2['message_id'] == 1
    assert msg3['message_id'] == 2

####################### Tests for message_react function #####################
def test_message_react_invalid_token():
    '''
    Input:
        Invalid token
    Output:
        message_react should raise an AccessError
    '''
    clear()
    user = auth_register('bananamilk@gmail.com', 'kdaidK120m', 'Milk', 'Banana')
    channel = channels_create(user['token'], "Test_Channel", False)
    msg = message_send(user['token'], channel['channel_id'], 'SOS')
    # Invalidates token by logging out
    auth_logout(user['token'])

    with pytest.raises(AccessError):
        message_react(user['token'], msg['message_id'], 1)

def test_message_react_invalid_message_id():
    '''
    Input:
        message_react is given an invalid message_id (message_id does not exist)
    Output:
        message_react should raise an InputError
    '''
    clear()
    user = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')
    channels_create(user['token'], "Test_Channel", False)
    # Try reacting to an inexistent message_id
    with pytest.raises(InputError):
        message_react(user['token'], 12002, 1)

def test_message_react_user_not_in_channel():
    '''
    Input:
        message_react is given a message_id in a channel
        that the user is not part of
    Output:
        message_react should raise an InputError
    '''
    clear()
    user = auth_register('red@gmail.com', 'Mcansdews', 'Red', 'One')
    user2 = auth_register('red2@gmail.com', 'Msncasckw021', 'Red', 'Two')
    user3 = auth_register('red3@gmail.com', 'Kiacsnis120', 'Red', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])

    msg = message_send(user['token'], channel['channel_id'], 'First sentence!!')
    msg2 = message_send(user2['token'], channel['channel_id'], 'Second sentence!!')

    # msg_react should raise InputError when user3 which is not a member tries to react
    with pytest.raises(InputError):
        message_react(user3['token'], msg['message_id'], 1)
    with pytest.raises(InputError):
        message_react(user3['token'], msg2['message_id'], 1)

def test_message_react_invalid_react_id():
    '''
    Input:
        message_react is given a invalid react_id
    Output:
        message_react should raise an InputError
    '''
    clear()
    user = auth_register('camprex@gmail.com', 'aidKdamc0m', 'Camp', 'Rex')
    channel = channels_create(user['token'], "Test_Channel", True)
    # Send a message
    msg = message_send(user['token'], channel['channel_id'], "Hello World")

    with pytest.raises(InputError):
        message_react(user['token'], msg['message_id'], 101)
    with pytest.raises(InputError):
        message_react(user['token'], msg['message_id'], 911)

def test_message_react_twice():
    '''
    Input:
        message_react is a given a message_id which have been reacted previously
    Output:
        message_react should raise an InputError
    '''
    clear()
    user = auth_register('jimmykelly@gmail.com', 'Meo02MnKlej', 'Jimmy', 'Kelly')
    channel = channels_create(user['token'], "Test_Channel", True)

    msg = message_send(user['token'], channel['channel_id'], "XD")
    message_react(user['token'], msg['message_id'], 1)
    # Try reacting to the message again
    with pytest.raises(InputError):
        message_react(user['token'], msg['message_id'], 1)

def test_message_react_simple():
    '''
    Input:
        message_react tries to react to own message
    Output:
        no error should be raised, checking is done using channel_messages
    '''
    clear()
    user = auth_register('dumlapis@gmail.com', 'ksiw01m', 'Dum', 'Lapis')
    channel = channels_create(user['token'], "Test_Channel", True)

    # Send a message and react
    msg = message_send(user['token'], channel['channel_id'], "Hippity Hoppity")
    message_react(user['token'], msg['message_id'], 1)

    # Check using channel_messages
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "Hippity Hoppity"
    assert check_message['messages'][0]['reacts'][0]['react_id'] == 1
    assert check_message['messages'][0]['reacts'][0]['u_ids'][0] == user['u_id']
    assert check_message['messages'][0]['reacts'][0]['is_this_user_reacted'] == True
    # Check that the message list contains only 1 message
    assert len(check_message['messages']) == 1

def test_message_react_multiple_users():
    '''
    Input:
        message_react tries to react to messages sent by others
    Output:
        no error should be raised, checking is done using channel_messages
    '''
    clear()
    user = auth_register('targ1@gmail.com', 'LAwksgt21', 'Target', 'One')
    user2 = auth_register('targ2@gmail.com', 'Fiasnc210', 'Target', 'Two')
    user3 = auth_register('targ3@gmail.com', 'Fibscn101', 'Target', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send a message and other users react to it
    msg = message_send(user['token'], channel['channel_id'], "First!!!")
    message_react(user2['token'], msg['message_id'], 1)
    message_react(user3['token'], msg['message_id'], 1)

    # Check
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "First!!!"
    assert check_message['messages'][0]['reacts'][0]['react_id'] == 1
    assert check_message['messages'][0]['reacts'][0]['u_ids'][0] == user2['u_id']
    assert check_message['messages'][0]['reacts'][0]['is_this_user_reacted'] == False
    assert check_message['messages'][0]['reacts'][0]['react_id'] == 1
    assert check_message['messages'][0]['reacts'][0]['u_ids'][1] == user3['u_id']
    assert check_message['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

    # Sender reacts (user) to the message and check
    message_react(user['token'], msg['message_id'], 1)
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['reacts'][0]['react_id'] == 1
    assert check_message['messages'][0]['reacts'][0]['u_ids'][2] == user['u_id']
    assert check_message['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

####################### Tests for message_unreact function #####################
def test_message_unreact_invalid_token():
    '''
    Input:
        Invalid token
    Output:
        message_unreact should raise an AccessError
    '''
    clear()
    user = auth_register('bananamilk@gmail.com', 'kdaidK120m', 'Milk', 'Banana')
    channel = channels_create(user['token'], "Test_Channel", False)
    msg = message_send(user['token'], channel['channel_id'], 'SOS')
    # Invalidates token by logging out
    auth_logout(user['token'])

    with pytest.raises(AccessError):
        message_unreact(user['token'], msg['message_id'], 1)

def test_message_unreact_invalid_message_id():
    '''
    Input:
        message_unreact is given an invalid message_id (message_id does not exist)
    Output:
        message_unreact should raise an InputError
    '''
    clear()
    user = auth_register('jimmykenny@gmail.com', 'Gao02MnKlej', 'Jimmy', 'Kenny')
    channels_create(user['token'], "Test_Channel", False)
    # Try reacting to an inexistent message_id
    with pytest.raises(InputError):
        message_unreact(user['token'], 12002, 1)

def test_message_unreact_user_not_in_channel():
    '''
    Input:
        message_unreact is given a message_id in a channel
        that the user is not part of
    Output:
        message_unreact should raise an InputError
    '''
    clear()
    user = auth_register('red@gmail.com', 'Mcansdews', 'Red', 'One')
    user2 = auth_register('red2@gmail.com', 'Msncasckw021', 'Red', 'Two')
    user3 = auth_register('red3@gmail.com', 'Kiacsnis120', 'Red', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])

    msg = message_send(user['token'], channel['channel_id'], 'First sentence!!')
    msg2 = message_send(user2['token'], channel['channel_id'], 'Second sentence!!')

    # msg_react should raise InputError when user3 which is not a member tries to react
    with pytest.raises(InputError):
        message_unreact(user3['token'], msg['message_id'], 1)
    with pytest.raises(InputError):
        message_unreact(user3['token'], msg2['message_id'], 1)

def test_message_unreact_invalid_react_id():
    '''
    Input:
        message_unreact is given a invalid react_id
    Output:
        message_unreact should raise an InputError
    '''
    clear()
    user = auth_register('camprex@gmail.com', 'aidKdamc0m', 'Camp', 'Rex')
    channel = channels_create(user['token'], "Test_Channel", True)
    # Send a message
    msg = message_send(user['token'], channel['channel_id'], "Hello World")

    with pytest.raises(InputError):
        message_unreact(user['token'], msg['message_id'], 101)
    with pytest.raises(InputError):
        message_unreact(user['token'], msg['message_id'], 911)

def test_message_unreact_inexistent_react():
    '''
    Input:
        message_unreact is a given a message_id which has not been reacted to
    Output:
        message_unreact should raise an InputError
    '''
    clear()
    user = auth_register('jimmykelly@gmail.com', 'Meo02MnKlej', 'Jimmy', 'Kelly')
    channel = channels_create(user['token'], "Test_Channel", True)

    msg = message_send(user['token'], channel['channel_id'], "Potat")
    # Unreact directly
    with pytest.raises(InputError):
        message_unreact(user['token'], msg['message_id'], 1)

def test_message_unreact_simple():
    '''
    Input:
        message_unreact tries to unreact to own message
    Output:
        no error should be raised, checking is done using channel_messages
    '''
    clear()
    user = auth_register('dumlapis@gmail.com', 'ksiw01m', 'Dum', 'Lapis')
    channel = channels_create(user['token'], "Test_Channel", True)

    # Send a message, react, then unreact
    msg = message_send(user['token'], channel['channel_id'], "Hippity Hoppity")
    message_react(user['token'], msg['message_id'], 1)
    message_unreact(user['token'], msg['message_id'], 1)

    # Check using channel_messages
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "Hippity Hoppity"
    # Check that the message list contains only 1 message
    assert len(check_message['messages']) == 1
    # Check that the list react contains nothing
    assert len(check_message['messages'][0]['reacts']) == 0

def test_message_unreact_multiple_users():
    '''
    Input:
        message_unreact tries to unreact to messages sent by others
    Output:
        no error should be raised, checking is done using channel_messages
    '''
    clear()
    user = auth_register('targ1@gmail.com', 'LAwksgt21', 'Target', 'One')
    user2 = auth_register('targ2@gmail.com', 'Fiasnc210', 'Target', 'Two')
    user3 = auth_register('targ3@gmail.com', 'Fibscn101', 'Target', 'Three')
    # Create and join the channel
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    channel_join(user3['token'], channel['channel_id'])

    # Send a message and other users react to it
    msg = message_send(user['token'], channel['channel_id'], "First!!!")
    message_react(user2['token'], msg['message_id'], 1)
    message_react(user3['token'], msg['message_id'], 1)
    message_unreact(user2['token'], msg['message_id'], 1)

    # Check
    check_message = channel_messages(user['token'], channel['channel_id'], 0)
    assert check_message['messages'][0]['message'] == "First!!!"
    assert check_message['messages'][0]['reacts'][0]['react_id'] == 1
    assert len(check_message['messages'][0]['reacts'][0]['u_ids']) == 1
    assert check_message['messages'][0]['reacts'][0]['u_ids'][0] == user3['u_id']
    assert check_message['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

####################### Tests for message_pin function #####################

# tries to pin a message that dosnt exist
def test_message_pin_not_valid_message():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channels_create(user['token'], "Test_Channel", True)
    with pytest.raises(InputError):
        message_pin(user['token'], 65)

# tries to pin a message that is already pinned
def test_message_pin_already_pinned():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    msg = message_send(user['token'], channel['channel_id'], "I am the one")
    message_pin(user['token'], msg['message_id'])
    with pytest.raises(InputError):
        message_pin(user['token'], msg['message_id'])

# user who isnt in the channel tries to pin the message
def test_message_pin_not_a_member_of_channel():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    user2 = auth_register('carp2@gmail.com', 'kvsIWw021', 'Goldin', 'Carp')
    channel = channels_create(user2['token'], "Test_Channel", True)
    msg = message_send(user2['token'], channel['channel_id'], "I am the one")
    with pytest.raises(AccessError):
        message_pin(user['token'], msg['message_id'])

# user isnt an owner
def test_message_pin_not_an_owner():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    user2 = auth_register('carp2@gmail.com', 'kvsIWw021', 'Goldin', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    msg = message_send(user2['token'], channel['channel_id'], "I am the one")
    with pytest.raises(AccessError):
        message_pin(user2['token'], msg['message_id'])


# success case
def test_message_pin_successful():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    msg = message_send(user['token'], channel['channel_id'], "I am the one")
    message_pin(user['token'], msg['message_id'])
    messages = channel_messages(user['token'], channel['channel_id'], 0)
    assert messages["messages"][msg['message_id']]["is_pinned"] == True


####################### Tests for message_unpin function #####################

# tries to unpin a message that dosnt exist
def test_message_unpin_not_valid_message():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    msg = message_send(user['token'], channel['channel_id'], "I am the one")
    message_pin(user['token'], msg['message_id'])
    with pytest.raises(InputError):
        message_unpin(user['token'], 65)

# tries to unpin a message that isnt pinned
def test_message_unpin_already_unpinned():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    msg = message_send(user['token'], channel['channel_id'], "I am the one")
    with pytest.raises(InputError):
        message_unpin(user['token'], msg['message_id'])

# user who isnt in the channel tries to unpin the message
def test_message_unpin_not_a_member_of_channel():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    user2 = auth_register('carp2@gmail.com', 'kvsIWw021', 'Goldin', 'Carp')
    channel = channels_create(user2['token'], "Test_Channel", True)
    msg = message_send(user2['token'], channel['channel_id'], "I am the one")
    message_pin(user2['token'], msg['message_id'])
    with pytest.raises(AccessError):
        message_unpin(user['token'], msg['message_id'])

# user isnt an owner
def test_message_unpin_not_an_owner():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    user2 = auth_register('carp2@gmail.com', 'kvsIWw021', 'Goldin', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    channel_join(user2['token'], channel['channel_id'])
    msg = message_send(user2['token'], channel['channel_id'], "I am the one")
    message_pin(user['token'], msg['message_id'])
    with pytest.raises(AccessError):
        message_unpin(user2['token'], msg['message_id'])

# success case
def test_message_unpin_successful():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    msg = message_send(user['token'], channel['channel_id'], "I am the one")
    message_pin(user['token'], msg['message_id'])
    messages = channel_messages(user['token'], channel['channel_id'], 0)
    assert messages["messages"][msg['message_id']]["is_pinned"] == True
    message_unpin(user['token'], msg['message_id'])
    messages = channel_messages(user['token'], channel['channel_id'], 0)
    assert messages["messages"][msg['message_id']]["is_pinned"] == False

####################### Tests for hangman #####################
def test_hangman_win_test():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    message_send(user['token'], channel['channel_id'], "/hangman start")
    assert data.channels[channel['channel_id']].hangman.get_details()['word'] is not None
    assert data.channels[channel['channel_id']].hangman.get_details()['mode'] == True
    assert data.channels[channel['channel_id']].hangman.get_details()['guesses'] == []

    data.channels[channel['channel_id']].hangman.word = "potato"

    message_send(user['token'], channel['channel_id'], "/guess a")
    message_send(user['token'], channel['channel_id'], "/guess x")
    message_send(user['token'], channel['channel_id'], "/guess t")
    message_send(user['token'], channel['channel_id'], "/guess o")
    message_send(user['token'], channel['channel_id'], "/guess s")
    message_send(user['token'], channel['channel_id'], "/guess p")

    assert data.channels[channel['channel_id']].hangman.get_details()['mode'] == False
    assert data.channels[channel['channel_id']].hangman.get_details()['guesses'] == ["a", "x", "t", "o", "s", "p"]

def test_hangman_lose():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    message_send(user['token'], channel['channel_id'], "/hangman start")
    assert data.channels[channel['channel_id']].hangman.get_details()['word'] is not None
    assert data.channels[channel['channel_id']].hangman.get_details()['mode'] == True
    assert data.channels[channel['channel_id']].hangman.get_details()['guesses'] == []

    data.channels[channel['channel_id']].hangman.word = "potato"

    message_send(user['token'], channel['channel_id'], "/guess 0")
    message_send(user['token'], channel['channel_id'], "/guess")

    message_send(user['token'], channel['channel_id'], "/guess z")
    message_send(user['token'], channel['channel_id'], "/guess x")
    message_send(user['token'], channel['channel_id'], "/guess c")
    message_send(user['token'], channel['channel_id'], "/guess l")
    message_send(user['token'], channel['channel_id'], "/guess s")
    message_send(user['token'], channel['channel_id'], "/guess j")
    message_send(user['token'], channel['channel_id'], "/guess r")
    message_send(user['token'], channel['channel_id'], "/guess k")
    message_send(user['token'], channel['channel_id'], "/guess e")
    message_send(user['token'], channel['channel_id'], "/guess b")

    assert data.channels[channel['channel_id']].hangman.get_details()['mode'] == False
    assert data.channels[channel['channel_id']].hangman.get_details()['guesses'] == ["z", "x", "c", "l", "s", "j", "r", "k", "e", "b"]

def test_no_definition():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    message_send(user['token'], channel['channel_id'], "/hangman start")

    data.channels[channel['channel_id']].hangman.word = "tpo"
    message_send(user['token'], channel['channel_id'], "/guess t")
    message_send(user['token'], channel['channel_id'], "/guess p")
    message_send(user['token'], channel['channel_id'], "/guess o")
 
def test_no_definition_hangman_lose():
    clear()
    user = auth_register('carp1@gmail.com', 'Mcansdew21s', 'Magick', 'Carp')
    channel = channels_create(user['token'], "Test_Channel", True)
    message_send(user['token'], channel['channel_id'], "/hangman start")
    assert data.channels[channel['channel_id']].hangman.get_details()['word'] is not None
    assert data.channels[channel['channel_id']].hangman.get_details()['mode'] == True
    assert data.channels[channel['channel_id']].hangman.get_details()['guesses'] == []

    data.channels[channel['channel_id']].hangman.word = "tpo"

    message_send(user['token'], channel['channel_id'], "/guess 0")
    message_send(user['token'], channel['channel_id'], "/guess")

    message_send(user['token'], channel['channel_id'], "/guess z")
    message_send(user['token'], channel['channel_id'], "/guess x")
    message_send(user['token'], channel['channel_id'], "/guess c")
    message_send(user['token'], channel['channel_id'], "/guess l")
    message_send(user['token'], channel['channel_id'], "/guess s")
    message_send(user['token'], channel['channel_id'], "/guess j")
    message_send(user['token'], channel['channel_id'], "/guess r")
    message_send(user['token'], channel['channel_id'], "/guess k")
    message_send(user['token'], channel['channel_id'], "/guess e")
    message_send(user['token'], channel['channel_id'], "/guess b")
