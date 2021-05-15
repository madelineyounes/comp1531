""" tests for channels.py file """

import pytest
from other import clear
from error import InputError, AccessError
from channels import channels_create, channels_list, channels_listall
from channel import channel_invite
from auth import auth_register
from data import data

####################### Tests for channels_list function #####################
### Testing that given invalid inputs an InputError is generated ###
# Empty Input
def test_channels_list_empty_input():
    clear()
    with pytest.raises(InputError):
        channels_list('')

# Input into token is not a string
def test_channels_list_invalid_type_input():
    clear()
    # Invalid integer input
    with pytest.raises(AccessError):
        channels_list(128737)

    # Invalid float input
    with pytest.raises(AccessError):
        channels_list(54.32)

    # Invalid complex input
    with pytest.raises(AccessError):
        channels_list(1j)

    # Invalid Boolean input
    with pytest.raises(AccessError):
        channels_list(True)

    # Invalid list input
    with pytest.raises(AccessError):
        channels_list(["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(AccessError):
        channels_list(("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(AccessError):
        channels_list({"name" : "Takko", "age" : 32})

# Input token is unauthenticated and so is invalid
def test_channels_list_invalid_token():
    clear()
    with pytest.raises(AccessError):
        channels_list("badtoken")

### Test that given valid inputs channels_list returns valid outputs ###
# Test that when the user is not in any channels channels_list returns an empty
# channel list
def test_channels_list_output_nochannels():
    clear()
    user = auth_register("names@gmail.com", 'DZVznKzzuPnjc', 'Alexie', 'Evie-Mae')
    output = channels_list(user['token'])
    assert output is not None
    assert output['channels'] is not None
    assert output['channels'] == []

# Test that when the user is in channels, channels_list returns an channel list
# with contents of 'channel_id' and 'name'
def test_channels_list_output_channels():
    clear()
    user = auth_register("potatose@gmail.com", 'tubatrumpet3', 'Jezz', 'Basso')
    channels_create(user['token'], "amezons", True)

    output = channels_list(user['token'])
    assert output is not None
    assert output['channels'] is not None

    assert output['channels'][0]['channel_id'] is not None
    assert isinstance(output['channels'][0]['channel_id'], int)

    assert output['channels'][0]['name'] is not None
    assert isinstance(output['channels'][0]['name'], str)

# Test that all the channels that the user in are listed
def test_channels_list_functionality():
    clear()
    user1 = auth_register("brunchisameal@iinet.net", 'N*B@C*N1@5', 'Britney', 'Bakon')
    user2 = auth_register("email@email.com", 'OewewrI', 'Angel', 'Kit')

    channel_id1 = channels_create(user1['token'], "channel1", True)
    channel_id2 = channels_create(user1['token'], "channel2", False)
    channel_id3 = channels_create(user1['token'], "channel3", False)
    channel_id4 = channels_create(user1['token'], "channel4", True)

    channel_invite(user1['token'], channel_id1['channel_id'], user2['u_id'])
    channel_invite(user1['token'], channel_id2['channel_id'], user2['u_id'])
    channel_invite(user1['token'], channel_id3['channel_id'], user2['u_id'])
    channel_invite(user1['token'], channel_id4['channel_id'], user2['u_id'])

    output = channels_list(user2['token'])

    check_list = [channel['channel_id'] for channel in output['channels']]
    expected_output = [channel_id1['channel_id'], channel_id2['channel_id'], channel_id3['channel_id'], channel_id4['channel_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output


####################### Tests for channels_listall function #####################
### Testing that given invalid inputs an InputError is generated ###
# Empty Input
def test_channels__listall_empty_input():
    clear()
    with pytest.raises(InputError):
        channels_listall('')

# Input into token is not a string
def test_channels__listall_invalid_type_input():
    clear()
    # Invalid integer input
    with pytest.raises(AccessError):
        channels_listall(128737)

    # Invalid float input
    with pytest.raises(AccessError):
        channels_listall(54.32)

    # Invalid complex input
    with pytest.raises(AccessError):
        channels_listall(1j)

    # Invalid Boolean input
    with pytest.raises(AccessError):
        channels_listall(True)

    # Invalid list input
    with pytest.raises(AccessError):
        channels_listall(["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(AccessError):
        channels_listall(("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(AccessError):
        channels_listall({"name" : "Takko", "age" : 32})

### Test that given valid inputs channels_listall returns valid outputs ###
# Test that given valid inputs a channels dictionary is returned
def test_channels_listall_output_channels():
    clear()
    user = auth_register("hobgoblin@optus.com", 'magic&g@LDSS!!!', 'Henrietta', 'Mackantosh')
    output = channels_create(user['token'], "HOBGoblinsAnon", True)

    output = channels_listall(user['token'])
    assert output is not None
    assert output['channels'] is not None
    assert output['channels'][0]['channel_id'] is not None
    assert isinstance(output['channels'][0]['channel_id'], int)

    assert output['channels'][0]['name'] is not None
    assert isinstance(output['channels'][0]['name'], str)

# Test that all the channels are listed
def test_channels_listall_functionality():
    clear()
    user1 = auth_register("EBronte@hotmail.com", '@JR4slkdN', 'Edgar', 'Bronte')
    user2 = auth_register("Kahlil@thepoets.com", 'D3@d@uthors', 'Kahlil', 'Gibran')
    user3 = auth_register("FranMaroun@theInternet.com", 'Intj3234*)2nkB', 'Francessa', 'Maroun')


    channel_id1 = channels_create(user1['token'], "channel1", True)
    channel_id2 = channels_create(user1['token'], "channel2", False)
    channel_id3 = channels_create(user2['token'], "channel3", False)
    channel_id4 = channels_create(user2['token'], "channel4", True)

    channel_invite(user1['token'], channel_id1['channel_id'], user2['u_id'])
    channel_invite(user1['token'], channel_id2['channel_id'], user3['u_id'])
    channel_invite(user2['token'], channel_id3['channel_id'], user1['u_id'])
    channel_invite(user2['token'], channel_id4['channel_id'], user3['u_id'])

    output = channels_list(user1['token'])

    check_list = [channel['channel_id'] for channel in output['channels']]
    expected_output = [channel_id1['channel_id'], channel_id2['channel_id'], channel_id3['channel_id'], channel_id4['channel_id']]
    assert check_list.sort() == expected_output.sort()

####################### Tests for channels_create function #####################
# Testing that given invalid inputs an InputError is generated
# Empty Inputs
def test_channels_create_empty_inputs():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    with pytest.raises(InputError):
        channels_create('', '', '')

    with pytest.raises(InputError):
        channels_create(user['token'], '', '')

    with pytest.raises(InputError):
        channels_create('', 'valid_name', '')

    with pytest.raises(InputError):
        channels_create('', '', True)

    with pytest.raises(InputError):
        channels_create('', 'valid_name', False)

    with pytest.raises(InputError):
        channels_create(user['token'], '', False)

# Non Boolean input into is_public
def test_channels_create_invalid_type_is_public():
    clear()
    user = auth_register('KingPrincess@girlred.com', '8*^(Hsjhfbsk', 'Julie', 'Nightgale')
    # Invalid string input
    with pytest.raises(InputError):
        channels_create(user['token'], 'goodname1', 'string')

    # Invalid integer input
    with pytest.raises(InputError):
        channels_create(user['token'], 'goodname2', 128737)

    # Invalid float input
    with pytest.raises(InputError):
        channels_create(user['token'], 'goodname3', 54.32)

    # Invalid complex input
    with pytest.raises(InputError):
        channels_create(user['token'], 'goodname4', 1j)

    # Invalid list input
    with pytest.raises(InputError):
        channels_create(user['token'], 'goodname5', ["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(InputError):
        channels_create(user['token'], 'goodname6', ("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(InputError):
        channels_create(user['token'], 'goodname7', {"name" : "Takko", "age" : 32})

# Input into name is not a string
def test_channels_create_invalid_type_name():
    clear()
    user = auth_register('genericemail@boringbois.com', 'BORED@fmakingT3$ts', 'Timmy', 'Iago')
    # Invalid integer input
    with pytest.raises(InputError):
        channels_create(user['token'], 128737, True)

    # Invalid float input
    with pytest.raises(InputError):
        channels_create(user['token'], 54.32, False)

    # Invalid complex input
    with pytest.raises(InputError):
        channels_create(user['token'], 1j, True)

    # Invalid Boolean input
    with pytest.raises(InputError):
        channels_create(user['token'], True, False)

    # Invalid list input
    with pytest.raises(InputError):
        channels_create(user['token'], ["apple", "banana", "cherry"], False)

    # Invalid tulpe input
    with pytest.raises(InputError):
        channels_create(user['token'], ("apple", "banana", "cherry"), True)

    # Invalid dictionary input
    with pytest.raises(InputError):
        channels_create(user['token'], {"name" : "Takko", "age" : 32}, False)

# Input into token is not a string
def test_channels_create_invalid_type_token():
    clear()
    # Invalid integer input
    with pytest.raises(AccessError):
        channels_create(128737, 'goodname1', True)

    # Invalid float input
    with pytest.raises(AccessError):
        channels_create(54.32, 'goodname2', False)

    # Invalid complex input
    with pytest.raises(AccessError):
        channels_create(1j, 'goodname3', True)

    # Invalid Boolean input
    with pytest.raises(AccessError):
        channels_create(True, 'goodname4', False)

    # Invalid list input
    with pytest.raises(AccessError):
        channels_create(["apple", "banana", "cherry"], 'goodname5', False)

    # Invalid tulpe input
    with pytest.raises(AccessError):
        channels_create(("apple", "banana", "cherry"), 'goodname6', True)

    # Invalid dictionary input
    with pytest.raises(AccessError):
        channels_create({"name" : "Takko", "age" : 32}, 'goodname7', False)

# Name is more than 20 characters
def test_channels_create_name_too_long():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    with pytest.raises(InputError):
        channels_create(user['token'], 'anamethatistoolongbutlowercase', True)

    with pytest.raises(InputError):
        channels_create(user['token'], 'anamethatistoolongbutUPPERcase', True)

    with pytest.raises(InputError):
        channels_create(user['token'], '1232323234394894543948239', True)

    with pytest.raises(InputError):
        channels_create(user['token'], '1253andlettersbutonlylowercase', True)

    with pytest.raises(InputError):
        channels_create(user['token'], '!@#$%^&*()(*&^%$#$%^&*(*&^%$%^)*', True)

    with pytest.raises(InputError):
        channels_create(user['token'], 'ALLthepossible#$*(*#*23942089things', True)

# Test that given valid inputs a channels_id is generated
def test_channels_create_output():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    output = channels_create(user['token'], 'validname1', True)
    assert output is not None
    assert output['channel_id'] is not None
    assert isinstance(output['channel_id'], int)

    output = channels_create(user['token'], 'validname2', False)
    assert output is not None
    assert output['channel_id'] is not None
    assert isinstance(output['channel_id'], int)


# Test that added channel appears in listing of channels
def test_channels_create_inList():
    clear()
    user1 = auth_register('user1@test.com', 'password', 'First', 'User')
    user2 = auth_register('user2@test.com', 'password', 'Second', 'User')

    channel1 = channels_create(user1['token'], 'channel1', True)
    channel_invite(user1['token'], channel1['channel_id'], user2['u_id'])

    channel2 = channels_create(user1['token'], 'channel2', True)

    channelList = channels_listall(user1['token'])
    channels_dict = channelList['channels']

    assert channels_dict[0]['channel_id'] == channel1['channel_id']
    assert channels_dict[1]['channel_id'] == channel2['channel_id']
    assert channels_dict[0]['name'] == 'channel1'
    assert channels_dict[1]['name'] == 'channel2'

def test_auth_logout_chack_token_with_hacked_account():
    clear()
    auth_register('test@test.com', 'password', 'firstName', 'lastName')
    # wrong token with correct data, mimics hacker changing token and trying to logout
    data.tokens[0] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjowfQ.WFXdj6pQPToti8lowJ9F-B4BIRbUkVp97-5IgHnBi2s'
    with pytest.raises(AccessError):
        channels_create('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjowfQ.WFXdj6pQPToti8lowJ9F-B4BIRbUkVp97-5IgHnBi2s', 'channel2', True)
