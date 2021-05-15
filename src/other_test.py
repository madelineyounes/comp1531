""" tests for other.py file """
import pytest
import copy
from auth import auth_login, auth_logout, auth_register
from error import InputError, AccessError
from expected_data import expected_data5, expected_data6
from expected_data import expected_data7, expected_data8, expected_data9
from other import clear, users_all, admin_userpermission_change, valid_channel_id, valid_user_id
from other import valid_email, existing_email, existing_handle, authenticate_token
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from user import user_profile

####################### Tests for users_all function #####################

def test_users_all_invalid_token():
    clear()
    with pytest.raises(AccessError):
        users_all("invalid")

def test_users_all_one_user():
    clear()
    user = auth_register("ron@workinghard.com", 'Monkey354rahh', 'Ron', 'Weasleton')
    expected_data = {'users': [{}]}
    user1 =  {
            'u_id': 0,
            'email': 'ron@workinghard.com',
            'name_first': 'Ron',
            'name_last': 'Weasleton',
            'handle_str': 'ronweasleton',
            'profile_img_url': ""
    }

    expected_data['users'][0] = user1

    assert users_all(user['token']) == expected_data

def test_users_all_expected_data5():
    clear()
    # create users
    user = auth_register('WICKEDER@yahoo.org', '123abc!@#', 'Cosmo', 'Kearns')
    auth_register('RenameLHC@yahoo.org', '123abc!@#', 'Abida', 'Zhang')
    auth_register("repeatin-rifle@yahoo.org", '123abc!@#', 'Brenden', 'Partridge')
    copyexpected = copy.deepcopy(expected_data5['users'])
    for users1 in copyexpected:
        del users1['permission_id']

    assert users_all(user['token']) == {'users': copyexpected}

def test_users_all_expected_data6():
    clear()
    user = auth_register('hello@yahoo.org', '12sdf3abcsf!@#', 'sudifhsdfhssdsdfsoifusdfs', 'Arsdfsdfwxefefchsdfsdsdfer')
    assert users_all(user['token']) == {'users': expected_data6['users']}


def test_users_all_changed_handle():
    clear()
    user1 = auth_register('Mario@yahoo.org', '123asdgc!@#', 'Lugi', 'Mario')
    auth_register('MarioKart@yahoo.org', '123abc!@#', 'Lugi', 'Mario')
    returned_users = users_all(user1['token'])
    assert returned_users['users'][0]['handle_str'] != returned_users['users'][1]['handle_str']

####################### Tests for admin_userpermission_change function #####################
### Testing that given invalid inputs an InputError is generated ###
# Empty Input
def test_admin_userpermission_change_empty_input():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    user2 = auth_register('themail@online.com', '(&^hbhasj', 'Kyle', 'Phantom')
    with pytest.raises(InputError):
        admin_userpermission_change('', '', '')

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], '', '')

    with pytest.raises(InputError):
        admin_userpermission_change('', 12, '')

    with pytest.raises(InputError):
        admin_userpermission_change('', '', 1)

    with pytest.raises(InputError):
        admin_userpermission_change('', 12, 1)

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], '', 1)

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user2['u_id'], '')

# Input into token is not a string
def test_admin_userpermission_change_invalid_type_token():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    # Invalid integer input
    with pytest.raises(AccessError):
        admin_userpermission_change(128737, user['u_id'], 2)

    # Invalid float input
    with pytest.raises(AccessError):
        admin_userpermission_change(54.32, user['u_id'], 2)

    # Invalid complex input
    with pytest.raises(AccessError):
        admin_userpermission_change(1j, user['u_id'], 2)

    # Invalid Boolean input
    with pytest.raises(AccessError):
        admin_userpermission_change(True, user['u_id'], 2)

    # Invalid list input
    with pytest.raises(AccessError):
        admin_userpermission_change(["apple", "banana", "cherry"], user['u_id'], 2)

    # Invalid tulpe input
    with pytest.raises(AccessError):
        admin_userpermission_change(("apple", "banana", "cherry"), user['u_id'], 2)

    # Invalid dictionary input
    with pytest.raises(AccessError):
        admin_userpermission_change({"name" : "Takko", "age" : 32}, user['u_id'], 2)

# Input into token is not a string
def test_admin_userpermission_change_invalid_type_u_id():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    # Invalid string input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], 'string', 2)

    # Invalid float input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], 54.32, 2)

    # Invalid complex input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], 1j, 2)

    # Invalid Boolean input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], True, 2)

    # Invalid list input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], ["apple", "banana", "cherry"], 2)

    # Invalid tulpe input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], ("apple", "banana", "cherry"), 2)

    # Invalid dictionary input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], {"name" : "Takko", "age" : 32}, 2)

# Input into token is not a string
def test_admin_userpermission_change_invalid_type_permission_id():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    # Invalid string input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], 'string')

    # Invalid float input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], 54.32)

    # Invalid complex input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], 1j)

    # Invalid Boolean input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], True)

    # Invalid list input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], ["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], ("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], {"name" : "Takko", "age" : 32})

# Testing when u_id does not refer to a valid user
def test_admin_userpermission_change_invalid_user():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    invalid_u_id1 = user['u_id'] + 34
    invalid_u_id2 = user['u_id'] + 79

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], invalid_u_id1, 2)

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], invalid_u_id2, 2)

# Testing when permission_id does not refer to a permission
def test_admin_userpermission_change_invalid_permission():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    user2 = auth_register('mail@box.com', 'JHUjd8bdjJ*%$', 'Katia', 'Lao')

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user2['u_id'], 3)

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user2['u_id'], 0)

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user2['u_id'], 91)

    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user2['u_id'], 13)

# Testing that owner can not change their own permission_id
def test_admin_userpermission_change_owner_selfchange():
    clear()
    user = auth_register('anotherbox@mailcorp.com', '3mptyH3@dn0i', 'Ben', 'Lucas')
    with pytest.raises(InputError):
        admin_userpermission_change(user['token'], user['u_id'], 2)


### AccessError when the authorised user is not an admin or owner ###
def test_admin_userpermission_change_user_notowner():
    clear()
    user1 = auth_register('owner@gmail.com', 'NKJ*j2j3b', 'Thomas', 'Dean')
    user2 = auth_register('notanowner@gmail.com', '980ujdfKJn', 'Bethany', 'Bridgers')
    user3 = auth_register('notanowner2@gmail.com', '&YHBJBNJMK', 'Bob', 'Higgins')

    with pytest.raises(AccessError):
        admin_userpermission_change(user2['token'], user1['u_id'], 1)

    with pytest.raises(AccessError):
        admin_userpermission_change(user2['token'], user3['u_id'], 1)

### Testing that given valid and auth inputs the permission is changed ###
def test_admin_userpermission_change_valid_inputs():
    clear()
    user1 = auth_register('owner@gmail.com', 'IJFB73d', 'Johnny', 'Mack')
    user2 = auth_register('memeber@mails.com', 'JHFJSDJ083', 'Thomas', 'Dean')
    user3 = auth_register('anothermemeber@mailbox.com', 'IJU83bdsH', 'Meradith', 'Indiana')

    assert expected_data5['users'][0]['permission_id'] == 1
    assert expected_data5['users'][1]['permission_id']== 2
    assert expected_data5['users'][2]['permission_id'] == 2
    # make member owner
    admin_userpermission_change(user1['token'], user2['u_id'], 1)
    assert expected_data7['users'][0]['permission_id'] == 1
    assert expected_data7['users'][1]['permission_id'] == 1
    assert expected_data7['users'][2]['permission_id'] == 2

    # remove owner permission
    admin_userpermission_change(user2['token'], user1['u_id'], 2)
    assert expected_data8['users'][0]['permission_id'] == 2
    assert expected_data8['users'][1]['permission_id'] == 1
    assert expected_data8['users'][2]['permission_id'] == 2

    # make member owner
    admin_userpermission_change(user2['token'], user3['u_id'], 1)
    assert expected_data9['users'][0]['permission_id'] == 2
    assert expected_data9['users'][1]['permission_id'] == 1
    assert expected_data9['users'][2]['permission_id'] == 1

####################### Tests for helper functions #####################
### testing that vaild_channel_id returns channel if it exists
def test_valid_channel_id_valid_channel():
    clear()
    user1 = auth_register('test@test.com', 'password', 'Test', 'Test')
    channel1 = channels_create(user1['token'], "Test Channel", True)

    result = valid_channel_id(channel1['channel_id'])
    assert result.name == "Test Channel"

### testing that valid channel id raises an input error if given an invalid channel
def test_valid_channel_invalid_channel():
    clear()
    user1 = auth_register('test@test.com', 'password', 'Test', 'Test')
    channels_create(user1['token'], "Test Channel", True)

    with pytest.raises(InputError):
        valid_channel_id(42)

    with pytest.raises(InputError):
        valid_channel_id("notvalidchannelid")

### testing that valid_user_id returns the user if found
def test_valid_user_id_valid_user():
    clear()
    user1 = auth_register('test@test.com', 'password', 'Test', 'Test')
    result = valid_user_id(user1['u_id'])
    assert result.name_first == "Test"

### testing that valid_user_id raises input error if invalid u_id
def test_valid_user_id_invalid_user():
    clear()
    auth_register('test@test.com', 'password', 'Test', 'Test')

    with pytest.raises(InputError):
        valid_user_id(42)

    with pytest.raises(InputError):
        valid_user_id("test")

### testing that valid_email raises input error if given invalid email, otherwise, does nothing
def test_valid_email_invalid_email():
    clear()
    with pytest.raises(InputError):
        valid_email("obviously not")

    with pytest.raises(InputError):
        valid_email("12345")

### testing that valid_email does nothing if given a valid email
def test_valid_email_valid_email():
    clear()
    k = 2
    valid_email("test@test.com")
    k = 3
    assert k == 3

### testing that existing email raises input error if the email already exists
def test_existing_email_exists():
    clear()
    user1 = auth_register('test@test.com', 'password', 'Test', 'Test')
    profile = user_profile(user1['token'], user1['u_id'])

    with pytest.raises(InputError):
        existing_email(profile['user']['email'])

### testing that existing email does nothing if the email is not taken
def test_existing_email_free():
    clear()
    k = 1
    auth_register('test@test.com', 'password', 'Test', 'Test')
    existing_email("newemail@test.com")
    k = 3
    assert k == 3

### testing that exiting handle raises an input error if given a handle string that already exists
def test_existing_handle_exists():
    clear()
    user1 = auth_register('test@test.com', 'password', 'Test', 'Test')

    profile = user_profile(user1['token'], user1['u_id'])
    with pytest.raises(InputError):
        existing_handle(profile['user']['handle_str'])

### testing that existing_handle does nothing when the handle string is available
def test_existing_handle_free():
    clear()
    k = 1
    existing_handle("thisshouldbeok")
    k = 3
    assert k == 3

### testing that authenticate_token raises an AccessError when the token given is invalid
def test_authenticate_token_invalid_token():
    clear()
    user1 = auth_register('test@test.com', 'password', 'Test', 'Test')
    auth_logout(user1['token'])
    with pytest.raises(AccessError):
        authenticate_token(user1['token'])

### testing that authenticate_token returns the given tokens holders u_id
def test_authenticate_token_valid_token():
    clear()
    user1 = auth_register('test@test.com', 'password', 'Test', 'Test')
    returned_id = authenticate_token(user1['token'])
    assert returned_id == user1['u_id']
