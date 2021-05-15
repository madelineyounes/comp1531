""" Functions used for individual channels """
from data import data
from other import authenticate_token
from other import valid_channel_id, valid_user_id
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    """
    Invites user into channel.

    Parameters:
        token (str): a unique token (to determine authorisation)
        channel_id(int): a unique id for such channel
        u_id (int): A unique identidier to indicate the target of this function

    Return:
        {}
    """
    # raise InputError if any of the inputs is empty
    if token == '':
        raise InputError("Invalid Input")
    if channel_id == '':
        raise InputError("Invalid Input")
    if u_id == '':
        raise InputError("Invalid Input")

    # raise InputError if any of the inputs is an invalid type
    if not isinstance(token, str):
        raise AccessError("Token must be string")
    if not isinstance(channel_id, int):
        raise InputError("Channel_id must be integer")
    if not isinstance(u_id, int):
        raise InputError("u_id must be integer")

    # check that token is authorised
    caller_id = authenticate_token(token)
    caller = valid_user_id(caller_id)
    
    # Check that target exists
    target = valid_user_id(u_id)

    # raises InputError if channel_id doesn't refer to a valid channel
    channel = valid_channel_id(channel_id)

    # raises AccessError if caller is not member of channel
    if not channel.existing_member(caller):
        raise AccessError(description = "Caller is not in target channel")

    # rasies InputError if target already a member
    if channel.existing_member(target):
        raise InputError(description = "Target is already a member.")

    # Add user to channel
    channel.new_member(target)

    # if the new_member is also a global owner they need to be added as an owner_member
    if target.permission_id == 1:
        channel.new_owner(target)

    return {
    }

def channel_details(token, channel_id):
    """
    Provides basic details about the channel a user is in.

    Parameters:
        token (str): a unique token (to determine authorisation)
        channel_id(int): a unique id for such channel

    Returns:
        {
            name (str): The name of the channel
            owner_members (list): List of dictionaries of the owner memebr of the channel,
                                  where each dictionary contains types { u_id, name_first, name_last }
            all_members (list): List of dictionaries of all the member in the channel,
                                where each dictionary contains types { u_id, name_first, name_last }
        }
    """
    # Check token and find index, aka u_id
    u_id = authenticate_token(token)
    user = valid_user_id(u_id)

    channel = valid_channel_id(channel_id)

    if not channel.existing_member(user):
        raise AccessError(description = "User not in desired channel.")

    return channel.channel_details()

def channel_messages(token, channel_id, start):
    """
    Returns a list of messages, start and end.

    Parameters:
        token (str): a unique token (to determine authorisation)
        channel_id(int): a unique id for such channel
        start (int): index indicating when the messages start

    Returns:
        {
            messages (str): the message which will be sent in the channel
            start (int): index indicating when the messages start
            end (int): index indicating when the messages end
        }
    """
    # Check that token is valid and gets it index(u_id)
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)

    # Check that channel_id is valid
    channel = valid_channel_id(channel_id)

    # Check that user is part of the desired channel
    if not channel.existing_member(user):
        raise AccessError(description = "User not in desired channel.")

    # Check that start is not greater
    # than the total number of messages in the channel and not negative
    msg_count = channel.num_messages()
    if (start > msg_count or start < 0):
        raise InputError("invalid start")

    # Initialize the desired return data
    ch_messages = {}
    ch_messages['messages'] = []

    msg_load = msg_count - start
    if msg_count == 0:  # No messages to load
        end = -1
    elif start == msg_count: # Only loads a single message if start is equal to message_count
        msg = channel.channel_messages[msg_count - 1].message_details()
        ch_messages['messages'].append(msg)
        end = -1
    elif msg_load <= 50:  # Loads all the messages in the channel if there are less than 50 messages to load
        for i in range(msg_load, start, -1):
            msg = channel.channel_messages[i - 1].message_details()
            ch_messages['messages'].append(msg)
        end = -1
    else:   # Only loads the first 50 messages if there are more than 50 messages in the channel
        for i in range(start + 50, start, -1):
            msg = channel.channel_messages[i - 1].message_details()
            ch_messages['messages'].append(msg)
        end = start + 50

    # Updates the start and end value which needs to be returned
    ch_messages['start'] = start
    ch_messages['end'] = end

    return ch_messages


def channel_leave(token, channel_id):
    """
    Removes a user from a channel,
    User should have been authenticated and should be a member of this channel

    Parameters:
        token (str): a unique token (to determine authorisation)
        channel_id(int): a unique id for such channel

    Returns:
        {}
    """
    # Check that token is valid and gets it index(u_id)
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)

    # Check that channel_id is valid
    channel = valid_channel_id(channel_id)

    # Check that user is a member of the channel
    if not channel.existing_member(user):
        raise AccessError(description = "User not in desired channel.")

    # Removes user from all_members list
    channel.remove_member(user)

    # Check if user is owner and remove from owner_members if TRUE
    if user.u_id in [user['u_id'] for user in channel.channel_details()['owner_members']]:
        channel.remove_owner(user)

    return {
    }

def channel_join(token, channel_id):
    """
    Adds a user from a channel,
    User should have been authenticated and authorised to join the channel.

    Parameters:
        token (str): a unique token (to determine authorisation)
        channel_id(int): a unique id for such channel

    Returns:
        {}
    """
    # Check that token is valid
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)

    # Check that channel_id is valid
    channel = valid_channel_id(channel_id)

    # Check that user is allowed to join
    if not channel.is_public and not user.permission_id == 1:
        raise AccessError("Channel is private, unable to join")

    # Check that the user is not in the channel yet
    if channel.existing_member(user):
        raise InputError(description = "User is already a member.")

    # Adds user to the channel
    channel.new_member(user)

    # Promote to owner if user is flockr owner
    if user.permission_id == 1:
        channel.new_owner(user)

    return {
    }

def channel_addowner(token, channel_id, u_id):
    """
    Function that adds target user as owner. If global owner, then bypass check
    of caller being an owner or target being member.

    Parameters:
    	token (str): A unique token to determine authorisation
    	channel_id (int): A unique identifier of channels
    	u_id (int): A unique identidier to indicate the target of this function

    Returns:
    	{}
    """
    # Check that token is valid
    caller_id = authenticate_token(token)
    caller = valid_user_id(caller_id)
    
    target = valid_user_id(u_id)

    # Check that channel_id is valid
    channel = valid_channel_id(channel_id)
    
    # Check that the caller is a member and an owner
    if caller.u_id not in [user['u_id'] for user in channel.channel_details()['owner_members']]:
        raise AccessError(description = "Caller is not an owner / member")

    # Check that the target is a member (If global owner, make member first)
    if not channel.existing_member(target):
        if target.permission_id == 1:
            channel.new_member(target)
        else:
            raise InputError(description = "Target is not a member")

    # Check that not targeted at an owner
    if target.u_id in [user['u_id'] for user in channel.channel_details()['owner_members']]:
        raise InputError(description = "Target is already an owner")

    # If reached, here then successful
    channel.new_owner(target)
    return {
    }


def channel_removeowner(token, channel_id, u_id):
    """
    Function that removes target user as owner. Global owner cannot be removed
    except for by another global owner.

    Parameters:
    	token (str): A unique token to determine authorisation
    	channel_id (int): A unique identifier of channels
    	u_id (int): A unique identidier to indicate the target of this function

    Returns:
    	{}
    """
    # Check that token is valid
    caller_id = authenticate_token(token)
    caller = valid_user_id(caller_id)
    
    target = valid_user_id(u_id)

    # Check that channel_id is valid
    channel = valid_channel_id(channel_id)
    
    # Check that caller is a member
    if not channel.existing_member(caller):
        raise AccessError(description = "Caller not in channel")

    # Check that access is from an owner and targeted at an owner
    if caller.u_id not in [user['u_id'] for user in channel.channel_details()['owner_members']]:
        raise AccessError(description = "Caller is not an owner")
    if target.u_id not in [user['u_id'] for user in channel.channel_details()['owner_members']]:
        raise InputError(description = "Target is not an owner")

    # Only a global owner can remove a global owner
    if caller.permission_id != 1 and target.permission_id == 1:
        raise AccessError('Need global permissions to remove global owner')

    # If reached, here then successful
    channel.remove_owner(target)
    return {
    }
