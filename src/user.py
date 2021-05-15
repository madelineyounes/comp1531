from error import InputError, AccessError
from other import clear, existing_email, valid_email, valid_user_id
from other import existing_handle, authenticate_token
from data import data

import jwt
import urllib
from PIL import Image

def user_profile(token, u_id):
    """
    Function that returns the profile of the
    user with the given u_id as a dictionary.

    Parameters:
    	token (str): Used to validate the users login session

    Return:
    	{
            user: {
        		u_id (int): Unique identification number of target
        		email (str): email address of target
        		name_first (str): first name of target
        		name_last (str): last name of target
        		handle_str (str): Not sure what this is used for
            },
    	}
    """
    valid_user_id(u_id)
    authenticate_token(token)

    return {
    	'user': data.users[u_id].user_details()
    }

def user_profile_setname(token, name_first, name_last):
    """
    Changes and sets users first and last name.
    Parameters:
        token(str): A string that validates the users actions while
    				 they are logged in
        name_first(str): The new first name of user
        name_last(string): The new last name of user

    Returns: None
    """
    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("token input left empty")
    if name_first == '':
        raise InputError("name_first left empty")
    if name_last == '':
        raise InputError("name_last left empty")

    # raise InputError if any of the inputs is an invalid type
    if not isinstance(token, str):
        raise AccessError("token of wrong data type")
    if not isinstance(name_first, str):
        raise InputError("name_first of wrong data type")
    if not isinstance(name_last, str):
        raise InputError("name_last of wrong data type")

    # name_first is not between 1 and 50 characters or
    # name_last is not between 1 and 50 characters
    if (len(name_first) > 50 or len(name_first) < 1):
        raise InputError("name_first length is out of range")
    if (len(name_last) > 50 or len(name_last) < 1):
        raise InputError("name_last length is out of range")

    # check that token is authorised
    tok = authenticate_token(token)

    user = data.users[tok]

    user.name_first = name_first
    user.name_last = name_last
    return {
    }

def user_profile_setemail(token, email):
    """
    Changes and sets user's email.
    Parameters:
        token(str): A string that validates the users actions while
    				 They are logged in
        email(str): The new email of the user
    Returns: None
    """
    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("token input left empty")
    if email == '':
        raise InputError("email input left empty")

    # raise InputError if any of the inputs is an invalid type
    if not isinstance(token, str):
        raise AccessError("token of wrong data type.")
    if not isinstance(email, str):
        raise InputError("email of wrong data type.")

    # Checks that email is in valid format
    valid_email(email)
    # Checks that email is not being used by another user
    existing_email(email)

    # check that token is authorised
    tok = authenticate_token(token)

    user = data.users[tok]
    user.email = email
    return {
    }

def user_profile_sethandle(token, handle_str):
    """
    Changes and sets user's handle_str.
    Parameters:
        token(str): A string that validates the users actions while
    				they are logged in
        handle_str(str): The handle the user wants to change to

    Returns: None
    """
    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("Token input left empty")
    if handle_str == '':
        raise InputError("Handle_str input left empty")

    # raise InputError if any of the inputs is an invalid type
    if not isinstance(token, str):
        raise AccessError("Invalid Token")
    if not isinstance(handle_str, str):
        raise InputError("Invalid Email")

    # raises an error if the handle is not of the required length
    if len(handle_str) < 3:
        raise InputError("handle string too short")
    elif len(handle_str) > 20:
        raise InputError("handle string too long")

    # check that token is authorised
    tok = authenticate_token(token)
    # check that handle_str is not being used by another user
    existing_handle(handle_str)

    user = data.users[tok]
    user.handle_str = handle_str
    return {
    }


def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, host_url):
    """
    Upoloads a photo for the users profile.

    Parameters:
        token(str): A string that validates the users actions while
    				they are logged in
        img_url(str): URL of an image on the internet
        x_start(int): x position to start cropping
        y_start(int): y position to start cropping
        x_end(int): x position to end cropping
        y_end(int): y position to end cropping

    Returns: {}
    """
    # check that token is authorised
    user_id = authenticate_token(token)

    path = "src/static/profile_img_for_" + str(user_id) + ".jpg"
    # get image
    try:
        urllib.request.urlretrieve(img_url, path)
    except:
        raise InputError("invalid url")

    img = Image.open(path)
    width, height = img.size

    if x_start < 0 or x_start > width:
        raise InputError("Invalid x_start")
    elif y_start < 0 or y_start > height:
        raise InputError("Invalid y_start")
    elif x_end > width or x_end < x_start:
        raise InputError("Invalid x_end")
    elif y_end > height or y_end < y_start:
        raise InputError("Invalid x_end")

    if img.format != "JPEG":
        raise InputError("not a JPEG file")

    img_cropped = img.crop((x_start, y_start, x_end, y_end))
    img_cropped.save(path)

    data.users[user_id].update_profile_img_url(host_url + path)

    return {}
