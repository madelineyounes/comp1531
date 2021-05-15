import re
from data import data
from error import InputError, AccessError
import re
import jwt

def clear():
    """
    resets all attributes of data object

    Parameters: None

    Returns: None
    """
    data.users.clear()
    data.channels.clear()
    data.tokens.clear()
    data.message_index = 0
    return {}

def users_all(token):
    """
    Returns a list of all users and their associated details

    Parameters:
    	token (str): A string that validates the users actions while
    				 They are logged in

   	Returns:
   		{
   			users (list): A list of dictionaries, where each dictionary contains
                          types u_id, email, name_first, name_last, handle_str

   		}
    """

    # Check that token is valid
    authenticate_token(token)

    users = []

    for user in data.users:
        users.append(user.user_details())

    return {
        'users': users
    }

def admin_userpermission_change(token, u_id, permission_id):
    """
    Changes the user permission to that specifed.
    Parameters:
    	token (str): A string that validates the users actions while
    				 They are logged in
        u_id (int): Identification number of target
        permission_id (int): Level of authority to be given to target

   	Returns:
   		{}
    """
    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("token input empty")
    if u_id == '':
        raise InputError("u_id input empty")
    if permission_id == '':
        raise InputError("permission_id input empty")

    # raise InputError if any of the inputs is an invalid type
    if not isinstance(token, str):
        raise AccessError("token must be string")
    if not isinstance(u_id, int):
        raise InputError("u_id must be integer")
    if not isinstance(permission_id, int):
        raise InputError("permission_id must be integer")

    # check permission_id is in range
    if (permission_id != 1 and permission_id != 2):
        raise InputError("permission_id out of range")

    # check that token is authorised
    tok = authenticate_token(token)
    # check user id is valid
    target = valid_user_id(u_id)

    if (target.u_id ==  data.users[tok].u_id):
        raise InputError("user trying to change their own permission_id")
    
    print(data.users[tok].permission_id)
    if (data.users[tok].permission_id != 1):
        raise AccessError("user is not authorised to change permission_ids")

    # update permission_id
    target.permission_id = permission_id
    return {}

def search(token, query_str):
    """
    Function that searches the messages of every channel that the user
    for messages matching a query string

    Parameters:
    	token (str): for validation
        query_str (str): The string to search for

    Returns:
    	[
    		{
    			message_id (int): Unique identification of each message
    			u_id (int): Unique identification of each member
    			message (str): The string contents of the message dictionary
    			time_created (UNIX timestamp): The time at which the message was sent
    	  	}
    	]
    """
    # Authenticate token and get user id
    user_id = authenticate_token(token)

    # Get list of all channels the user is in
    all_channels = []
    query_str = re.escape(query_str) # Treats special characters as normal text
    for channel in data.channels:
        check_u_id = [user.u_id for user in channel.all_members]
        if user_id in check_u_id:
            all_channels.append(channel)

    # Search each relevent channel for messages that match the query
    return_messages = []
    for channel in all_channels:
        for message in channel.channel_messages:
            if re.search(query_str, message.message):
                return_messages.append(message.message_details())
    return {
        'messages': return_messages
    }

def valid_channel_id(channel_id):
    if not isinstance(channel_id, int) or isinstance(channel_id, bool):
        raise InputError('channel_id must be integer')

    check_channel_id = [channel.channel_id for channel in data.channels]
    if channel_id not in check_channel_id:
        raise InputError("invalid channel_id")
    return data.channels[channel_id]

def valid_user_id(u_id):
    if not isinstance(u_id, int) or isinstance(u_id, bool):
        raise InputError('user_id must be integer')
    check_u_id = [user.u_id for user in data.users]
    if u_id not in check_u_id:
        raise InputError("invalid user_id")
    return data.users[u_id]


def valid_email(email):
    """ Checks if the email format is valid
        Parameters: email(string)
        Return: None    """
    if not isinstance(email, str):
        raise InputError("Invalid Email")
    regex = '^[a-zA-Z0-9]+[/\\._-]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError("Invalid Email")

def existing_email(email):
    """ Checks if the email is already being used
        Parameters: email(string)
        Return: None    """
    check_email = [user.email for user in data.users]
    if email in check_email:
        raise InputError("Email already exists and is being used by another user")

def existing_handle(handle_str):
    """ Checks if the handle_str is already being used
        Parameters: handle_str(string)
        Return: None    """
    check_handle = [user.handle_str for user in data.users]
    if handle_str in check_handle:
        raise InputError("Handle already exists and is being used by another user")


def authenticate_token(token):

    if token not in data.tokens:
        raise AccessError("Invalid Token")

    SECRET = 'aaaaaddeeeiiklmmnnnnnorrsy'
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        user_id = payload.get("u_id")
    except:
        raise AccessError("Invalid Token")

    return user_id
