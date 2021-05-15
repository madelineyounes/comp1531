""" File for functions concering authenticating users"""
import random
import string
import re
import hashlib
import jwt
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from data import data, user
from error import InputError
from other import valid_email, existing_email

def auth_passwordreset_reset(reset_code, new_password):
    """
    Given a valid reset code, it changes the password for a user.

    Parameters:
    	reset_code (str): A code generated by auth_passwordreset_request that
                          needs to be checked against to validate the user changing
                          the password.
    	new_password (str): A security feature that needs to be checked with
    					   the password entered on registry
    Returns:
        {}
    """
    # Check password of a valid format
    # Password is less than 6 characters
    if len(new_password) < 6:
        raise InputError("Password too short.")

    # Check that the reset_code is valid
    key_valid = False
    for user in data.users:
        if user.secret_key != None:
            if user.secret_key == reset_code:
                key_valid = True
                user.password = hashlib.sha256(new_password.encode()).hexdigest()
                user.secret_key = None # invalidate key
                break
    if key_valid == False:
        raise InputError("Invalid reset code given.")
    return {}

def auth_passwordreset_request(email):
    """
    Sends user an secret code to their email.
    Parameters:
    	email (str): an email address to identify the user
   	Returns:
   		{}
    """

    # checks email is for a valid user
    valid_email(email)
    # Check email exists - If reached here, then email is valid
    email_exists = False

    for user in data.users:
        if user.email == email:
            current_user = user
            email_exists = True

    if not email_exists:
        raise InputError("No registered user with that email")

    # generates a secret key
    letdig = string.ascii_letters + string.digits
    secret_key = ''.join((random.choice(letdig) for i in range(5)))

    # stores the key in the user dictionary
    current_user.secret_key = secret_key

    # sends email with secret key
    system_email = 'testcode03@gmail.com'
    system_password = 'testcodepasword@99'

    msg =  MIMEMultipart()
    msg["Subject"] = "flockr Changing your Password"
    msg["From"] = system_email
    msg["To"] = email

    text = f"""\
    Hi {current_user.name_first},

    The code to reset your password is {secret_key}.

    This is an Automated message from Flockr. Do not reply.
    """
    msgtext = MIMEText(text, "plain")
    msg.attach(msgtext)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server_ssl:
        server_ssl.login(system_email, system_password)
        server_ssl.sendmail(system_email, email, msg.as_string())
        server_ssl.quit()

    return {}

def auth_login(email, password):
    """
    Logs in a user, generates a token for their session

    Parameters:
    	email (str): an email address to identify the user
    	password (str): A security feature that needs to be checked with
    					the password entered on registry

   	Returns:
   		{
   			u_id (int): A unique ID for each user
   			token (str): A new generated token for the user until they log out
   		}
    """
    # Check email format - Used Siennas method + test if email is string
    valid_email(email)

    # Check email exists - If reached here, then email is valid
    email_exists = False

    for item in data.users:
        if item.email == email:
            current_user = item.u_id
            email_exists = True

    if not email_exists:
        raise InputError("No registered user with that email")

    if not isinstance(password, str):
        raise InputError("Invalid password")

    # Check hashed password - If reached here, then user exists
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if not hashed_password == data.users[current_user].password:
        print(data.users[current_user].password)
        print(hashed_password)
        raise InputError("Incorrect Password")

    # Generate Token - Used Siennas method - If reached here, login successful
    token = generate_token(current_user)
    data.tokens[current_user] = token

    return {
        'u_id': current_user,
        'token': token,
    }

def auth_logout(token):
    """
    logs out a user, invalidating their token.

    Parameters:
    	token (str): A string that validates the users actions while
    				 They are logged in

    Returns:
    	{
    		is_success (bool): true/false depending on whether or not
    						  the token was valid
    	}
    """
    if token in data.tokens:
        index_token = data.tokens.index(token)

        success = True
        data.tokens[index_token] = ''
    else:
        success = False

    return {
        'is_success': success,
    }

def auth_register(email, password, name_first, name_last):
    """
    Given a user's details, create a new account for them

    Parameters:
        email (str): user input of their email
        password (str): user input of their password
        name_first (str): user input of their first name
        name_last (str): user input of their last name

    Returns:
        {
        	u_id (int):  A unique id for the user
            token (str): A string that validates the users actions while
        				 They are logged in
        }
    """
    ### Errors ###
    # Check for Invalid emails
    # Checks if email follows the above regex if not raises an error,
    # NOTE: added capitals, / and - to be allowed
    valid_email(email)

    # Email already belongs to another user
    if data.users != []:
        existing_email(email)

    # Password is less than 6 characters
    if len(password) < 6:
        raise InputError("Password too short")

    # name_first or name_last not is between 1 and 50 characters in length
    if len(name_first) > 50 or len(name_last) > 50:
        raise InputError("Name too long")

    if len(name_first) < 1 or len(name_last) < 1:
        raise InputError("No name entered")

    ### Creates the user ###
    new_user = user(email, password, name_first, name_last)

    # add the new user to the data
    data.new_user(new_user)

    ### Token generation ###
    token = generate_token(new_user.u_id)
    data.tokens.append(token)

    return {
        'u_id': new_user.u_id,
        'token': token,
    }


def generate_token(u_id):
    """
    Generates an encoded token given a user id
    Parameters:
        u_id (int): A unique ID for each user

    Returns:
        token (str): A string that validates the users actions while
                     They are logged in

    """
    SECRET = 'aaaaaddeeeiiklmmnnnnnorrsy'
    encoded_jwt = jwt.encode({'u_id':u_id}, SECRET, algorithm='HS256').decode('utf-8')

    return encoded_jwt
