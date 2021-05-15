""" File for functions concering channels"""
from data import data, channel
from error import InputError, AccessError
from other import authenticate_token

def channels_list(token):
    """
    Lists all the channels a user is a part of.

    Paramaters:
    token (str): A string that validates the users actions while
                 they are logged in.

    Returns:
        {
            channels (list): A list of all the channel dicitionaries
            which the user is in.
        }
    """
    # raise InputError if inputed data is the wrong type
    if not isinstance(token, str):
        raise AccessError("Invalid token")

    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("Invalid token")

    # check that token is authorised
    token_index = authenticate_token(token)
    user_id = data.users[token_index].u_id

    channels_list_array = []
    # if user is memember add channel to list
    for channel in data.channels:
        for user in channel.all_members:
            if user.u_id == user_id:
                channels_list_array.append({'channel_id': channel.channel_id, 'name': channel.name})
                break

    return {
        'channels': channels_list_array
    }

def channels_listall(token):
    """
    Lists all the channels that exist.

    Paramaters:
    token (str): A string that validates the users actions while
                 they are logged in.

    Returns:
        {
            channels: []
        }: A list of all the channel dicitionaries.
    """
    # raise InputError if inputed data is the wrong type
    if not isinstance(token, str):
        raise AccessError("Invalid token")

    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("Invalid input")

    # check that token is authorised
    authenticate_token(token)
    
    return_list = []
    for channel in data.channels:
        return_list.append({'channel_id': channel.channel_id, 'name': channel.name})

    return {
        'channels' : return_list
    }

def channels_create(token, name, is_public):
    """
    Creates a channel.

    Paramaters:
    token (str): A string that validates the users actions while
                 they are logged in.
    name (str): A string with the name of the channel.
    is_public (boolean): A boolean indicating if the channel is
                         public or private.
    Returns:
        {
            'channel_id' : (int)
        }: A directory containg the id of the new channel.
    """
    # raise InputError if inputed data is the wrong type
    if not isinstance(token, str):
        raise AccessError("Invalid token")
    if not isinstance(name, str):
        raise InputError("Invalid input")
    if not isinstance(is_public, bool):
        raise InputError("Invalid input for bool")

    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("Invalid input")
    if name == '':
        raise InputError("Invalid input")

    # raise InputError if the name is more than 20 characters
    if len(name) > 20:
        raise InputError("Invalid input")

    # check that token is authorised
    u_id = authenticate_token(token)

    # initlise channel
    new_channel = channel(name, is_public)

    #  get user_id, first_name,last_name from token
    creator = data.users[u_id]

    new_channel.new_owner(creator)
    new_channel.new_member(creator)

    data.new_channel(new_channel)

    return {
        'channel_id' : new_channel.channel_id
    }
