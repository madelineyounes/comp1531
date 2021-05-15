""" Tests focused on functions in auth.py """

import pytest
import jwt
from data import data
from auth import auth_login, auth_logout, auth_register
from auth import generate_token, auth_passwordreset_reset, auth_passwordreset_request
from error import InputError
from other import clear


######################## Tests focused on auth_logout #################################

# Invalid token should return False
def test_auth_logout_invalid_token():
    clear()
    registered = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    assert registered['token'] is not None
    result = auth_logout('invalidToken')
    assert not result['is_success']


# Valid token should return True and invalidate the token
def test_auth_logout_valid_token():
    clear()
    registered = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    assert registered['token'] is not None
    result = auth_logout(registered['token']) # Can't possibly be wrong
    assert result['is_success']

    secondAttempt = auth_logout(registered['token']) # Should now be invalid
    assert not secondAttempt['is_success']


######################## Tests focused on auth_login #################################


# Invalid Email format should cause InputError
def test_auth_login_invalid_email_format():
    clear()
    with pytest.raises(InputError):
        auth_login('notcorrectformat', 'testPassword') # not an email


# Valid email format should work fine
def test_auth_login_valid_email_format():
    clear()
    auth_register('test@test.com', 'password', 'firstName', 'lastName')
    result = auth_login('test@test.com', 'password')
    assert result['u_id'] is not None
    assert result['token'] is not None


# Unregistered email should cause error
def test_auth_login_unregistered_email():
    clear()
    with pytest.raises(InputError):
        auth_login('test@validbutunregistered.com', 'password') # Nothing yet registered


# Incorrect password should cause error
def test_auth_login_incorrect_password():
    clear()
    auth_register('test@test.com', 'password', 'firstName', 'lastName')
    with pytest.raises(InputError):
        auth_login('test@test.com', 'incorrectPassword')


# Incorrect Input type for email should cause error
def test_auth_login_invalid_email_type():
    clear()
    auth_register('test@test.com', 'password', 'firstName', 'lastName')

    # Invalid integer input
    with pytest.raises(InputError):
        auth_login(128737, 'password')

    # Invalid float input
    with pytest.raises(InputError):
        auth_login(54.32, 'password')

    # Invalid complex input
    with pytest.raises(InputError):
        auth_login(1j, 'password')

    # Invalid Boolean input
    with pytest.raises(InputError):
        auth_login(True, 'password')

    # Invalid list input
    with pytest.raises(InputError):
        auth_login(["apple", "banana", "cherry"], 'password')

    # Invalid tulpe input
    with pytest.raises(InputError):
        auth_login(("apple", "banana", "cherry"), 'password')

    # Invalid dictionary input
    with pytest.raises(InputError):
        auth_login({"name" : "Takko", "age" : 32}, 'password')



# Incorrect Input type for password should cause error
def test_auth_login_invalid_password_type():
    clear()
    registered = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    assert registered['token'] is not None

    # Invalid integer input
    with pytest.raises(InputError):
        auth_login('test@test.com', 128737)

    # Invalid float input
    with pytest.raises(InputError):
        auth_login('test@test.com', 54.32)

    # Invalid complex input
    with pytest.raises(InputError):
        auth_login('test@test.com', 1j)

    # Invalid Boolean input
    with pytest.raises(InputError):
        auth_login('test@test.com', True)

    # Invalid list input
    with pytest.raises(InputError):
        auth_login('test@test.com', ["apple", "banana", "cherry"])

    # Invalid tulpe input
    with pytest.raises(InputError):
        auth_login('test@test.com', ("apple", "banana", "cherry"))

    # Invalid dictionary input
    with pytest.raises(InputError):
        auth_login('test@test.com', {"name" : "Takko", "age" : 32})


# An Empty Input should cause error
def test_auth_login_empty():
    clear()
    registered = auth_register('test@test.com', 'password', 'firstName', 'lastName')
    assert registered['token'] is not None
    # email and password empty
    with pytest.raises(InputError):
        auth_login('', '')

    # Password empty
    with pytest.raises(InputError):
        auth_login('test@test.com', '')

    # Email empty
    with pytest.raises(InputError):
        auth_login('', 'password')


######################################## Tests for auth_register ########################################

# Testing if the function returns something
def test_auth_register_simple_return():
    clear()
    result = auth_register('Valid/email@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert result is not None
    assert result['u_id'] is not None
    assert result['token'] is not None

# Tests for Non vaild emais
def test_auth_register_nonvalid_email_1():
    clear()
    with pytest.raises(InputError):
        auth_register('validemailgmail.org', 'wEM*TUX5xF]P_gSR', 'Liam', 'Tate') # Missing @ symbol

def test_auth_register_nonvalid_email_2():
    clear()
    with pytest.raises(InputError):
        auth_register('validemail@outlookcom', 'Wbmj4CRn', 'Devon', 'Devon') # no . near end

def test_auth_register_nonvalid_email_3():
    clear()
    with pytest.raises(InputError):
        auth_register('validemail@.com', '8pts3SKY', 'Rumaisa', 'James') # @. are next to eachother

def test_auth_register_nonvalid_email_4():
    clear()
    with pytest.raises(InputError):
        auth_register('@gmail.com', '"e"WsEbPx*qk}uhYF9kj', 'Arun', 'Snyder') # no leading text

def test_auth_register_nonvalid_email_5():
    clear()
    with pytest.raises(InputError):
        auth_register('', 'z.n&MTv9gN[-', 'Oskar', 'Woolley') # no email at all

def test_auth_register_nonvalid_email_6():
    clear()
    with pytest.raises(InputError):
        auth_register('myemail', 'Ratsgcdjue(;c}', 'Mine', 'Atrian') # no domain nor @


# Email already belongs to another user
def test_auth_register_email_already_used():
    clear()
    auth_register('Besera@gmail.com', 'BXeeyr%K4;X+Z', 'Oskar', 'Woolley')
    with pytest.raises(InputError):
        auth_register('Besera@gmail.com', 'AQZ>K_n>`5V*^', 'Jia', 'Werner')


# Password is less than 6 characters
def test_auth_register_password_too_short():
    clear()
    with pytest.raises(InputError):
        auth_register('herruling@yahoo.com', 'z.n', 'Saim', 'Saim')
    with pytest.raises(InputError):
        auth_register('herrug@yahoo.com', '12345', 'Saihm', 'Saim')

# No password was given
def test_auth_register_no_password():
    clear()
    with pytest.raises(InputError):
        auth_register('miyaknee@gmail.com', '', 'Miya', 'Knee')

# Name_first not is between 1 and 50 characters in length
def test_auth_register_no_first_name():
    clear()
    with pytest.raises(InputError):
        auth_register('unshattered@gmail.com', 'z.n&MTv9gN[-', '', 'Moses')

def test_auth_register_long_first_name():
    clear()
    with pytest.raises(InputError):
        auth_register('Rhod.endron@yahoo.com', ']m7CKC~7w:NpW', 'OskarAlstonAlstonNorthOskarAlstonAlstonNorth123455Kain', 'Britt')

# Name_last is not between 1 and 50 characters in length
def test_auth_register_no_last_name():
    clear()
    with pytest.raises(InputError):
        auth_register('momsinthecity@yahoo.net', 'ZsWnYJpyGNVNH', 'Oskar', '')

def test_auth_register_long_last_name():
    clear()
    with pytest.raises(InputError):
        auth_register("777-200ERs@gmail.com", 'RpVGkZCakugaz', 'CynthiaKemp124fghfgh',\
         'ufgbceuyrceuecfhsukehfudhfsehfcufgbceuyrceuecfhsukehfudhfsehfcufgbceuyrceuecfhsukehfudhfsehfc')

# No first_name and last_name was given
def test_auth_register_no_name():
    clear()
    with pytest.raises(InputError):
        auth_register("777-200ERs@gmail.com", 'RpVGkZCakugaz', '', '')

# Null input
def test_auth_register_null_input():
    clear()
    with pytest.raises(InputError):
        auth_register('', '', '', '') # All input is blank

# Everything is incorrect
def test_auth_register_all_input_is_wrong():
    clear()
    with pytest.raises(InputError):
        auth_register('hdags.com', '345', 'OskarAlstonAlstondfgdfdghf4575NorthOskarAlstonAlstonNorth123455Kain',\
         'ufgbceuyrceuecfhsukehfudhfsehfcufgbceuyrceuecfhsukehfudhfsehfcufgbceuyrceuecfhsukehfudhfsehfc')

# Check account is created aka check other functoions work after used
def test_auth_register_check_with_logout():
    clear()
    result = auth_register('Lindsfor@gmail.net', 'AE_>)_rg:V7vyrEG', 'Meera', 'Franklin')
    assert auth_logout(result['token']) # If user is created then they can be logged out

# Check it works with handle over 20 characters - cant check if the handle is correct yet
# becuase none of the user functions will be implemented in iteration 1
def test_auth_register_long_handle():
    clear()
    result = auth_register("ZAH-kee@gmail.com", 'DZVznKzzuPnjc', 'AlexieAlexieAlexie', 'Evie-Mae')
    assert auth_logout(result['token'])

# Check if it works when handle is already used
def test_auth_register_handle_already_used():
    clear()
    auth_register("ZAH-kee@gmail.com", 'P?=Hfu$xK<`Qt', 'Alexie', 'Evie')
    result = auth_register("topothefold@gmail.com", 'DZVznKzzuPnjc', 'Alexie', 'Evie') # alexieevie would be the handle for both hopefully its changed
    assert auth_logout(result['token'])

def test_auth_register_handle_already_used_long():
    clear()
    auth_register("ZAH-kee@gmail.com", 'P?=Hfu$xK<`Qt', 'AlexieAlexieAlexieAlexie', 'Evie')
    result = auth_register("topothefold@gmail.com", 'DZVznKzzuPnjc', 'AlexieAlexieAlexieAlexie', 'Evie')
    assert auth_logout(result['token'])

# Adding several users in a row
def test_auth_register_several_users():
    clear()
    result1 = auth_register('WICKEDER@yahoo.org', '123abc', 'Cosmo', 'Kearns')
    result2 = auth_register('RenameLHC@yahoo.org', '123abc!@#', 'A', 'Zhang')
    result3 = auth_register("repeatin-rifle@yahoo.org", '123abc!@#', 'BrendenBrendenBrendenBrendenBrendenBrendenBrendena', 'Partridge')
    assert auth_logout(result1['token'])
    assert auth_logout(result2['token'])
    assert auth_logout(result3['token'])

######################################## Tests for generate token ########################################
# Check that generate token returns an encoded token that can be decoded to return original input
def test_generate_token():
    SECRET = 'aaaaaddeeeiiklmmnnnnnorrsy'
    clear()
    token = generate_token(0)

    decoded = jwt.decode(token, SECRET, algorithms = 'HS256')
    assert decoded['u_id'] == 0

# Check that a few encoded tokens are not the same
def test_generate_token_uniqueness():
    clear()
    token1 = generate_token(0)
    token2 = generate_token(1)
    token3 = generate_token(2)
    token4 = generate_token(3)
    token5 = generate_token(4)
    token6 = generate_token(5)
    token7 = generate_token(6)

    tokens = [token1, token2, token3, token4, token5, token6, token7]

    assert len(tokens) == len(set(tokens))

######################## Tests focused on auth_passwordreset_request #################################
### Testing that given invalid inputs an InputError is generated ###
# Invalid Email format should cause InputError
def test_auth_passwordreset_request_invalid_email_format():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_request('notcorrectformat') # not an email

# Unregistered email should cause error
def test_auth_passwordreset_request_unregistered_email():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_request('test@validbutunregistered.com')


def test_auth_passwordreset_request_unregistered_email_muplitple_users():
    clear()
    auth_register('madeline.younes@gmail.com', 'password', 'madeline', 'younes')
    auth_register('user.2@gmail.com', '238hadJHJ', 'Mira', 'Bankstone')
    auth_register('user.3@gmail.com', '82hBKH', 'Thomas', 'Yossef')

    with pytest.raises(InputError):
        auth_passwordreset_request('test@validbutunregistered.com')

### Testing that given valid inputs an email is sent ###
# whitebox test to check that a secret code is assigned to the user
def test_auth_passwordreset_request_key_generated():
    clear()
    auth_register('madeline.younes@gmail.com', 'password', 'madeline', 'younes')

    for curr_user in data.users:
        if curr_user.email == 'madeline.younes@gmail.com':
            break

    curr_user.secret_key = None
    auth_passwordreset_request('madeline.younes@gmail.com')
    assert curr_user.secret_key is not None
# Invalid secret code cause InputError
def test_auth_passwordreset_reset_invalid_reset_code():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_reset('incorrect_code', 'newpassword')

def test_auth_passwordreset_reset_invalid_reset_code_manyuser():
    clear()
    auth_register('test1@gmail.com', 'password1', 'Test1', 'User')
    auth_register('test2@gmail.com', 'password2', 'Test2', 'User')
    auth_register('test3@gmail.com', 'password3', 'Test3', 'User')
    auth_register('test4@gmail.com', 'password4', 'Test4', 'User')
    auth_register('test5@gmail.com', 'password5', 'Test5', 'User')
    auth_passwordreset_request('test2@gmail.com')
    auth_passwordreset_request('test3@gmail.com')
    auth_passwordreset_request('test5@gmail.com')

    with pytest.raises(InputError):
        auth_passwordreset_reset('incorrect_code', 'newpassword')

######################## Tests focused on auth_passwordreset_reset #################################
# Invalid password should cause error
def test_auth_passwordreset_reset_invalid_password():
    clear()
    with pytest.raises(InputError):
        auth_passwordreset_reset('correct_code',  'z.n')

### Testing that given valid inputs an email is sent ###
# Test using auth_passwordreset_request
def test_auth_passwordreset_reset_success():
    clear()
    auth_register('madeline.younes@gmail.com', 'password', 'Madeline', 'Younes')
    auth_passwordreset_request('madeline.younes@gmail.com')
    for user in data.users:
        if user.email == 'madeline.younes@gmail.com':
            reset_code = user.secret_key
    auth_passwordreset_reset(reset_code, 'New_3dpassword')

# Whitebox test
def test_auth_passwordreset_reset_success_whitebox():
    clear()
    auth_register('whiteboxtest@gmail.com', 'password23s', 'Box', 'White')
    for user in data.users:
        if user.email == 'whiteboxtest@gmail.com':
            user.secret_key = '2Djk8'

    auth_passwordreset_reset('2Djk8', 'New_3dpassword')
