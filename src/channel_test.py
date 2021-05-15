""" tests for channel.py file """
import pytest
from other import clear
from auth import auth_register
from channel import channel_invite, channel_details, channel_messages
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create, channels_list, channels_listall
from message import message_send
from error import InputError, AccessError
from data import data

####################### Tests for channel_invite function #####################
### Testing that given invalid inputs an InputError is generated ###
# Empty Input
def test_channel_invite_empty_inputs():
    clear()
    user = auth_register("ron@workinghard.com", 'Monkey354rahh', 'Ron', 'Weasleton')
    channel = channels_create(user['token'], "channel1", False)

    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], '')

    with pytest.raises(InputError):
        channel_invite('', channel['channel_id'], user['u_id'])

    with pytest.raises(InputError):
        channel_invite(user['token'], '', user['u_id'])

# Input into token is not a string
def test_channel_invite_invalid_type_token():
    clear()
    user = auth_register("AnEmail@account.com", 'pasW@rd3299', 'Samwise', 'Gamgee')
    channel = channels_create(user['token'], "channel1", True)
    # Invalid integer input
    with pytest.raises(AccessError):
        channel_invite(128737, channel['channel_id'], user['u_id'])

    # Invalid float input
    with pytest.raises(AccessError):
        channel_invite(54.32, channel['channel_id'], user['u_id'])

    # Invalid complex input
    with pytest.raises(AccessError):
        channel_invite(1j, channel['channel_id'], user['u_id'])

    # Invalid Boolean input
    with pytest.raises(AccessError):
        channel_invite(True, channel['channel_id'], user['u_id'])

    # Invalid list input
    with pytest.raises(AccessError):
        channel_invite(["apple", "banana", "cherry"], channel['channel_id'], user['u_id'])

    # Invalid tulpe input
    with pytest.raises(AccessError):
        channel_invite(("apple", "banana", "cherry"), channel['channel_id'], user['u_id'])

    # Invalid dictionary input
    with pytest.raises(AccessError):
        channel_invite({"name" : "Takko", "age" : 32}, channel['channel_id'], user['u_id'])

# Input into channel_id is not an integer
def test_channel_invite_invalid_type_channel_id():
    clear()
    user = auth_register("Macbeth@hotmail.com", 'N@sauceL3ftb33f', 'Ryan', 'Macbeth')
    # Invalid string input
    with pytest.raises(InputError):
        channel_invite(user['token'], 'string', user['u_id'])

    # Invalid float input
    with pytest.raises(InputError):
        channel_invite(user['token'], 54.32, user['u_id'])

    # Invalid complex input
    with pytest.raises(InputError):
        channel_invite(user['token'], 43j, user['u_id'])

    # Invalid Boolean input
    with pytest.raises(InputError):
        channel_invite(user['token'], False, user['u_id'])

    # Invalid list input
    with pytest.raises(InputError):
        channel_invite(user['token'], ["chicken", "chips", "sauce"], user['u_id'])

    # Invalid tulpe input
    with pytest.raises(InputError):
        channel_invite(user['token'], ("apple", "banana", "cherry"), user['u_id'])

    # Invalid dictionary input
    with pytest.raises(InputError):
        channel_invite(user['token'], {"name" : "Maia", "age" : 19}, user['u_id'])

# Input into u_id is not an integer
def test_channel_invite_invalid_type_u_id():
    clear()
    user = auth_register("Raffale@gmail.com", 'N@t@g00dP@sw0rd', 'Sebastian', 'Raffale')
    channel = channels_create(user['token'], "channel1", True)
    # Invalid string input
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], 'string')

    # Invalid float input
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], 54.32)

    # Invalid complex input
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], 43j)

    # Invalid Boolean input
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], False)

    # Invalid list input
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], ["chicken", "chips", "sauce"])

    # Invalid tulpe input
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], ("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], {"name" : "Maia", "age" : 19})

# Input token is unauthenticated and so is invalid
def test_channel_invite_invalid_unauth_token():
    clear()
    user = auth_register("NofearShakey@web.com", 'kjskfdnm32rjfod9US9', 'Tristian', 'Hill')
    channel = channels_create(user['token'], "channel1", True)
    with pytest.raises(AccessError):
        channel_invite("badtoken", channel['channel_id'], user['u_id'])

# Input channel_id is unauthenticated and so is invalid
def test_channel_invite_invalid_unauth_channel_id():
    clear()
    user = auth_register("p_hobbits@lor.com", 'kjskfdnm32rjfod9US9', 'Pippin', 'Merryweather')
    channels_create(user['token'], "channel1", True)
    with pytest.raises(InputError):
        channel_invite(user['token'], 23, user['u_id'])

    with pytest.raises(InputError):
        channel_invite(user['token'], 94472, user['u_id'])

    with pytest.raises(InputError):
        channel_invite(user['token'], 7, user['u_id'])

# Input u_id is unauthenticated and so is invalid
def test_channel_invite_invalid_unauth_u_id():
    clear()
    user = auth_register("hobbits@lor.com", 'kjskfdnm32rjfod9US9', 'Pippin', 'Merryweather')
    channel = channels_create(user['token'], "channel1", True)
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], 980)

    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], 7533)

    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], 5)

# Invalid as user is already a memeber the channel
def test_channel_invite_existing_member():
    clear()
    user = auth_register("E_Catalini@gmail.com", 'w1tchK$nGK1ll3r', 'Eowyn', 'Catalini')
    channel = channels_create(user['token'], "Swords", True)
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], user['u_id'])

# Invalid as user is already a not an owner of the channel
def test_channel_invite_not_owner():
    clear()
    user = auth_register("E_Catalini@gmail.com", 'w1tchK$nGK1ll3r', 'Eowyn', 'Catalini')
    not_owner = auth_register("not_anowner@gmail.com", 'dsnf$dsfs(3)', 'Notta', 'Owner')
    channel = channels_create(user['token'], "Swords", False)
    with pytest.raises(AccessError):
        channel_invite(not_owner['token'], channel['channel_id'], user['u_id'])

### Test that given valid inputs channel_invites operates correctly ###

# Testing channel_invite using channel_details
# If channel_details fails then the user was not invited correctly
def test_channel_invite_details():
    clear()
    user1 = auth_register("E_Catalini@gmail.com", 'w1tchK$nGK1ll3r', 'Eowyn', 'Catalini')
    user2 = auth_register("BeyaMac@gmail.com", 'sd9e4rhjsd', 'Beya', 'Macarangiac')
    channel = channels_create(user2['token'], "Archie", False)
    channel_invite(user2['token'], channel['channel_id'], user1['u_id'])
    details = channel_details(user2['token'], channel['channel_id'])
    expected_output = [{'u_id': 1, 'name_first': 'Beya', 'name_last': 'Macarangiac', 'profile_img_url': ""},
    {'u_id': 0, 'name_first': 'Eowyn', 'name_last': 'Catalini', 'profile_img_url': ""}]

    assert [user for user in details['all_members']] == expected_output

# Testing channel_invite using channel_leave
# channel invite should raise AccessError as user is already in channel
def test_channel_invite_leave():
    clear()
    user = auth_register("Wrobinson@hotmail.com", 't!M31$@111usion', 'Wilbur', 'Robinson')
    channel = channels_create(user['token'], "Time", False)

    # User already in channel as it was created by the user
    with pytest.raises(InputError):
        channel_invite(user['token'], channel['channel_id'], user['u_id'])
    ''' This was removed on 25/10/2020
    # only User / Owner leaves, deleting the channel in the process
    channel_leave(user['token'], channel['channel_id'])
    with pytest.raises(InputError):
        channel_details(user['token'], channel['channel_id'])
    '''

# added test for global permitions change
def test_channel_invite_owner_of_flockr():
    clear()
    # first user is global owner
    user1 = auth_register("billyboi@bagend.com", 'Th#1r3nG09', 'Bilbo', 'Baggins')
    user2 = auth_register("test@test.com", 'password', 'firstName', 'lastName')
    # second user creates a channel
    channel = channels_create(user2['token'], "Appreciate Dwarfs", True)
    channel_invite(user2['token'], channel['channel_id'], user1['u_id'])
    details = channel_details(user2['token'], channel['channel_id'])
    check_memebrs_list = [user['u_id'] for user in details['owner_members']]
    # makes sure global owner is added as owner of a channel
    assert user1['u_id'] in check_memebrs_list


######################################## Tests for channel_details ########################################

# InputError- Channel ID is not a valid channel
def test_channel_details_not_a_vaild_channel():
    clear()
    result = auth_register("ZAH-kee@gmail.com", 'DZVznKzzuPnjc', 'Alexie', 'Evie-Mae')
    channels_create(result['token'], "test_channel", True)
    # A channel exists but channel details is not given the correct id
    with pytest.raises(InputError):
        channel_details(result['token'], "NotCorrect")

# The given token is not a vaild one
def test_invalid_token():
    clear()
    result = auth_register("ZAH-kee@gmail.com", 'DZVznKzzuPnjc', 'Alexie', 'Evie-Mae')
    channel_id = channels_create(result['token'], "test_channel", True)
    with pytest.raises(AccessError):
        channel_details("123", channel_id)

# AccessError- Authorised user is not a member of channel with channel_id
def test_channel_details_not_a_memebr_of_channel():
    clear()
    person1 = auth_register("pies@gmail.net", 'hU5,&>Q$>HnDfa<N', 'Toyah', 'Rennie')
    person2 = auth_register("storytelecom@gmail.net", 'hU5,&>Q$>HnDfa<N', 'Carys', 'Chaney')
    channel_id = channels_create(person1['token'], "test_channel", False)
    with pytest.raises(AccessError):
        channel_details(person2['token'], channel_id["channel_id"]) # Person 2 isn't part of the channel so it should fail

# Check channel name is correct
def test_channel_details_not_valid_channel():
    clear()
    result = auth_register("udiNovo@gmail.net", 'Aa_pm^[uC_w[Nu55', 'Nannie', 'Herring')
    channel_id = channels_create(result['token'], "test_channel", True)
    output = channel_details(result['token'], channel_id["channel_id"])
    assert output['name'] == "test_channel"

### Check u_id of owner members ###
# One member
def test_channel_details_owner_u_id():
    clear()
    person1 = auth_register("UNSURPASSINGLY@gmail.net", 'Aa_pm^[uC_w[Nu55', 'Hope', 'Klein')
    channel_id = channels_create(person1['token'], "test_channel", True)
    output = channel_details(person1['token'], channel_id["channel_id"])
    assert output["owner_members"][0]['u_id'] == person1['u_id']

# Three members
def test_channel_details_owners_u_id():
    clear()
    # Register 3 users
    person1 = auth_register("Jreviendrai@gmail.net", 'pKnrV5RPevE8UkHq', 'Neelam', 'Mcculloch')
    person2 = auth_register("Lapastora@gmail.net", 'HeX3yPxdB6t35v3C', 'Zahid', 'Gordon')
    person3 = auth_register("Qaribullah@gmail.net", 'Q6k5Ntr2kTpEQzBW', 'Lilly-Ann', 'Robinson')
    # Person 1 creates a channel
    channel_id = channels_create(person1['token'], "test_channel", True)
    # The other two join the channel
    channel_join(person2['token'], channel_id['channel_id'])
    channel_join(person3['token'], channel_id['channel_id'])
    # Person 1 adds the other 2 as owners
    channel_addowner(person1['token'], channel_id["channel_id"], person2['u_id'])
    channel_addowner(person1['token'], channel_id["channel_id"], person3['u_id'])
    # Person 1 requests the channels details
    output = channel_details(person1['token'], channel_id["channel_id"])
    # Checks the outputed u_id's are correct by comparing sorted lists
    check_list = [user['u_id'] for user in output['owner_members']]
    expected_output = [person1['u_id'], person2['u_id'], person3['u_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output

### Check names of owner members, first and last ###
# One member
def test_channel_details_owner_names():
    clear()
    person1 = auth_register("Tysheema@gmail.net", 'BUaPg2e5CNSFEaGC', 'Riley', 'Feeney')
    channel_id = channels_create(person1['token'], "test_channel", True)
    output = channel_details(person1['token'], channel_id["channel_id"])
    assert output["owner_members"][0]['name_first'] == 'Riley'
    assert output["owner_members"][0]['name_last'] == 'Feeney'

# Three members
def test_channel_details_owners_names():
    clear()
    # Register 3 users
    person1 = auth_register("Jreviendrai@gmail.net", 'pKnrV5RPevE8UkHq', 'Neelam', 'Mcculloch')
    person2 = auth_register("Lapastora@gmail.net", 'HeX3yPxdB6t35v3C', 'Zahid', 'Gordon')
    person3 = auth_register("Qaribullah@gmail.net", 'Q6k5Ntr2kTpEQzBW', 'Lilly-Ann', 'Robinson')
    # Person 1 creates a channel
    channel_id = channels_create(person1['token'], "test_channel", False)
    # The other two are invited to the channel
    channel_invite(person1['token'], channel_id['channel_id'], person2['u_id'])
    channel_invite(person1['token'], channel_id['channel_id'], person3['u_id'])
    # Person 1 adds the other 2 as owners
    channel_addowner(person1['token'], channel_id["channel_id"], person2['u_id'])
    channel_addowner(person1['token'], channel_id["channel_id"], person3['u_id'])
    # Person 1 requests the channels details
    output = channel_details(person1['token'], channel_id["channel_id"])
    # Checks the outputed u_id's are correct by comparing sorted lists
    check_list_first = [user['name_first'] for user in output['owner_members']]
    check_list_last = [user['name_last'] for user in output['owner_members']]
    expected_output_first = ['Neelam', 'Zahid', 'Lilly-Ann']
    expected_output_last = ['Mcculloch', 'Gordon', 'Robinson']
    check_list_first.sort()
    expected_output_first.sort()
    check_list_first.sort()
    expected_output_first.sort()
    assert check_list_first == expected_output_first
    assert check_list_last == expected_output_last


### Check u_id of all members ###
# One member
def test_channel_details_member_u_id():
    clear()
    person1 = auth_register("UNSURPASSINGLY@gmail.net", 'Aa_pm^[uC_w[Nu55', 'Hope', 'Klein')
    channel_id = channels_create(person1['token'], "test_channel", True)
    output = channel_details(person1['token'], channel_id["channel_id"])
    assert output["all_members"][0]['u_id'] == person1['u_id']


# Three members
def test_channel_details_members_u_id():
    clear()
    # Register 3 users
    person1 = auth_register("Jreviendrai@gmail.net", 'pKnrV5RPevE8UkHq', 'Neelam', 'Mcculloch')
    person2 = auth_register("Lapastora@gmail.net", 'HeX3yPxdB6t35v3C', 'Zahid', 'Gordon')
    person3 = auth_register("Qaribullah@gmail.net", 'Q6k5Ntr2kTpEQzBW', 'Lilly-Ann', 'Robinson')
    # Person 1 creates a channel
    channel_id = channels_create(person1['token'], "test_channel", True)
    # Person 1 adds person 3 as a owner and person 2 joins themselves
    channel_join(person2['token'], channel_id["channel_id"])
    channel_invite(person1['token'], channel_id['channel_id'], person3['u_id'])
    channel_addowner(person1['token'], channel_id["channel_id"], person3['u_id'])
    # Person 2 requests the channels details, also testing a non owner can ask for details
    output = channel_details(person2['token'], channel_id["channel_id"])
    # Checks the outputed u_id's are correct by comparing sorted lists
    check_list = [user['u_id'] for user in output['all_members']]
    expected_output = [person1['u_id'], person2['u_id'], person3['u_id']]
    check_list.sort()
    expected_output.sort()
    assert check_list == expected_output


### Check names of all members, first and last ###
# One member
def test_channel_details_member_name():
    clear()
    person1 = auth_register("Tysheema@gmail.net", 'BUaPg2e5CNSFEaGC', 'Riley', 'Feeney')
    channel_id = channels_create(person1['token'], "test_channel", True)
    output = channel_details(person1['token'], channel_id["channel_id"])
    assert output["all_members"][0]['name_first'] == 'Riley'
    assert output["all_members"][0]['name_last'] == 'Feeney'

# Three members
def test_channel_details_members_names():
    clear()
    # Register 3 users
    person1 = auth_register("Jreviendrai@gmail.net", 'pKnrV5RPevE8UkHq', 'Neelam', 'Mcculloch')
    person2 = auth_register("Lapastora@gmail.net", 'HeX3yPxdB6t35v3C', 'Zahid', 'Gordon')
    person3 = auth_register("Qaribullah@gmail.net", 'Q6k5Ntr2kTpEQzBW', 'Lilly-Ann', 'Robinson')
    # Person 1 creates a channel
    channel_id = channels_create(person1['token'], "test_channel", True)
    # Person 1 adds the other 2 as owners
    channel_join(person2['token'], channel_id["channel_id"])
    channel_join(person3['token'], channel_id["channel_id"])
    channel_addowner(person1['token'], channel_id["channel_id"], person2['u_id'])
    channel_addowner(person1['token'], channel_id["channel_id"], person3['u_id'])
    # Person 1 requests the channels details
    output = channel_details(person3['token'], channel_id["channel_id"])
    # Checks the outputed u_id's are correct by comparing sorted lists
    check_list_first = [user['name_first'] for user in output['all_members']]
    check_list_last = [user['name_last'] for user in output['all_members']]
    expected_output_first = ['Neelam', 'Zahid', 'Lilly-Ann']
    expected_output_last = ['Mcculloch', 'Gordon', 'Robinson']
    check_list_first.sort()
    expected_output_first.sort()
    check_list_first.sort()
    expected_output_first.sort()
    assert check_list_first == expected_output_first
    assert check_list_last == expected_output_last

############################## Tests for channel_messages ##############################
# Raises InputError as given channel_id is not a valid channel
def test_channel_messages_invalid_type_channel_id():
    ''' channel_messages should raise InputError when it is given an invalid channel_id'''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    usr_sven = auth_register('validemail2@gmail.com', 'NootNoot32', 'Sven', 'Ping')

    with pytest.raises(InputError):
        channel_messages(usr_leony['token'], 20210, 0)
    with pytest.raises(InputError):
        channel_messages(usr_hayden['token'], 1003, 0)
    with pytest.raises(InputError):
        channel_messages(usr_sven['token'], 1455, 0)

# Raises InputError as start is:
# -> greater than total number of messages in the channel
# -> or less than 0
def test_channel_messages_invalid_type_start():
    ''' channel_messages should raise InputError when given an invalid start argument '''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    # Create channels
    channel_public = channels_create(usr_hayden['token'], "Testing_public", True)
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)

    # Invalid complex input
    with pytest.raises(InputError):
        channel_messages(usr_leony['token'], channel_private['channel_id'], -100)
    with pytest.raises(InputError):
        channel_messages(usr_hayden['token'], channel_public['channel_id'], 1000)

# Raises AccessError as user is not a member of the channel
def test_channel_messages_invalid_member():
    ''' channel_messages should raise AccesError as user given is not in the channel '''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    usr_sven = auth_register('validemail2@gmail.com', 'NootNoot32', 'Sven', 'Ping')
    # Create channels
    channel_public = channels_create(usr_hayden['token'], "Testing_public", True)
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)

    with pytest.raises(AccessError):
        channel_messages(usr_leony['token'], channel_public['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages(usr_hayden['token'], channel_private['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages(usr_sven['token'], channel_private['channel_id'], 0)

# Test to see if channel_messages will still work when there are no messages in the channel
def test_channel_messages_no_messages():
    ''''
    channel_messages should return an empty list of messages, start = 0, and end = -1,
    when it is given a channel with no messages and start of 0 as input
    '''
    clear()
    # Register users first
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    # Create channels
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)

    message = channel_messages(usr_leony['token'], channel_private['channel_id'], 0)
    assert message == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_channel_messages_many_messages():
    '''
    channel_messages should only return the first 50 messages in the channel
    when start is 100 and there more than 50 messages in the the channel
    '''
    clear()
    # Register users first
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    # Create channels
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)

    # Send 100 messages
    sent_msg = 0
    while sent_msg < 100:
        message_send(usr_leony['token'], channel_private['channel_id'], 'Hello')
        sent_msg += 1

    # Check
    message = channel_messages(usr_leony['token'], channel_private['channel_id'], 20)
    assert len(message['messages']) == 50
    assert message['start'] == 20
    assert message['end'] == 70
    print(message['messages'])
    assert message['messages'][0]['message_id'] == 69
    assert message['messages'][49]['message_id'] == 20

def test_channel_messages_start_equal_message_count():
    '''
    channel_messages should only return 1 message if start is equal to the number
    of messages in the channel
    '''
    clear()
    # Register users first
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    # Create channels
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)

    # Send 50 messages
    sent_msg = 0
    while sent_msg < 50:
        message_send(usr_leony['token'], channel_private['channel_id'], 'Oof')
        sent_msg += 1

    # Check
    message = channel_messages(usr_leony['token'], channel_private['channel_id'], 50)
    assert len(message['messages']) == 1
    assert message['start'] == 50
    assert message['end'] == -1
    assert message['messages'][0]['message_id'] == 49
    assert message['messages'][0]['message'] == 'Oof'

############################## Tests for channel_leave ###################################
# Raises InputError as given channel_id is not a valid channel
def test_channel_leave_invalid_type_channel_id():
    ''' channel_leave should raise InputError as it is given an invalid channel '''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    usr_sven = auth_register('validemail2@gmail.com', 'NootNoot32', 'Sven', 'Ping')

    # Invalid tulpe input
    with pytest.raises(InputError):
        channel_leave(usr_hayden['token'], 1100)
    with pytest.raises(InputError):
        channel_leave(usr_leony['token'], 1004)
    with pytest.raises(InputError):
        channel_leave(usr_sven['token'], 1020)

# Raises AccessError since user is not a member of the the channel
def test_channel_leave_invalid_member():
    ''' channel_leave should raise AccessError as user given is not in the channel '''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    usr_sven = auth_register('validemail2@gmail.com', 'NootNoot32', 'Sven', 'Ping')
    # Creating channels
    channel_public = channels_create(usr_hayden['token'], "Testing_public", True)
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)


    with pytest.raises(AccessError):
        channel_leave(usr_leony['token'], channel_public['channel_id'])
    with pytest.raises(AccessError):
        channel_leave(usr_hayden['token'], channel_private['channel_id'])
    with pytest.raises(AccessError):
        channel_leave(usr_sven['token'], channel_private['channel_id'])

# Given a valid token and channel_id, user is removed from the channel
def test_channel_leave_hayden():
    ''' test to check if channel_leave is working when the owner leaves a public channel '''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_nothayden = auth_register('test@test.com', 'password', 'test', 'user')
    # Creating channels
    channel_public = channels_create(usr_hayden['token'], "Testing_public", True)

    channel_leave(usr_hayden['token'], channel_public['channel_id'])

    # Channel should now have no members but still exist
    channels = channels_listall(usr_nothayden['token'])
    assert channels['channels'] == [{
        'channel_id': 0,
        'name': "Testing_public"
    }]

def test_channel_leave_leony():
    ''' test to check if channel_leave is working when the owner leaves a private channel'''
    clear()
    # Register users first
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    usr_notleony = auth_register('test@test.com', 'password', 'test', 'user')
    # Creating channels
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)

    channel_leave(usr_leony['token'], channel_private['channel_id'])

    # Channel should now have no members but still exist
    channels = channels_listall(usr_notleony['token'])
    assert channels['channels'] == [{
        'channel_id': 0,
        'name': "Testing_private"
    }]

############################## Tests for channel_join ###################################
# Raises InputError as given channel_id is not a valid channel
def test_channel_join_invalid_type_channel_id():
    ''' channel_join should raise InputError as it is given an invalid / inexistent channel'''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    usr_sven = auth_register('validemail2@gmail.com', 'NootNoot32', 'Sven', 'Ping')

    # CHECK
    with pytest.raises(InputError):
        channel_join(usr_hayden['token'], 1002)
    with pytest.raises(InputError):
        channel_join(usr_leony['token'], 1005)
    with pytest.raises(InputError):
        channel_join(usr_sven['token'], 8001)

# Raises AccessError since user is not a member of the the channel
def test_channel_join_invalid_member():
    ''' channel_join should raise AccessError as user given is not in the channel '''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    usr_sven = auth_register('validemail2@gmail.com', 'NootNoot32', 'Sven', 'Ping')
    # Create a private channel
    channel_private = channels_create(usr_leony['token'], "Testing_private", False)

    channel_join(usr_hayden['token'], channel_private['channel_id'])
    with pytest.raises(AccessError):
        channel_join(usr_sven['token'], channel_private['channel_id'])

# Testing channel_join for public channel (channel_public)
def test_channel_join_public():
    ''' check to see if channel_join works for a public channel'''
    clear()
    # Register users first
    usr_hayden = auth_register('validemail@gmail.com', 'RedRocket88', 'Hayden', 'Everest')
    usr_leony = auth_register('validemail1@outlook.com', 'BlueDaisy99', 'Leony', 'Mint')
    # Create a public channel
    channel_public = channels_create(usr_hayden['token'], "Testing_public", True)

    # CHECKS
    channel_join(usr_leony['token'], channel_public['channel_id'])
    # Channel_details should be succesful for leony in public channel
    result = channel_details(usr_leony['token'], channel_public['channel_id'])
    assert result['name'] == "Testing_public"

    assert result['owner_members'] == [
        {'u_id': usr_hayden["u_id"], 'name_first': "Hayden", 'name_last': "Everest", 'profile_img_url': ""}
    ]
    assert result['all_members'] == [
        {'u_id': usr_hayden["u_id"], 'name_first': "Hayden", 'name_last': "Everest", 'profile_img_url': ""},
        {'u_id': usr_leony["u_id"], 'name_first': "Leony", 'name_last': "Mint", 'profile_img_url': ""}
    ]

def test_channel_join_leave_many():
    '''
    Testing using both channel_join and channel_leave to
    check that both are working as it should
    '''
    clear()
    # test many joining
    person1 = auth_register("Jreviendrai@gmail.net", 'pKnrV5RPevE8UkHq', 'Neelam', 'Mcculloch')
    person2 = auth_register("Lapastora@gmail.net", 'HeX3yPxdB6t35v3C', 'Zahid', 'Gordon')
    person3 = auth_register("Qaribullah@gmail.net", 'Q6k5Ntr2kTpEQzBW', 'Lilly-Ann', 'Robinson')
    channel_id = channels_create(person1['token'], "test_channel1", True)
    channel_join(person2['token'], channel_id['channel_id'])
    channel_join(person3['token'], channel_id['channel_id'])
    result = channel_details(person1['token'], channel_id['channel_id'])
    assert result['name'] == "test_channel1"
    assert result['owner_members'] == [
        {'u_id': person1["u_id"], 'name_first': 'Neelam', 'name_last': 'Mcculloch', 'profile_img_url': ""}
    ]
    assert result['all_members'] == [
        {'u_id': person1["u_id"], 'name_first': 'Neelam', 'name_last': 'Mcculloch', 'profile_img_url': ""},
        {'u_id': person2["u_id"], 'name_first': 'Zahid', 'name_last': 'Gordon', 'profile_img_url': ""},
        {'u_id': person3["u_id"], 'name_first': 'Lilly-Ann', 'name_last': 'Robinson', 'profile_img_url': ""}
    ]
    # test many leaving
    channel_leave(person3['token'], channel_id['channel_id'])
    result = channel_details(person1['token'], channel_id['channel_id'])
    assert result['owner_members'] == [
        {'u_id': person1["u_id"], 'name_first': 'Neelam', 'name_last': 'Mcculloch', 'profile_img_url': ""}
    ]
    assert result['all_members'] == [
        {'u_id': person1["u_id"], 'name_first': 'Neelam', 'name_last': 'Mcculloch', 'profile_img_url': ""},
        {'u_id': person2["u_id"], 'name_first': 'Zahid', 'name_last': 'Gordon', 'profile_img_url': ""}
    ]
    channel_leave(person2['token'], channel_id['channel_id'])
    result = channel_details(person1['token'], channel_id['channel_id'])
    assert result['owner_members'] == [
        {'u_id': person1["u_id"], 'name_first': 'Neelam', 'name_last': 'Mcculloch', 'profile_img_url': ""}
    ]
    assert result['all_members'] == [
        {'u_id': person1["u_id"], 'name_first': 'Neelam', 'name_last': 'Mcculloch', 'profile_img_url': ""}
    ]
    channel_leave(person1['token'], channel_id['channel_id'])
    # Channel should be deleted as the only owner left
    # and therefore channel_details should raise an error when given the already deleted channel_id
    ''' This was removed on 25/10/2020
    with pytest.raises(InputError):
        channel_details(person1['token'], channel_id['channel_id'])
    And the following was added '''
    # Channel should now have no members but still exist
    channels = channels_listall(person1['token'])
    assert channels['channels'] == [{
        'channel_id': 0,
        'name': "test_channel1"
    }]

def test_channel_join_global_owner():
    '''
    Testing that if the user that joins is a global owner, they are automatically
    added to the owners list as well
    '''
    clear()
    # First registered user should have permission_id: 1
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')

    # Create new users, who creates channel
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')
    user3 = auth_register('test3@test.com', 'password3', 'firstName3', 'lastName3')
    channel = channels_create(user2['token'], "channel1", True)
    channel_join(user3['token'], channel['channel_id'])

    # user1 joins, and should be an owner (able to remove user2 as owner)
    channel_join(user1['token'], channel['channel_id'])
    channel_removeowner(user1['token'], channel['channel_id'], user2['u_id'])

    # user2 should now be unable to add user3 as an owner
    with pytest.raises(AccessError):
        channel_addowner(user2['token'], channel['channel_id'], user3['u_id'])

    # Check that only user1 appears in owner_members
    details = channel_details(user2['token'], channel['channel_id'])
    assert details['owner_members'] == [{'u_id': user1['u_id'],
                                         'name_first': "firstName",
                                         'name_last': "lastName",
                                         'profile_img_url': ""}]

def test_channel_join_already_member():
    '''
    Tests that channel join raises InputError if the caller is already a member
    '''
    clear()
    user = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    channel = channels_create(user['token'], "channel1", True)
    
    with pytest.raises(InputError):
        channel_join(user['token'], channel['channel_id'])

######################## Tests focused on channel_addowner #################################

# Invalid channel_id should cause error
def test_channel_addowner_invalid_channel_id():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins channel
    invalid_id = -4
    assert channel['channel_id'] != invalid_id

    with pytest.raises(InputError):
        channel_addowner(user1['token'], invalid_id, user2['u_id']) # User 1 attempts to add user2 as an owner

# Invalid user_id should cause error
def test_channel_addowner_invalid_user_id():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel

    with pytest.raises(InputError):
        channel_addowner(user1['token'], channel['channel_id'], -42) # User 1 attempts to add nonexistent user

# Invalid user_id should cause error after adding one successfully
def test_channel_addowner_invalid_user_id_more_users():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins channel
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User 1 adds user2 as owner

    user3 = auth_register('test3@test.com', 'password', 'firstName3', 'lastName3') # User 3 is not a member

    with pytest.raises(InputError):
        channel_addowner(user1['token'], channel['channel_id'], user3['u_id']) # User 1 attempts to add nonmember user


# User_id already an owner should cause error
def test_channel_addowner_already_owner():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins channel
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User1 adds User2 as owner

    with pytest.raises(InputError):
        channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User 1 attempts to add user2 as an owner again


# Access by user who is not an owner themselves should cause error
def test_channel_addowner_unauthorized_access():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')
    user3 = auth_register('test3@test.com', 'password3', 'firstName3', 'lastName3')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins channel
    channel_join(user3['token'], channel['channel_id']) # User3 joins channel

    with pytest.raises(AccessError):
        channel_addowner(user2['token'], channel['channel_id'], user3['u_id']) # User 2 attempts to add user3 as an owner


# Added owner should appear in the channel owners list
def test_channel_addowner_added_owner():
    clear()

    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins channel
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User1 adds User2 as owner

    details = channel_details(user1['token'], channel['channel_id'])

    assert user2['u_id'] in [user['u_id'] for user in details['owner_members']]

# Global owner can be added regardless of existing channel membership
def test_channel_addowner_add_globalowner():
    clear()

    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    # User2 creates a Private Channel
    channel = channels_create(user2['token'], 'channelName', True)

    # User2 adds user1 as owner even though user2 is not a member
    details = channel_details(user2['token'], channel['channel_id'])
    assert len(details['all_members']) == 1
    assert len(details['owner_members']) == 1
    channel_addowner(user2['token'], channel['channel_id'], user1['u_id'])

    # User1 should appear in all_members and owner_members
    details_after = channel_details(user2['token'], channel['channel_id'])

    assert len(details_after['all_members']) == 2
    assert len(details_after['owner_members']) == 2
    user_1_summary = {'u_id': user1['u_id'], 'name_first': "firstName", 'name_last': "lastName", 'profile_img_url': ""}
    assert user_1_summary in details_after['all_members']
    assert user_1_summary in details_after['owner_members']

######################## Tests focused on channel_removeowner #################################

# Invalid channel_id should cause error
def test_channel_removeowner_invalid_channel_id():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins the channel
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User1 adds User2 as owner

    invalid_id = -4
    assert channel['channel_id'] != invalid_id

    with pytest.raises(InputError):
        channel_removeowner(user1['token'], invalid_id, user2['u_id']) # User 1 attempts to remove User2 as owner

def test_channel_removeowner_invalid_u_id():
    clear()
    # Register a user and create a channel
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    fake_u_id = 100020

    # channel_removeowner should raise an InputError when target u_id is invalid
    with pytest.raises(InputError):
        channel_removeowner(user1['token'], channel['channel_id'], fake_u_id)

# Access by user who is not an owner themselves should cause error
def test_channel_removeowner_unauthorized_access():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins the channel

    with pytest.raises(AccessError):
        channel_removeowner(user2['token'], channel['channel_id'], user1['u_id']) # User 2 attempts to remove User1 as owner


# Removed owner should not appear in the channel owners list
def test_channel_removeowner_removed_owner():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User1 adds User2 as owner

    details_before = channel_details(user1['token'], channel['channel_id'])

    assert user2['u_id'] in [user['u_id'] for user in details_before['owner_members']]

    channel_removeowner(user1['token'], channel['channel_id'], user2['u_id']) # User1 removes User2 as owner

    details_after = channel_details(user1['token'], channel['channel_id'])

    assert not user2['u_id'] in [user['u_id'] for user in details_after['owner_members']]

# Normal channel owner cannot remove global channel owner
def test_channel_removeowner_normal_removes_global():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User1 adds User2 as owner

    with pytest.raises(AccessError):
        channel_removeowner(user2['token'], channel['channel_id'], user1['u_id'])

    # User1 should be able to remove user2
    channel_removeowner(user1['token'], channel['channel_id'], user2['u_id'])
    details = channel_details(user1['token'], channel['channel_id'])

    user_2_summary = {'u_id': user2['u_id'], 'name_first': "firstName2", 'name_last': "lastName2", 'profile_img_url': ""}
    assert not user_2_summary in details['owner_members']
    assert user_2_summary in details['all_members']

# Global user can demote themselves
def test_channel_removeowner_globalowner_self_demotion():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins
    channel_addowner(user1['token'], channel['channel_id'], user2['u_id']) # User1 adds User2 as owner

    channel_removeowner(user1['token'], channel['channel_id'], user1['u_id'])
    details = channel_details(user1['token'], channel['channel_id'])

    user_1_summary = {'u_id': user1['u_id'], 'name_first': "firstName", 'name_last': "lastName", 'profile_img_url': ""}
    assert not user_1_summary in details['owner_members']
    assert user_1_summary in details['all_members']

def test_channel_removeowner_not_member():
    '''
    Test that removeowner raises Access Error if called by someone not in the channel
    '''
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    
    # User2 tries to remove user1 as owner, but is not even in the channel, let alone an owner
    with pytest.raises(AccessError):
        channel_removeowner(user2['token'], channel['channel_id'], user1['u_id'])

def test_channel_removeowner_target_not_owner():
    clear()
    user1 = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    user2 = auth_register('test2@test.com', 'password2', 'firstName2', 'lastName2')

    channel = channels_create(user1['token'], 'channelName', True) # User1 creates a public channel
    channel_join(user2['token'], channel['channel_id']) # User2 joins
    
    # user1 tries to removeowner on user2, but they're not an owner
    with pytest.raises(InputError):
        channel_removeowner(user1['token'], channel['channel_id'], user2['u_id'])
