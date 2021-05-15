import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

from http_fixtures import url

######################## Tests all the existing http functions in Iteration 2#################################
### Helper Functions ###
def register_user(url, email, password, first_name, last_name):
    """Call auth/register to register a user in the server with the appropriate inputs"""
    data_in = {
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }
    registered = requests.post(f"{url}auth/register", json = data_in)
    user = registered.json()
    # Return a python dictionary, user which has the keys: u_id and token.
    return user

def create_channels(url, token, name, is_public):
    """Call channels/create to register a channel in the server with the appropriate inputs"""
    data_in = {
        'token': token,
        'name': name,
        'is_public': is_public
    }
    created = requests.post(f"{url}channels/create", json = data_in)
    channel = created.json()
    # Return a python dictionary, channel which has the key: channel_id
    return channel

def get_channel_details(url, token, channel_id):
    """Call channel/details to get details of the specified channel in the server"""
    data_in = {
        'token': token,
        'channel_id': channel_id
    }
    request = requests.get(f"{url}channel/details", params = data_in)
    detail = request.json()
    # Return a python dictioanary, detail which has the key: token and channel_id
    return detail

def join_channel(url, token, channel_id):
    """Call channel/join to let the a user join the channel"""
    data_in = {
        'token': token,
        'channel_id': channel_id
    }
    request = requests.post(f"{url}channel/join", json =  data_in)
    empty = request.json()
    # Return an empty dictionary
    return empty

def invite_channel(url, token, channel_id, u_id):
    """Call channel/invite to invite a user to a channel"""
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    }
    request = requests.post(f"{url}channel/invite", json =  data_in)
    empty = request.json()
    # Return an empty dictionary
    return empty

def leave_channel(url, token, channel_id):
    """Call channel/leave to make a user leave a channel"""
    data_in = {
        'token': token,
        'channel_id': channel_id
    }
    request = requests.post(f"{url}channel/leave", json =  data_in)
    empty = request.json()
    # Return an empty dictionary
    return empty

def get_messages(url, token, channel_id, start):
    """Call channel/messages to get the current messages in the channel"""
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': start
    }
    request = requests.get(f"{url}channel/messages", params = data_in)
    msg = request.json()
    # Return a python dictionary, msg which has the keys: messsages, start and end
    return msg

def add_owner(url, token, channel_id, u_id):
    """Call channel/addowner to add a member of a channel as a owner"""
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    }
    request = requests.post(f"{url}channel/addowner", json = data_in)
    ownership = request.json()
    # Return an empty dictionary
    return ownership

def remove_owner(url, token, channel_id, u_id):
    """Call channel/removeowner to remove the ownership of a channel from a member"""
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    }
    request = requests.post(f"{url}channel/removeowner", json = data_in)
    ownership = request.json()
    # Return an empty dictionary
    return ownership

def send_message(url, token, channel_id, message):
    """Call message/send to send a message in a channel"""
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': message
    }
    request = requests.post(f"{url}message/send", json = data_in)
    msg = request.json()
    # Return a dictionary, containing a key: message_id
    return msg

def remove_message(url, token, message_id):
    """Call message/remove to remove a message in a channel"""
    data_in = {
        'token': token,
        'message_id': message_id
    }
    request = requests.delete(f"{url}message/remove", json = data_in)
    msg = request.json()
    # Return an empty dictionary
    return msg

def edit_message(url, token, message_id, message):
    """Call message/edit to edit a message in a channel"""
    data_in = {
        'token': token,
        'message_id': message_id,
        'message': message
    }
    request = requests.put(f"{url}message/edit", json = data_in)
    msg = request.json()
    # Return an empty dictionary
    return msg

### Big Test Function ###
def test_run_program_http_all(url):
    '''
    test_run_program_http_all tests if all the http functions in Iteration 2
    is working as it should when used cohesively with other functions
    '''
    # Resets the current database
    requests.delete(f"{url}clear")

    # Register the owner of flockr
    owner = register_user(url, "greenAPPLE@gmail.com", "Rottenappple08", "Alice", "Fern")
    assert owner['u_id'] == 0

    # Registers 4 users into flockr
    usr2 = register_user(url, "blue_Lion@outlook.com", "Gettschwarz03", "Bennett", "Rite")
    usr3 = register_user(url, "REDbullion@yahoo.com", "Lambda121", "Karen", "Mac")
    usr4 = register_user(url, "Geryy/snel@yahoo.org", "Spongex_021ad", "Patrick", "Liam")
    usr5 = register_user(url, "xxCocoon@gmail.com", "Nelson1998", "Nelson", "Spire")

    # CHECK if auth/register manages to identify an invalid email and password
    inval_user = register_user(url, "invalid@gmailcom", "Rose1", "Jack", "Ron")
    assert inval_user['code'] == 400

    # Logs out all five users by calling auth/logout
    log1 = requests.post(f"{url}auth/logout", json = {'token': owner['token']}).json()
    log2 = requests.post(f"{url}auth/logout", json = {'token': usr2['token']}).json()
    log3 = requests.post(f"{url}auth/logout", json = {'token': usr3['token']}).json()
    log4 = requests.post(f"{url}auth/logout", json = {'token': usr4['token']}).json()
    log5 = requests.post(f"{url}auth/logout", json = {'token': usr5['token']}).json()
    # Check if they are properly logged out
    assert log1['is_success'] == True
    assert log2['is_success'] == True
    assert log3['is_success'] == True
    assert log4['is_success'] == True
    assert log5['is_success'] == True

    # Logs out the 5 users again using auth/logout
    log1 = requests.post(f"{url}auth/logout", json = {'token': owner['token']}).json()
    log2 = requests.post(f"{url}auth/logout", json = {'token': usr2['token']}).json()
    log3 = requests.post(f"{url}auth/logout", json = {'token': usr3['token']}).json()
    log4 = requests.post(f"{url}auth/logout", json = {'token': usr4['token']}).json()
    log5 = requests.post(f"{url}auth/logout", json = {'token': usr5['token']}).json()
    # Check if invalid logouts are treated as per the documentation
    assert log1['is_success'] == False
    assert log2['is_success'] == False
    assert log3['is_success'] == False
    assert log4['is_success'] == False
    assert log5['is_success'] == False

    # Logs in the owner of flockr and 2 users
    login_in1 = {'email': "greenAPPLE@gmail.com", 'password': "Rottenappple08"}
    login_in2 = {'email': "blue_Lion@outlook.com", 'password': "Gettschwarz03"}
    login_in3 = {'email': "REDbullion@yahoo.com", 'password': "Lambda121"}
    owner = requests.post(f"{url}auth/login", json = login_in1).json()
    usr2 = requests.post(f"{url}auth/login", json = login_in2).json()
    usr3 = requests.post(f"{url}auth/login", json = login_in3).json()

    # Check if all values is valid
    assert owner['token'] is not None
    assert owner['u_id'] is not None
    assert usr2['token'] is not None
    assert usr2['u_id'] is not None
    assert usr3['token'] is not None
    assert usr3['u_id'] is not None

    ### Testing channel creations ###
    # Creates a public channel called 'Master Channel' by Alice Fern
    master_channel = create_channels(url, owner['token'], 'Master Channel', True)
    ch1_info = get_channel_details(url, owner['token'], master_channel['channel_id'])
    assert ch1_info['all_members'][0]['u_id'] == owner['u_id']
    assert ch1_info['all_members'][0]['name_first'] == 'Alice'
    assert ch1_info['all_members'][0]['name_last'] == 'Fern'

    # Two other users join the public master_channel
    join_channel(url, usr2['token'], master_channel['channel_id'])
    join_channel(url, usr3['token'], master_channel['channel_id'])
    ch1_info = get_channel_details(url, owner['token'], master_channel['channel_id'])
    assert ch1_info['all_members'][0]['u_id'] == owner['u_id']
    assert ch1_info['all_members'][0]['name_first'] == 'Alice'
    assert ch1_info['all_members'][0]['name_last'] == 'Fern'
    assert ch1_info['name'] == "Master Channel"
    # CHECK all_members
    assert ch1_info['all_members'][1]['u_id'] == usr2['u_id']
    assert ch1_info['all_members'][1]['name_first'] == 'Bennett'
    assert ch1_info['all_members'][1]['name_last'] == 'Rite'
    assert ch1_info['all_members'][2]['u_id'] == usr3['u_id']
    assert ch1_info['all_members'][2]['name_first'] == 'Karen'
    assert ch1_info['all_members'][2]['name_last'] == 'Mac'
    # CHECK owner_members
    assert ch1_info['owner_members'][0]['u_id'] == owner['u_id']
    assert ch1_info['owner_members'][0]['name_first'] == 'Alice'
    assert ch1_info['owner_members'][0]['name_last'] == 'Fern'

    # usr2 creates a new private channel
    private_channel = create_channels(url, usr2['token'], 'Private Channel', False)
    ch2_info = get_channel_details(url, usr2['token'], private_channel['channel_id'])
    assert ch2_info['all_members'][0]['u_id'] == usr2['u_id']
    assert ch2_info['all_members'][0]['name_first'] == 'Bennett'
    assert ch2_info['all_members'][0]['name_last'] == 'Rite'
    assert ch2_info['name'] == 'Private Channel'
    # Invites owner into the channel
    invite_channel(url, usr2['token'], private_channel['channel_id'], owner['u_id'])
    # Invites usr4 which should have been logged out
    invite_channel(url, usr2['token'], private_channel['channel_id'], usr4['u_id'])

    #CHECK
    ch2_info = get_channel_details(url, owner['token'], private_channel['channel_id'])
    assert ch2_info['all_members'][1]['u_id'] == owner['u_id']
    assert ch2_info['all_members'][1]['name_first'] == 'Alice'
    assert ch2_info['all_members'][1]['name_last'] == 'Fern'
    assert ch2_info['all_members'][2]['u_id'] == usr4['u_id']
    assert ch2_info['all_members'][2]['name_first'] == 'Patrick'
    assert ch2_info['all_members'][2]['name_last'] == 'Liam'

    '''
    NOTE:
    a global owner (owner of flockr), i.e. the first user
    will always be added as an owner when
    they join a channel
	'''
    # Check if the owner members are appropriate
    assert ch2_info['owner_members'][0]['u_id'] == usr2['u_id']
    assert ch2_info['owner_members'][0]['name_first'] == 'Bennett'
    assert ch2_info['owner_members'][0]['name_last'] == 'Rite'
    assert ch2_info['owner_members'][1]['u_id'] == owner['u_id']
    assert ch2_info['owner_members'][1]['name_first'] == 'Alice'
    assert ch2_info['owner_members'][1]['name_last'] == 'Fern'

    # Use channel_list and channel_listall to view if the current data is accurate #
    usr3_channels = requests.get(f"{url}channels/list", params = {'token': usr3['token']}).json()
    # CHECK for channel_list
    usr3_channels['channels'][0]['channel_id'] == master_channel['channel_id']
    usr3_channels['channels'][0]['name'] == 'Master Channel'

    usr3_channels = requests.get(f"{url}channels/listall", params = {'token': usr3['token']}).json()
    # CHECK for channel_listall
    usr3_channels['channels'][0]['channel_id'] == master_channel['channel_id']
    usr3_channels['channels'][0]['name'] == 'Master Channel'
    usr3_channels['channels'][1]['channel_id'] == private_channel['channel_id']
    usr3_channels['channels'][1]['name'] == 'Private Channel'

    '''
    NOTE:
    No one can remove a global owner (owner of flockr) from their channel
    '''
    owner_channels = requests.get(f"{url}channels/list", params = {'token': owner['token']}).json()
    # Check if still a member of private_channel
    assert owner_channels['channels'][0]['channel_id'] == master_channel['channel_id']
    assert owner_channels['channels'][0]['name'] == 'Master Channel'
    assert owner_channels['channels'][1]['channel_id'] == private_channel['channel_id']
    assert owner_channels['channels'][1]['name'] == 'Private Channel'
    # Check if owner_members is correct in owner channel list
    owner_true = [{'u_id': usr2['u_id'], 'name_first': "Bennett", 'name_last': "Rite", 'profile_img_url': ""},
                  {'u_id': owner['u_id'], 'name_first': "Alice", 'name_last': "Fern", 'profile_img_url': ""}]
    # This was added as a result of the above
    details = get_channel_details(url, usr2['token'], owner_channels['channels'][1]['channel_id'])
    assert details['owner_members'] == owner_true



    # Try leaving with usr3 which should be invalid
    leave_out1 = leave_channel(url, usr3['token'], private_channel['channel_id'])
    assert leave_out1['code'] == 400

	# force Alice Fern to leave the channel for the following to work
    leave_channel(url, owner['token'], private_channel['channel_id'])
    # Usr2 leaves private_channel, causing channel to be deleted
    leave_channel(url, usr2['token'], private_channel['channel_id'])

    ch_out1 = get_channel_details(url, usr2['token'], private_channel['channel_id'])
    assert ch_out1['code'] == 400

    # Check the messages in master_channel, should raise error as there are no messages
    msg_out1 = get_messages(url, owner['token'], master_channel['channel_id'], 5)
    assert msg_out1['code'] == 400

    ################# Continuation of tests for iteration 2 #################
    # Logs in user 4
    login_in4 = {'email': "Geryy/snel@yahoo.org", 'password': "Spongex_021ad"}
    usr4 = requests.post(f"{url}auth/login", json = login_in4).json()
    # Create a public channel by user4 called "Red Room"
    red_room = create_channels(url, usr4['token'], "Red Room", True)
    join_channel(url, usr2['token'], red_room['channel_id'])
    join_channel(url, usr3['token'], red_room['channel_id'])

    # Check current channel
    ch3_info = get_channel_details(url, usr4['token'], red_room['channel_id'])
    assert len(ch3_info['all_members']) == 3
    assert len(ch3_info['owner_members']) == 1

    # Adds usr2 as an owner
    add_owner(url, usr4['token'], red_room['channel_id'], usr2['u_id'])
    ch3_info = get_channel_details(url, usr4['token'], red_room['channel_id'])
    assert len(ch3_info['owner_members']) == 2
    assert ch3_info['owner_members'][1]['u_id'] == usr2['u_id']
    assert ch3_info['owner_members'][1]['name_first'] == 'Bennett'
    assert ch3_info['owner_members'][1]['name_last'] == 'Rite'
    assert ch3_info['owner_members'][0]['u_id'] == usr4['u_id']
    assert ch3_info['owner_members'][0]['name_first'] == 'Patrick'
    assert ch3_info['owner_members'][0]['name_last'] == 'Liam'

    # Removes usr2 from owner
    remove_owner(url, usr4['token'], red_room['channel_id'], usr2['u_id'])
    ch3_info = get_channel_details(url, usr4['token'], red_room['channel_id'])
    assert len(ch3_info['owner_members']) == 1
    assert ch3_info['owner_members'][0]['u_id'] == usr4['u_id']
    assert ch3_info['owner_members'][0]['name_first'] == 'Patrick'
    assert ch3_info['owner_members'][0]['name_last'] == 'Liam'

    # Send a message in channel 3
    msg1 = send_message(url, usr4['token'], red_room['channel_id'], "First!!")
    msg2 = send_message(url, usr2['token'], red_room['channel_id'], "Second!!")
    send_message(url, usr3['token'], red_room['channel_id'], "Third!!")
    assert msg1['message_id'] == 0
    assert msg2['message_id'] == 1
    # Check
    msg_detail = get_messages(url, usr4['token'], red_room['channel_id'], 0)
    assert msg_detail['start'] == 0
    assert msg_detail['end'] == -1
    assert len(msg_detail['messages']) == 3

    # Remove a message in channel 3
    remove_message(url, usr4['token'], msg2['message_id'])
    msg_detail = get_messages(url, usr4['token'], red_room['channel_id'], 0)
    assert msg_detail['start'] == 0
    assert msg_detail['end'] == -1
    assert len(msg_detail['messages']) == 2

    # Edit a message in channel 3
    edit_message(url, usr4['token'], msg1['message_id'], "hueh?")
    msg_detail = get_messages(url, usr4['token'], red_room['channel_id'], 0)
    assert msg_detail['start'] == 0
    assert msg_detail['end'] == -1
    assert len(msg_detail['messages']) == 2
    assert msg_detail['messages'][1]['message'] == 'hueh?'

    # Search for a certain message in the channel
    msg = requests.get(f"{url}search", params = {'token': usr4['token'], 'query_str': "hueh"}).json()
    assert msg['messages'][0]['message'] == 'hueh?'
    # Search for a message that is not available in any channels
    msg = requests.get(f"{url}search", params = {'token': usr4['token'], 'query_str': "Literal"}).json()
    assert msg['messages'] == []

    # Get the user profile of the flockr owner (first user)
    owner_profile = requests.get(f"{url}user/profile", params = {'token': owner['token'], 'u_id': owner['u_id']}).json()
    assert owner_profile['user']['u_id'] == owner['u_id']
    assert owner_profile['user']['email'] == "greenAPPLE@gmail.com"
    assert owner_profile['user']['name_first'] == "Alice"
    assert owner_profile['user']['name_last'] == "Fern"
    assert owner_profile['user']['handle_str'] == "alicefern"

    # Change a name of the flockr owner
    set_name_in = {
        'token': owner['token'],
        'name_first': "Monica",
        'name_last': "Amber"
    }
    empty = requests.put(f"{url}user/profile/setname", json = set_name_in).json()
    assert empty == {}
    # Check
    owner_profile = requests.get(f"{url}user/profile", params = {'token': owner['token'], 'u_id': owner['u_id']}).json()
    assert owner_profile['user']['u_id'] == owner['u_id']
    assert owner_profile['user']['email'] == "greenAPPLE@gmail.com"
    assert owner_profile['user']['name_first'] == "Monica"
    assert owner_profile['user']['name_last'] == "Amber"
    assert owner_profile['user']['handle_str'] == "alicefern"

    # Change the email of the flockr owner
    set_email_in = {
        'token': owner['token'],
        'email': "redmonica@gmail.com"
    }
    empty = requests.put(f"{url}user/profile/setemail", json = set_email_in).json()
    assert empty == {}
    # Check
    owner_profile = requests.get(f"{url}user/profile", params = {'token': owner['token'], 'u_id': owner['u_id']}).json()
    assert owner_profile['user']['u_id'] == owner['u_id']
    assert owner_profile['user']['email'] == "redmonica@gmail.com"
    assert owner_profile['user']['name_first'] == "Monica"
    assert owner_profile['user']['name_last'] == "Amber"
    assert owner_profile['user']['handle_str'] == "alicefern"

    # Change the handle string of a user
    set_handle_in = {
        'token': owner['token'],
        'handle_str': "Moonamber"
    }
    empty = requests.put(f"{url}user/profile/sethandle", json = set_handle_in).json()
    assert empty == {}
    # Check
    owner_profile = requests.get(f"{url}user/profile", params = {'token': owner['token'], 'u_id': owner['u_id']}).json()
    assert owner_profile['user']['u_id'] == owner['u_id']
    assert owner_profile['user']['email'] == "redmonica@gmail.com"
    assert owner_profile['user']['name_first'] == "Monica"
    assert owner_profile['user']['name_last'] == "Amber"
    assert owner_profile['user']['handle_str'] == "Moonamber"

    # Call users/all and check
    users_list = requests.get(f"{url}users/all", params = {'token': owner['token']}).json()
    assert len(users_list['users']) == 5

    # Change permission of a user from member to owner
    perm_in = {
        'token': owner['token'],
        'u_id': usr2['u_id'],
        'permission_id': 1
    }
    perm_status = requests.post(f"{url}admin/userpermission/change", json = perm_in).json()
    assert perm_status == {}

    # Logs out of all the respective accounts
    log1 = requests.post(f"{url}auth/logout", json = {'token': owner['token']}).json()
    log2 = requests.post(f"{url}auth/logout", json = {'token': usr2['token']}).json()
    log3 = requests.post(f"{url}auth/logout", json = {'token': usr3['token']}).json()
    log4 = requests.post(f"{url}auth/logout", json = {'token': usr4['token']}).json()
    log5 = requests.post(f"{url}auth/logout", json = {'token': usr5['token']}).json()
    # Check if logouts return correct output
    assert log1['is_success'] == True
    assert log2['is_success'] == True
    assert log3['is_success'] == True
    assert log4['is_success'] == True
    assert log5['is_success'] == False

    # Resets the current database
    requests.delete(f"{url}clear")
