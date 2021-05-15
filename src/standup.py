from datetime import datetime, timedelta, timezone
from data import data
from other import valid_channel_id, authenticate_token, valid_user_id
from user import user_profile
from error import InputError, AccessError
import threading
import time
from message import message_send

""" Couldn't avoid adding a new field to channels in data. Multiple standup timers have
    to be set independently for different channels """

def timed_send(token, channel_id):
    """
    Called at the end of the timer set in the standup_start function.
    Calls message send, after checking some conditions.
    
    Parameters:
        token (str): Passed on to message_send.
        channel_id (int) Passed on to message_send. Also needed for channel data
    
    Returns:
        None
    """
    channel = valid_channel_id(channel_id)
    
    # Get standup details and reset
    standup = channel.standup_details()
    channel.standup_reset()

    # Abort if no message has been queued
    if standup['message_queue'] == "":
        return
    
    # Call message send otherwise, truncating trailing newline characters
    message_send(token, channel_id, standup['message_queue'])
    return

def standup_active(token, channel_id):
    """
    Checks if a timer to timed_send is currently running.
    
    Parameters:
        token (str): Checks that the user is validated to call the function
        channel_id (int): Needed to check the right channel
    
    Returns:
        {
            is_active (bool): Is there a standup running in that channel?
            time_finish (UNIX timestamp): If yes, when does it end, else None
        }
    """
    authenticate_token(token)
    channel = valid_channel_id(channel_id)
    standup = channel.standup_details()

    return {
        'time_finish': standup['time_finish'],
        'is_active': standup['is_active']
    }

def standup_start(token, channel_id, length):
    """
    Starts the timer that calls timed_send when it finishes
    
    Parameters:
        token (str): Check that the user is validated to call.
        channel_id (int): Specifies which channel the standup is to be in.
        length (int): Specifies the duration of the standup ( > 0).
    
    Returns:
        {
            time_finish (UNIX timestamp): When will timed_send be called?
        }
    """
    u_id = authenticate_token(token)
    user = valid_user_id(u_id)
    # Check valid channel and user belongs to channel
    channel = valid_channel_id(channel_id)
    if not channel.existing_member(user):
        raise AccessError('User is not in the target channel')

    # Check that the object is not currently running
    if standup_active(token, channel_id)['is_active']:
        raise InputError(description = "Standup already in progress")
    
    # Check length is positive
    if length <= 0:
        raise InputError("Duration must be positive")
    
    # Start the timer if reached here
    timer = threading.Timer(length, timed_send, [token, channel_id])
    timer.start()
    current_time = int(time.time())
    added = current_time + length
    channel.standup_end = added

    return {
        'time_finish': channel.standup_end
    }


def standup_send(token, channel_id, message):
    """
    Add a message to the queue that will be collated after the timer tuns out
    
    Parameters:
        token (str): Check that the user is validated to call.
        channel_id (int): Specifies which channel the standup is to be in.
        message (str): The message that is to be added.
    
    returns: {}
    """
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)
    channel = valid_channel_id(channel_id)
    standup = channel.standup_details()
    
    # Check that user is in this channel
    if not channel.existing_member(user):
        raise AccessError('User is not in the target channel')

    # Checking for invalid input
    if len(message) > 1000:
        raise InputError(description = "Mesage too long")

    # Check that the timer is running
    if standup['time_finish'] is None:
        raise InputError(description = "Standup not active")

    # Get senders handle
    handle = user_profile(token, user_id)['user']['handle_str']
    
    # Add the message queue
    channel.standup_message_add(handle, message)
    return {}
