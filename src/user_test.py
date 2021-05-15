""" Tests focused on functions in user.py """
import pytest
from user import user_profile_setname, user_profile_setemail
from user import user_profile_sethandle, user_profile, user_profile_uploadphoto
from error import InputError, AccessError
from other import clear
from data import data
from auth import auth_register, auth_logout
from channels import channels_create
from channel import channel_join

######################## Tests focused on user_profile #################################

def test_user_profile_single_user():
    """
    Tests that given a single registered user and a valid token,
    the user_profile function returns the correct data type
    """
    clear()
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    result = user_profile(user['token'], user['u_id'])
    assert result['user'] == {'u_id': user['u_id'],
                              'email': "test@test.com",
                              'name_first': "firstName",
                              'name_last': "lastName",
                              'handle_str': "firstnamelastname",
                              'profile_img_url': ''}

def test_user_profile_multiple_users():
    """
    Tests that given multiple registered users, and a valid token,
    the user_profile functions can choose between the users and
    return the right one
    """
    clear()
    user1 = auth_register("test1@test.com", "password1", "firstName1", "lastName1")
    user2 = auth_register("test2@test.com", "password2", "firstName2", "lastName2")
    result = user_profile(user2['token'], user1['u_id'])
    assert result['user'] == {'u_id': user1['u_id'],
                              'email': "test1@test.com",
                              'name_first': "firstName1",
                              'name_last': "lastName1",
                              'handle_str': "firstname1lastname1",
                              'profile_img_url': ''}

def test_user_profile_crosscheck():
    """
    Tests that given multiple registered users and a valid token,
    The user_profile can return data for other user and for themselves
    """
    clear()
    user = auth_register("campbell@gmail.com", "mcckaw12", "Joshua", "Campbell")
    user2 = auth_register("redwagon@yahoo.com", "meanfo21e", "Reed", "Trisha")
    user3 = auth_register("rosarin@outlook.com", "radmo201", "Rosa", "Mina")

    # Check
    result = user_profile(user['token'], user2['u_id'])
    assert result['user'] == {'u_id': user2['u_id'],
                              'email': "redwagon@yahoo.com",
                              'name_first': "Reed",
                              'name_last': "Trisha",
                              'handle_str': "reedtrisha",
                              'profile_img_url': ''}
    result = user_profile(user['token'], user3['u_id'])
    assert result['user'] == {'u_id': user3['u_id'],
                              'email': "rosarin@outlook.com",
                              'name_first': "Rosa",
                              'name_last': "Mina",
                              'handle_str': "rosamina",
                              'profile_img_url': ''}
    result = user_profile(user3['token'], user['u_id'])
    assert result['user'] == {'u_id': user['u_id'],
                              'email': "campbell@gmail.com",
                              'name_first': "Joshua",
                              'name_last': "Campbell",
                              'handle_str': "joshuacampbell",
                              'profile_img_url': ''}

def test_user_profile_invalid_token():
    """
    Tests that given a registered user and an invalid token,
    the user_profile function raises an access error
    """
    clear()
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    # Logging out invalidates your token
    auth_logout(user['token'])
    with pytest.raises(AccessError):
        user_profile(user['token'], user['u_id'])

def test_user_profile_invalid_user_id():
    """
    Tests that given a registered user and a valid token,
    the user_profile function raises an Acces Error if the u_id
    does not belong to an existing user
    """
    clear()
    user = auth_register("test@test.com", "password", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile(user['token'], -1)

def test_user_profile_logged_out():
    """
    Tests that given a registered user and a valid token,
    the user_profile function returns the correct details
    even if the target is logged out
    """
    clear()
    user1 = auth_register("test@test.com", "password", "User", "One")
    user2 = auth_register("test2@test.com", "password", "User", "Two")

    auth_logout(user1['token'])

    result = user_profile(user2['token'], user1['u_id'])
    assert result['user'] == {'u_id': user1['u_id'],
                              'email': "test@test.com",
                              'name_first': "User",
                              'name_last': "One",
                              'handle_str': "userone",
                              'profile_img_url': ''}

######################## Tests focused on user_profile_setname #################################
### Testing that given invalid inputs an InputError is generated ###

# Empty Input
def test_user_profile_setname_empty_inputs():
    clear()
    user = auth_register('EMAILS@snailmail.com', '234sdjs@dn0i', 'Ellanor', 'Page')
    with pytest.raises(InputError):
        user_profile_setname('', '', '')

    with pytest.raises(InputError):
        user_profile_setname(user['token'], '', '')

    with pytest.raises(InputError):
        user_profile_setname('', 'Ellen', '')

    with pytest.raises(InputError):
        user_profile_setname('', '', 'Paige')

    with pytest.raises(InputError):
        user_profile_setname('', 'Ellen', 'Paige')

    with pytest.raises(InputError):
        user_profile_setname(user['token'], '', 'Paige')

    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Ellen', '')

# Input into token is not a string
def test_user_profile_setname_invalid_type_token():
    clear()
    # Invalid integer input
    with pytest.raises(AccessError):
        user_profile_setname(128737, 'Jeffory', 'Beans')

    # Invalid float input
    with pytest.raises(AccessError):
        user_profile_setname(54.32, 'Jeffory', 'Beans')

    # Invalid complex input
    with pytest.raises(AccessError):
        user_profile_setname(1j, 'Jeffory', 'Beans')

    # Invalid Boolean input
    with pytest.raises(AccessError):
        user_profile_setname(True, 'Jeffory', 'Beans')

    # Invalid list input
    with pytest.raises(AccessError):
        user_profile_setname(["apple", "banana", "cherry"], 'Jeffory', 'Beans')

    # Invalid tulpe input
    with pytest.raises(AccessError):
        user_profile_setname(("apple", "banana", "cherry"), 'Jeffory', 'Beans')

    # Invalid dictionary input
    with pytest.raises(AccessError):
        user_profile_setname({"name" : "Takko", "age" : 32}, 'Jeffory', 'Beans')

# Input into name_first is not a string
def test_user_profile_setname_invalid_type_name_first():
    clear()
    user = auth_register('jbeans@mail.com', '234sdjs@dn0i', 'Jeff', 'Banzo')

    # Invalid integer input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 128737, 'Beans')

    # Invalid float input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 54.32, 'Beans')

    # Invalid complex input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 1j, 'Beans')

    # Invalid Boolean input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], True, 'Beans')

    # Invalid list input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], ["apple", "banana", "cherry"], 'Beans')

    # Invalid tulpe input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], ("apple", "banana", "cherry"), 'Beans')

    # Invalid dictionary input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], {"name" : "Takko", "age" : 32}, 'Beans')

# Input into name_last is not a string
def test_user_profile_setname_invalid_type_name_last():
    clear()
    user = auth_register('jbeans@mail.com', '234sdjs@dn0i', 'Jeff', 'Banzo')

    # Invalid integer input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Jeffory', 128737)

    # Invalid float input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Jeffory', 54.32)

    # Invalid complex input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Jeffory', 1j)

    # Invalid Boolean input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Jeffory', True)

    # Invalid list input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Jeffory', ["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Jeffory', ("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Jeffory', {"name" : "Takko", "age" : 32})

# Input token is unauthenticated and so is invalid
def test_user_profile_setname_invalid_token():
    clear()
    with pytest.raises(AccessError):
        user_profile_setname('badtoken', 'Shrek', 'Swamp')

# Input error when name_first is not inclusively between 1 and 50 characters
def test_user_profile_setname_invalid_len_name_first():
    clear()
    user = auth_register('catberry@pumkin.com', '32rmrekN!i', 'Catrina', 'Berry')
    with pytest.raises(InputError):
        user_profile_setname(user['token'], '''AveryVERYVERYYYYYYYYYYYYYYYyyyy
        yyyyyyyyyyyyyysdflkdskjflskdjfksdjflskdjfskldjfslkdfjskldfjskldfjskldj
        fslkdjfslkdfjsldkfjslkdjflskdjfslkjfslkdjfsldjslfjsdfjsldkfjsldkfjsldk
        jfslkdjfslkdjfslkdjflskdjflskdjfslkfdjsldjsljdkjflskdjfskdjfsldkfjslkd
        jfslkdjfsldkjfslkdjfldkfjsldkfjslkdjfslkdjlfksjdflksjdflskdjfslkdjfslk
        djfslkdfjslkdfjsldkjfslkdjfskdjfslkdjfslkdfjslkdfjslkdfjslkdfjslkdfjsl
        dkjfkjdkjfksjdkmawdscvlfsfmdkjfjkdsjgurewwafjdvJHnmnjdnfkdkdkfjmlkk'''\
        , 'Lemmy')

    with pytest.raises(InputError):
        user_profile_setname(user['token'], '''AveryVERYVERYYyyyyyyyyYYYYYYYYYY
        YYYYYYlongfirstname''', 'Lemmy')

    with pytest.raises(InputError):
        user_profile_setname(user['token'], '''ANEVENLONGERveryVERYVERYYyyyyyyy
        yYYYYYYYYYYYYYYYYlongfirstname''', 'Lemmy')

# Input error when name_last is not inclusively between 1 and 50 characters
def test_user_profile_setname_invalid_len_name_last():
    clear()
    user = auth_register('catberry@pumkin.com', '32rmrekN!i', 'Catrina', 'Berry')
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Catty', '''AveryVERYVERYYYYYYYYYYY
        yyyyyyyyyyyyyysdflkdskjflskdjfksdjflskdjfskldjfslkdfjskldfjskldfjskldj
        fslkdjfslkdfjsldkfjslkdjflskdjfslkjfslkdjfsldjslfjsdfjsldkfjsldkfjsldk
        jfslkdjfslkdjfslkdjflskdjflskdjfslkfdjsldjsljdkjflskdjfskdjfsldkfjslkd
        jfslkdjfsldkjfslkdjfldkfjsldkfjslkdjfslkdjlfksjdflksjdflskdjfslkdjfslk
        djfslkdfjslkdfjsldkjfslkdjfskdjfslkdjfslkdfjslkdfjslkdfjslkdfjslkdfjsl
        dkjfkjdkjfksjdkmawdscvlfsfmdkjfjkdsjgurewwafjdvJHnmnjdnfkdkdkfjmlkk'''\
        )

    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Catty', '''AveryVERYVERYYyyyyyyyyY
        YYYYYYYYYYYYYYYlongfirstname''')

    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Catty', '''ANEVENLONGERveryVERYVERYY
        yyyyyyyyYYYYYYYYYYYYYYYYlongfirstname''')

### Testing that given valid inputs the name is updated ###
def test_user_profile_setname_update():
    clear()
    user = auth_register('BassBass@kev.com', 'JKnSI3@33i', 'Kevin', 'Basta')

    user_profile_setname(user['token'], 'Kelvin', 'Boss')
    u_prof = user_profile(user['token'], user['u_id'])
    assert u_prof['user']['name_first'] == 'Kelvin'
    assert u_prof['user']['name_last'] == 'Boss'

    user_profile_setname(user['token'], 'Kaive', 'Boss')
    u_prof = user_profile(user['token'], user['u_id'])
    assert u_prof['user']['name_first'] == 'Kaive'
    assert u_prof['user']['name_last'] == 'Boss'

    user_profile_setname(user['token'], 'Kalvin', 'Beach')
    u_prof = user_profile(user['token'], user['u_id'])
    assert u_prof['user']['name_first'] == 'Kalvin'
    assert u_prof['user']['name_last'] == 'Beach'

######################## Tests focused on user_profile_setemail #################################
### Testing that given invalid inputs an InputError is generated ###

# Empty Input
def test_user_profile_setemail_empty_inputs():
    clear()
    user = auth_register('OliveS@mail.com', 'sdLnK@dn0i', 'Olive', 'Aoil')
    with pytest.raises(InputError):
        user_profile_setemail('', '')

    with pytest.raises(InputError):
        user_profile_setemail(user['token'], '')

    with pytest.raises(InputError):
        user_profile_setemail('', 'newOlivemail@mail.com')

# Input into token is not a string
def test_user_profile_setemail_invalid_type_token():
    clear()
    # Invalid integer input
    with pytest.raises(AccessError):
        user_profile_setemail(128737, 'newOlivemail@mail.com')

    # Invalid float input
    with pytest.raises(AccessError):
        user_profile_setemail(54.32, 'newOlivemail@mail.com')

    # Invalid complex input
    with pytest.raises(AccessError):
        user_profile_setemail(1j, 'newOlivemail@mail.com')

    # Invalid Boolean input
    with pytest.raises(AccessError):
        user_profile_setemail(True, 'newOlivemail@mail.com')

    # Invalid list input
    with pytest.raises(AccessError):
        user_profile_setemail(["apple", "banana", "cherry"], 'newOlivemail@mail.com')

    # Invalid tulpe input
    with pytest.raises(AccessError):
        user_profile_setemail(("apple", "banana", "cherry"), 'newOlivemail@mail.com')

    # Invalid dictionary input
    with pytest.raises(AccessError):
        user_profile_setemail({"name" : "Takko", "age" : 32}, 'newOlivemail@mail.com')

# Input into email is not a string
def test_user_profile_setemail_invalid_type_email():
    clear()
    user = auth_register('jbeans@mail.com', '234sdjs@dn0i', 'Jeff', 'Banzo')

    # Invalid integer input
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 128737)

    # Invalid float input
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 54.32)

    # Invalid complex input
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 1j)

    # Invalid Boolean input
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], True)

    # Invalid list input
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], ["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], ("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], {"name" : "Takko", "age" : 32})

# Input token is unauthenticated and so is invalid
def test_user_profile_setemail_invalid_token():
    clear()
    with pytest.raises(AccessError):
        user_profile_setemail('badtoken', 'shrek@swamp.com')

# InputError when email is an invalid format
def test_user_profile_setemail_nonvalid_email_1():
    clear()
    user = auth_register('goodmail@gmail.com', 'HJBKASK0i', 'Elsa', 'Ardenda')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'validemailgmail.org') # Missing @ symbol

def test_user_profile_setemail_nonvalid_email_2():
    clear()
    user = auth_register('goodmail@gmail.com', 'HJBKASK0i', 'Zuko', 'Flameo')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'validemail@outlookcom') # no . near end

def test_user_profile_setemail_nonvalid_email_3():
    clear()
    user = auth_register('goodmail@gmail.com', 'HJBKASK0i', 'Zuko', 'Flameo')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'validemail@.com') # @. are next to eachother

def test_user_profile_setemail_nonvalid_email_4():
    clear()
    user = auth_register('goodmail@gmail.com', 'HJBKASK0i', 'Zuko', 'Flameo')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], '@gmail.com') # no leading text

def test_user_profile_setemail_nonvalid_email_5():
    clear()
    user = auth_register('goodmail@gmail.com', 'HJBKASK0i', 'Zuko', 'Flameo')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'myemail') # no domain nor @

# Email already belongs to another user
def test_user_profile_setemail_email_preexists():
    clear()
    user1 = auth_register('yipyip@appa.com', 'IH*p3iu8sb', 'Katara', 'Waters')
    user2 = auth_register('blindbadger@earth.com', 'PAOIJ*&73b', 'Toph', 'Beifong')
    user2 = auth_register('hotdanger@firenation.com', 'PAOIJ*&73b', 'Azula', 'Flameo')

    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], 'blindbadger@earth.com')

    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], 'hotdanger@firenation.com')

    with pytest.raises(InputError):
        user_profile_setemail(user2['token'], 'yipyip@appa.com')

    with pytest.raises(InputError):
        user_profile_setemail(user2['token'], 'hotdanger@firenation.com')

### Testing that given valid inputs the email is updated ###
def test_user_profile_setemail_update():
    clear()
    user = auth_register('airyfairy@avatar.com', 'Y1ppY1ppY!!', 'Anag', 'Airno')

    user_profile_setemail(user['token'], 'hotdanger@firenation.com')
    u_prof = user_profile(user['token'], user['u_id'])
    assert u_prof['user']['email'] == 'hotdanger@firenation.com'

    user_profile_setemail(user['token'], 'yipyip@appa.com')
    u_prof = user_profile(user['token'], user['u_id'])
    assert u_prof['user']['email'] == 'yipyip@appa.com'

######################## Tests focused on user_profile_sethandle #################################
### Testing that given invalid inputs an InputError is generated ###

# Empty Input
def test_user_profile_sethandle_empty_inputs():
    clear()
    user = auth_register('OliveS@mail.com', 'sdLnK@dn0i', 'Olive', 'Aoil')
    with pytest.raises(InputError):
        user_profile_sethandle('', '')

    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], '')

    with pytest.raises(InputError):
        user_profile_sethandle('', 'newOlivemail@mail.com')

# Input into token is not a string
def test_user_profile_sethandle_invalid_type_token():
    clear()
    # Invalid integer input
    with pytest.raises(AccessError):
        user_profile_sethandle(128737, 'newOlivemail@mail.com')

    # Invalid float input
    with pytest.raises(AccessError):
        user_profile_sethandle(54.32, 'newOlivemail@mail.com')

    # Invalid complex input
    with pytest.raises(AccessError):
        user_profile_sethandle(1j, 'newOlivemail@mail.com')

    # Invalid Boolean input
    with pytest.raises(AccessError):
        user_profile_sethandle(True, 'newOlivemail@mail.com')

    # Invalid list input
    with pytest.raises(AccessError):
        user_profile_sethandle(["apple", "banana", "cherry"], 'newOlivemail@mail.com')

    # Invalid tulpe input
    with pytest.raises(AccessError):
        user_profile_sethandle(("apple", "banana", "cherry"), 'newOlivemail@mail.com')

    # Invalid dictionary input
    with pytest.raises(AccessError):
        user_profile_sethandle({"name" : "Takko", "age" : 32}, 'newOlivemail@mail.com')

# Input into handle_str is not a string
def test_user_profile_sethandle_invalid_type_handle():
    clear()
    user = auth_register('jbeans@mail.com', '234sdjs@dn0i', 'Jeff', 'Banzo')

    # Invalid integer input
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 128737)

    # Invalid float input
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 54.32)

    # Invalid complex input
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 1j)

    # Invalid Boolean input
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], True)

    # Invalid list input
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], ["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], ("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], {"name" : "Takko", "age" : 32})

# Input token is unauthenticated and so is invalid
def test_user_profile_sethandle_invalid_token():
    clear()
    with pytest.raises(AccessError):
        user_profile_sethandle('badtoken', 'new handle')

# InputError if handle_str len is less than 3 characters
def test_user_profile_sethandle_handle_str_short():
    clear()
    user = auth_register('korra@lok.com', 'AO(Jmmnpassword', 'Korra', 'Sato')

    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 'A')

    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 'Ko')

# InputError if handle_str len is greater than 20 characters
def test_user_profile_sethandle_handle_str_long():
    clear()
    user = auth_register('korra@lok.com', 'AO(Jmmnpassword', 'Korra', 'Sato')

    # 21 characters
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 'AvatarKorroRavaishere')
    # 55 characters
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], '''AvatarKorroRavaisherelettersto
        makethisareallylonghandle''')

# InputError if handle_str is used by another user
def test_user_profile_sethandle_handle_str_preexists():
    clear()
    user1 = auth_register('korra@lok.com', 'AO(Jmmnpassword', 'Korra', 'Sato')
    user2 = auth_register('assami@santocorp.com', '23fhKndsi3', 'Assami', 'Sato')

    user_profile_sethandle(user1['token'], 'asato')
    with pytest.raises(InputError):
        user_profile_sethandle(user2['token'], 'asato')

### Testing that given valid inputs an handle_str is updated ###
def test_user_profile_sethandle_update():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')

    user_profile_sethandle(user['token'], 'asato')
    u_prof = user_profile(user['token'], user['u_id'])
    assert u_prof['user']['handle_str'] == 'asato'

    user_profile_sethandle(user['token'], 'ksato')
    u_prof = user_profile(user['token'], user['u_id'])
    assert u_prof['user']['handle_str'] == 'ksato'

######################## Tests focused on user_profile_uploadphoto #################################

def test_user_profile_uploadphoto_invalid_img_url():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], "http://fake", 0, 0, 0, 0, "")

def test_user_profile_uploadphoto_x_start_out_of_range():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')
    img_url = "https://as1.ftcdn.net/jpg/02/51/65/04/500_F_251650473_YZUNKHngSbZZIaVNwATyaiflAZMWD1Dc.jpg"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, -3, 0, 50, 50, "")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 3000, 0, 50, 50, "")

def test_user_profile_uploadphoto_y_start_out_of_range():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')
    img_url = "https://as1.ftcdn.net/jpg/02/51/65/04/500_F_251650473_YZUNKHngSbZZIaVNwATyaiflAZMWD1Dc.jpg"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 0, -20, 50, 50, "")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 0, 7000, 50, 50, "")

def test_user_profile_uploadphoto_x_end_out_of_range():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')
    img_url = "https://as1.ftcdn.net/jpg/02/51/65/04/500_F_251650473_YZUNKHngSbZZIaVNwATyaiflAZMWD1Dc.jpg"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 0, 0, -10, 50, "")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 50, 0, 6000, 50, "")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 50, 0, 0, 50, "")

def test_user_profile_uploadphoto_y_end_out_of_range():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')
    img_url = "https://as1.ftcdn.net/jpg/02/51/65/04/500_F_251650473_YZUNKHngSbZZIaVNwATyaiflAZMWD1Dc.jpg"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 0, 0, 50, -10, "")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 50, 0, 50, 6000, "")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 0, 50, 100, 0, "")

def test_user_profile_uploadphoto_not_a_jpg():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')
    img_url = "https://thumbs.gfycat.com/AmpleHilariousAddax-size_restricted.gif"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], img_url, 0, 0, 50, 50, "")

def test_user_profile_uploadphoto_success():
    clear()
    user = auth_register('korra@lok.com', 'AOJmmnpassword', 'Korra', 'Sato')
    img_url = "https://as1.ftcdn.net/jpg/02/51/65/04/500_F_251650473_YZUNKHngSbZZIaVNwATyaiflAZMWD1Dc.jpg"
    user_profile_uploadphoto(user['token'], img_url, 0, 0, 200, 200, "")
    user_info = user_profile(user["token"], user["u_id"])
    assert user_info['user']["profile_img_url"] is not None

def test_user_profile_uploadphoto_after_already_in_chnnel():
    clear()
    # Register 3 users
    person1 = auth_register("Jreviendrai@gmail.net", 'pKnrV5RPevE8UkHq', 'Neelam', 'Mcculloch')
    person2 = auth_register("Lapastora@gmail.net", 'HeX3yPxdB6t35v3C', 'Zahid', 'Gordon')
    person3 = auth_register("Qaribullah@gmail.net", 'Q6k5Ntr2kTpEQzBW', 'Lilly-Ann', 'Robinson')

    # Create some channels
    channel_id = channels_create(person1['token'], "test_channel", True)
    channels_create(person2['token'], "test_channel", True)
    channel2_id = channels_create(person3['token'], "test_channel", True)

    # users join channel
    channel_join(person2['token'], channel_id['channel_id'])
    channel_join(person3['token'], channel_id['channel_id'])

    img_url = "https://as1.ftcdn.net/jpg/02/51/65/04/500_F_251650473_YZUNKHngSbZZIaVNwATyaiflAZMWD1Dc.jpg"
    user_profile_uploadphoto(person2['token'], img_url, 0, 0, 200, 200, "")

    channel_join(person2['token'], channel2_id['channel_id'])

    user_profile_uploadphoto(person2['token'], img_url, 0, 0, 50, 200, "")
    user_profile_uploadphoto(person3['token'], img_url, 0, 0, 50, 50, "")
