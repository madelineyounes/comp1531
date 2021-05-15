import pytest
from auth import auth_login, auth_logout, auth_register
from error import InputError, AccessError
from other import clear
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from data import data

######################## Tests when using all the functions #################################

'''
test_run_program tests if all the functions in the documentation
is working as it should when used cohesively with other functions
'''

'''
NOTE: Had to change some details of the flow of the test to allow for
	  changes to global permissions.
'''
def test_run_program_all():
    clear()

    # Registers 5 user into flockr
    usr1 = auth_register("greenAPPLE@gmail.com", "Rottenappple08", "Alice", "Fern")
    usr2 = auth_register("blue_Lion@outlook.com", "Gettschwarz03", "Bennett", "Rite")
    usr3 = auth_register("REDbullion@yahoo.com", "Lambda121", "Karen", "Mac")
    usr4 = auth_register("Geryy/snel@yahoo.org", "Spongex_021ad", "Patrick", "Liam")
    usr5 = auth_register("xxCocoon@gmail.com", "Nelson1998", "Nelson", "Spire")
    # CHECK if auth_register manages to identify an invalid email and password
    with pytest.raises(InputError):
        auth_register("invalid@gmailcom", "Rose1", "Jack", "Ron")

    # Logs out all five users and check if auth_login returns true
    assert auth_logout(usr1['token']) == {'is_success': True}
    assert auth_logout(usr2['token']) == {'is_success': True}
    assert auth_logout(usr3['token']) == {'is_success': True}
    assert auth_logout(usr4['token']) == {'is_success': True}
    assert auth_logout(usr5['token']) == {'is_success': True}

    # logs out the same token again and see it auth_logout returns false
    assert auth_logout(usr1['token']) == {'is_success': False}
    assert auth_logout(usr2['token']) == {'is_success': False}
    assert auth_logout(usr3['token']) == {'is_success': False}
    assert auth_logout(usr4['token']) == {'is_success': False}
    assert auth_logout(usr5['token']) == {'is_success': False}

    # Logs in the first three user and check if valid
    usr1 = auth_login("greenAPPLE@gmail.com", "Rottenappple08")
    assert usr1['token'] is not None
    assert usr1['u_id'] is not None
    usr2 = auth_login("blue_Lion@outlook.com", "Gettschwarz03")
    assert usr2['token'] is not None
    assert usr2['u_id'] is not None
    usr3 = auth_login("REDbullion@yahoo.com", "Lambda121")
    assert usr3['token'] is not None
    assert usr3['u_id'] is not None

    # Testing channel creations #
    # Creates a public channel called 'Master Channel' by Alice Fern
    master_channel = channels_create(usr1['token'], 'Master Channel', True)
    ch1_info = channel_details(usr1['token'], master_channel['channel_id'])
    assert ch1_info['all_members'][0]['u_id'] == usr1['u_id']
    assert ch1_info['all_members'][0]['name_first'] == 'Alice'
    assert ch1_info['all_members'][0]['name_last'] == 'Fern'

    # Two other users join the public master_channel
    channel_join(usr2['token'], master_channel['channel_id'])
    channel_join(usr3['token'], master_channel['channel_id'])
    ch1_info = channel_details(usr1['token'], master_channel['channel_id'])
    assert ch1_info['all_members'][0]['u_id'] == usr1['u_id']
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
    assert ch1_info['owner_members'][0]['u_id'] == usr1['u_id']
    assert ch1_info['owner_members'][0]['name_first'] == 'Alice'
    assert ch1_info['owner_members'][0]['name_last'] == 'Fern'

    # usr2 creates a new private channel
    private_channel = channels_create(usr2['token'], 'Private Channel', False)
    ch2_info = channel_details(usr2['token'], private_channel['channel_id'])
    assert ch2_info['all_members'][0]['u_id'] == usr2['u_id']
    assert ch2_info['all_members'][0]['name_first'] == 'Bennett'
    assert ch2_info['all_members'][0]['name_last'] == 'Rite'

    assert ch2_info['name'] == 'Private Channel'
    # Invites usr1 into the channel
    channel_invite(usr2['token'], private_channel['channel_id'], usr1['u_id'])
    # Invites usr4 which should have been logged out
    channel_invite(usr2['token'], private_channel['channel_id'], usr4['u_id'])

    #CHECK
    ch2_info = channel_details(usr1['token'], private_channel['channel_id'])
    assert ch2_info['all_members'][1]['u_id'] == usr1['u_id']
    assert ch2_info['all_members'][1]['name_first'] == 'Alice'
    assert ch2_info['all_members'][1]['name_last'] == 'Fern'
    assert ch2_info['all_members'][2]['u_id'] == usr4['u_id']
    assert ch2_info['all_members'][2]['name_first'] == 'Patrick'
    assert ch2_info['all_members'][2]['name_last'] == 'Liam'

    '''
    We decided that a global owner (Alice Fern)
    will automatically added as a channel owner upon entry through channel_invite
    This test has changed to reflect that, below lines commented out

    Adds ownership for usr1 in private_channel
    channel_addowner(usr2['token'], private_channel['channel_id'], usr1['u_id'])
	'''

    assert ch2_info['owner_members'][0]['u_id'] == usr2['u_id']
    assert ch2_info['owner_members'][0]['name_first'] == 'Bennett'
    assert ch2_info['owner_members'][0]['name_last'] == 'Rite'
    assert ch2_info['owner_members'][1]['u_id'] == usr1['u_id']
    assert ch2_info['owner_members'][1]['name_first'] == 'Alice'
    assert ch2_info['owner_members'][1]['name_last'] == 'Fern'

    # Use channel_list and channel_listall to view if the current data is accurate #
    usr3_channels = channels_list(usr3['token'])
    # CHECK for channel_list
    usr3_channels['channels'][0]['channel_id'] == master_channel['channel_id']
    usr3_channels['channels'][0]['name'] == 'Master Channel'

    usr3_channels = channels_listall(usr3['token'])
    # CHECK for channel_lisall
    usr3_channels['channels'][0]['channel_id'] == master_channel['channel_id']
    usr3_channels['channels'][0]['name'] == 'Master Channel'
    usr3_channels['channels'][1]['channel_id'] == private_channel['channel_id']
    usr3_channels['channels'][1]['name'] == 'Private Channel'

    '''
    This was commented out because a normal owner shouldnt be able to
    remove a global owner from channel_owners
    # Remove ownership of usr1 in private_channel
    channel_removeowner(usr2['token'], private_channel['channel_id'], usr1['u_id'])
    '''
    usr1_channels = channels_list(usr1['token'])
    # Check if still a member of private_channel
    assert usr1_channels['channels'][0]['channel_id'] == master_channel['channel_id']
    assert usr1_channels['channels'][0]['name'] == 'Master Channel'
    assert usr1_channels['channels'][1]['channel_id'] == private_channel['channel_id']
    assert usr1_channels['channels'][1]['name'] == 'Private Channel'
    # Check if owner_members is correct in usr1 channel list
    owner_true = [{'u_id': usr2['u_id'], 'name_first': "Bennett", 'name_last': "Rite", 'profile_img_url': ""},
                  {'u_id': usr1['u_id'], 'name_first': "Alice", 'name_last': "Fern", 'profile_img_url': ""}]
                  # This was added as a result of the above

    channel1_details = channel_details(usr1['token'], usr1_channels['channels'][1]['channel_id'])
    assert channel1_details['owner_members'] == owner_true

    # Try leaving with usr3 which should be invalid
    with pytest.raises(AccessError):
        channel_leave(usr3['token'], private_channel['channel_id'])

    # Usr2 leaves private_channel, causing channel to be deleted
    '''
	Forced Alice Fern to leave the channel for the following to work
    '''
    channel_leave(usr1['token'], private_channel['channel_id'])

    channel_leave(usr2['token'], private_channel['channel_id'])
    '''
    This was commented out because we decided to not
    remove channels when there were no owners left
    with pytest.raises(InputError):
        channel_details(usr2['token'], private_channel['channel_id'])
    The following was added instead
    '''
    assert data.channels[1].owner_members == []

    # Check the messages in master_channel, should raise error as there are no messages
    with pytest.raises(InputError):
        channel_messages(usr1['token'], master_channel['channel_id'], 5)

    # Logs out of all the respective accounts
    assert auth_logout(usr1['token']) == {'is_success': True}
    assert auth_logout(usr2['token']) == {'is_success': True}
    assert auth_logout(usr3['token']) == {'is_success': True}
    assert auth_logout(usr4['token']) == {'is_success': False}
    assert auth_logout(usr5['token']) == {'is_success': False}

    clear()
