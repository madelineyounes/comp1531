import time
from data import data, message
from other import authenticate_token, valid_channel_id, valid_user_id
import threading
from error import InputError, AccessError
import random
from english_words import english_words_lower_alpha_set
from PyDictionary import PyDictionary


### Helper functions ###
def check_message_valid(message_id):
    """
    Given a message_id, checks if the message_id exists in the data

    Parameters:
        message_id (int): the unique identifier of a message in the system

    Return:
        {
            is_message_valid (Bool): True means that the message_id exist in the data and vice versa
            sent_msg (dict): a dictionary containing the characteristics of the message;
                             the key values being message_id, u_id, message and time_created
            msg_index (int): the index where the message_id can be found in a list of messages
            ch_index (int): the index of the channel (channel_id) where the message was found
        }
    """
    # Initializes the required return data
    is_message_valid = False
    sent_msg = {}
    ch_index = 0
    # Search for the message_id in the channel
    for channel in data.channels:
        id_check = [message.message_id for message in channel.channel_messages]
        # message id is in data
        if message_id in id_check:
            msg_index = id_check.index(message_id)
            # Get the desired return data
            sent_msg = channel.channel_messages[msg_index]
            ch_index = data.channels.index(channel)
            is_message_valid = True

    # Raise InputError if message does not exist in the data
    if is_message_valid is False:
        raise InputError(description='Invalid message id')

    # Return the results
    return {
        'is_message_valid': is_message_valid,
        'sent_msg': sent_msg,
        'msg_index': msg_index,
        'ch_index': ch_index
    }

def check_message_access(user_id, msg_check):
    """
    Checks if the given message_id is valid for editing or removing;
    It is considered valid when either of these are true:
    - request is sent by the user who sent the message
    - request is made by the channel owner where the message is located
    - request is made by the flockr owner

    Parameters:
        user_id (int): the unique identification number of the person requesting the command
        msg_check (dict): a dictionary containing the keys is_message_valid (Bool),
                          sent_msg (dict), msg_index (int) and ch_index (int)

    Return:
        {}
    """
    # Get the data needed from msg_check
    sender_u_id  = msg_check['sent_msg'].u_id
    ch_index = msg_check['ch_index']

    # Check if command is requested by the same user who sent the message
    is_user = False
    if user_id == sender_u_id:
        is_user = True

    # Check if command is forcibly requested by admin (channel owner)
    is_owner = False
    check_owner_uid = [user.u_id for user in data.channels[ch_index].owner_members]
    if user_id in check_owner_uid:
        is_owner = True

    # Check if command is forcibly requested by flockr owner
    is_flockr_owner = False
    perm_status = data.users[user_id].permission_id
    if perm_status == 1:
        is_flockr_owner = True

    # Raise AccessError is neither of the conditions are True
    if not is_owner and not is_user and not is_flockr_owner:
        raise AccessError(description='Invalid authentication')

    return {
    }

def send_msg(msg_id, user_id, message_in, channel, time_sent):
    '''
    Given the appropriate parameters, create a message dictionary with the parameters
    and append it into the data (sends the message)

    Parameters:
        msg_id (int): the unique id of a message in the system
        user_id (int): the unique id of a the user in the system
        message (str): the message which will be sent in the channel
        time_sent (int): the unix timestamp for when the message needs to be generated
        index_channel (int): the index of the channel in the data where the message needs to be sent

    Return:
        {}
    '''
    new_message = message(message_in, user_id, msg_id)
    # Alter the message time sent to remove program execution time errors
    new_message.time_created = time_sent
    channel.channel_messages.append(new_message)
    return


def check_valid_react_id(react_id):
    """
    Given a react_id, checks if the react_id is a valid React ID in the system

    Parameters:
        react_id (int): the unique id of a 'react' that will be reacted to

    Return:
        {}
    """
    # List of valid react_id that is applicable in the system
    valid_react_id = [1]
    # Raise an InputError if the react_id is invalid else do nothing
    if react_id not in valid_react_id:
        raise InputError(description="react_id is not a valid React ID")

def find_react_id_index(reacts_list, react_id):
    """
    Given a list of reacts and a react_id,
    return the index where the react_id is found in the reacts_list

    Parameters:
        reacts_list (int): list of dictionaries containing the keys;
                           react_id, u_ids, is_this_user_reacted
        react_id (int): the unique id of a 'react' that will be reacted to

    Return:
        index (int): the index where the current react_id is found in the reacts_list
    """
    for index, react_dict in enumerate(reacts_list):
        if react_dict['react_id'] == react_id:
            return index
    return -1

### Message Functions###
def message_send(token, channel_id, message_in):
    """
    Sends a message from an authenticated user to a valid channel the user is in
    Generates a message_id and returns it.

    Parameters:
        token (str): Used to authenticate and identify the user
        channel_id (int): the unique id of a channel in the system
        message (str): the message which will be sent in the channel

    Return:
        message_id (int): the unique id of a message in the system
    """

    # Check message length, raise InputError if characters in message:
    # -> length of characters > 1000
    # -> length of characters == 0 (empty message)
    if len(message_in) > 1000 or len(message_in) == 0:
        raise InputError(description='Invalid message length')

    # Check if token and channel_id exists in data
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)
    channel = valid_channel_id(channel_id)

    # Check if user is in the channel, raise AccessError if user is not in channel
    if not channel.existing_member(user):
        raise AccessError("User not in desired channel")

    # Check if message is related to hangman and edit it accordingly if it is
    msg_check = message_in.split()
    is_guess = False
    if msg_check[0] == "/guess" and channel.hangman.get_details()['mode']:
        if len(msg_check) == 2:
            message_in = msg_check[1]
            is_guess = True

    if message_in == "/hangman start" or is_guess:
        message_in = hangman(message_in, channel)


    message_id = data.message_index
    data.message_index += 1
    message_object = message(message_in, user_id, message_id)

    channel.new_message(message_object)

    return {
        'message_id': message_object.message_id
    }

def message_remove(token, message_id):
    """
    Removes a message from the channel where message_id is found,
    Function only empties out the message, it does not remove it from the whole system.

    Parameters:
        token (str): Used to authenticate and identify the user
        message_id (int): the unique id of a message in the system

    Return:
    	{}
    """
    # Check if message exists in the data
    # Function will raise InputError if message does not exist
    msg_check = check_message_valid(message_id)
    ch_index = msg_check['ch_index']

    # Check if token is valid
    user_id = authenticate_token(token)

    # Check if message_remove does not raise AccessError
    check_message_access(user_id, msg_check)

    # Removes the message from the channel
    data.channels[ch_index].channel_messages.remove(msg_check['sent_msg'])
    return {
    }

def message_edit(token, message_id, message):
    """
    Edits a message from the channel where message_id is found,
    Function willremove the messaage from the whole system if given message is empty

    Parameters:
        token (str): Used to authenticate and identify the user
        message_id (int): the unique id of a message in the system
        message (str): the string containing the new message

    Return:
    	{}
    """
    # Check if message exists in the data
    # Function will raise InputError if message does not exist
    msg_check = check_message_valid(message_id)
    ch_index = msg_check['ch_index']
    msg_index = msg_check['msg_index']

    channel = valid_channel_id(ch_index)

    # Check if token is valid
    user_id = authenticate_token(token)

    # Check if message_edit does not raise AccessError
    check_message_access(user_id, msg_check)

    # Edits the message or remove it if message is empty
    if message == '':
        channel.channel_messages.remove(msg_check['sent_msg'])
    else:
        channel.channel_messages[msg_index].update_message(message)
    return {
    }

def message_sendlater(token, channel_id, message, time_sent):
    """
    Sends a message from an authenticated user to a valid channel the user is in
    Generates a message_id and returns it at the specified time_sent in the future.

    Parameters:
        token (str): Used to authenticate and identify the user
        channel_id (int): the unique id of a channel in the system
        message (str): the message which will be sent in the channel
        time_sent (int): unix integer timestamp for a given time (consist of year, month, day and time)

    Return:
        message_id (int): the unique id of a message in the system
    """
    # Check message length, raise InputError if characters in message is invalid
    if len(message) > 1000 or len(message) == 0:
        raise InputError(description='Invalid message length')

    # Check if token is valid and channel_id exists in data
    user_id = authenticate_token(token)
    channel = valid_channel_id(channel_id)
    user = valid_user_id(user_id)


    # Check if the time_sent is not a time in the past
    cur_time = int(time.time())
    if time_sent < cur_time:
        raise InputError(description='Time sent is a time in the past')

    # Check if user is in the channel, raise AccessError if user is not in channel
    if not channel.existing_member(user):
        raise AccessError("User not in desired channel")

    # Generate message id and increment the counter in the data
    # Message_id is generated when message_sendlater is called
    msg_id = data.message_index
    data.message_index += 1

    # Send the message according to the desired time
    timer = time_sent - cur_time
    send_after = threading.Timer(timer, send_msg,
                                [msg_id, user_id, message, channel, time_sent])
    send_after.start()

    # Return the generated message_id
    return {
        'message_id': msg_id
    }

def message_react(token, message_id, react_id):
    """
    Given a valid user appointed with the token, react to an existing message under
    the user's u_id. If the given message does not have any of the react yet,
    it will create append a new dictionary for the react_id.

    Parameters:
        token (str): Used to authenticate and identify the user
        message_id (int): the unique id of a message in the system
        react_id (int): the unique id of a 'react' that will be reacted to

    Return:
    	{}
    """
    # Check if token is valid
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)

    # Check if message exists in the data
    msg_check = check_message_valid(message_id)
    ch_index = msg_check['ch_index']
    msg_index = msg_check['msg_index']
    channel = valid_channel_id(ch_index)

    # Check if user is a member of the channel where the message was posted
    if not channel.existing_member(user):
        raise InputError(description="User is not in desired channel")

    # Check if the given react_id is a valid react_id, function will raise InputError if it is invalid
    check_valid_react_id(react_id)

    # Find the current user_id in the reacts u_id list
    cur_msg = data.channels[ch_index].channel_messages[msg_index]
    is_already_reacted = False
    for react in cur_msg.reacts:
        if react['react_id'] == react_id and user_id in react['u_ids']:
            is_already_reacted = True
    # Check if the current message has not been reacted by the user previously
    if is_already_reacted is True:
        raise InputError(description="Message has already been reacted by the user")

    # Get the index of the react_id in the list of reacts
    react_index = find_react_id_index(cur_msg.reacts, react_id)

    # react_id has yet to exist in the message, create a new react dictionary
    # with the current user data to append to the reacts list
    if react_index == -1:
        new_react_dict = {}
        new_react_dict['react_id'] = react_id
        new_react_dict['u_ids'] = [user_id]
        new_react_dict['is_this_user_reacted'] = False
        cur_msg.reacts.append(new_react_dict)
    else: # Add react data on the current dictionary
        cur_react_dict = cur_msg.reacts[react_index]
        # Append the current user_id into the u_ids list
        cur_react_dict['u_ids'].append(user_id)

    # Updates the is_this_user_reacted value if the current user who reacted is the
    # same user who sent the message
    if user_id == cur_msg.u_id:
        cur_msg.reacts[react_index]['is_this_user_reacted'] = True

    return {}

def message_unreact(token, message_id, react_id):
    """
    Given a valid user appointed with the token, unreact to an already reacted message under
    the user's u_id. If the given message does not have any of the react yet,
    it will raise an InputError.

    Parameters:
        token (str): Used to authenticate and identify the user
        message_id (int): the unique id of a message in the system
        react_id (int): the unique id of a 'react' that will be reacted to

    Return:
    	{}
    """
    # Check if token is valid
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)

    # Check if message exists in the data
    msg_check = check_message_valid(message_id)
    ch_index = msg_check['ch_index']
    msg_index = msg_check['msg_index']
    channel = valid_channel_id(ch_index)

    # Check if user is a member of the channel where the message was posted
    if not channel.existing_member(user):
        raise InputError(description="User is not in desired channel")

    # Check if the given react_id is a valid react_id, function will raise InputError if it is invalid
    check_valid_react_id(react_id)

    # Find the current user_id in the reacts u_id list
    cur_msg = data.channels[ch_index].channel_messages[msg_index]
    is_reacted = False
    for react in cur_msg.reacts:
        if react['react_id'] == react_id and user_id in react['u_ids']:
            is_reacted = True
    # Check if the current message has been reacted by the user previously
    if is_reacted is not True:
        print("Here")
        raise InputError(description="Message has not been reacted by the user")

    # Get the index of the react_id in the list of reacts
    react_index = find_react_id_index(cur_msg.reacts, react_id)

    # Remove the current u_id from the u_ids list in the reacts dictionary
    cur_react_dict = cur_msg.reacts[react_index]
    cur_react_dict['u_ids'].remove(user_id)

    # Updates the is_this_user_reacted value if the current user who unreacted is the
    # same user who sent the message
    if user_id == cur_msg.u_id:
        cur_msg.reacts[react_index]['is_this_user_reacted'] = False

    # Remove the react from the whole reacts list if u_ids list is empty
    if cur_msg.reacts[react_index]['u_ids'] == []:
        cur_msg.reacts.pop(react_index)

    return {}

def message_pin(token, message_id):
    """
    Sets a message to pinned by setting is_pinned to True

    Parameters:
        token (str): Used to authenticate and identify the user
        message_id (int): the unique id of a message in the system

    Return:
    	{}
    """
    # Check if token is valid
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)

    # Check if message exists in the data
    # Function will raise InputError if message does not exist
    msg_check = check_message_valid(message_id)
    ch_index = msg_check['ch_index']
    msg_index = msg_check['msg_index']

    channel = valid_channel_id(ch_index)

    # Check if user is an owner of the channel, raise AccessError if not
    if user not in channel.owner_members:
        raise AccessError("User not not an owner inside desired channel")

    # check is pinned and set
    if not channel.channel_messages[msg_index].is_pinned:
        channel.channel_messages[msg_index].is_pinned = True
    else:
        raise InputError(description='message is already pinned')

    return {}

def message_unpin(token, message_id):
    """
    Sets a message to unpinned by setting is_pinned to False

    Parameters:
        token (str): Used to authenticate and identify the user
        message_id (int): the unique id of a message in the system

    Return:
    	{}
    """
    # Check if token is valid
    user_id = authenticate_token(token)
    user = valid_user_id(user_id)

    # Check if message exists in the data
    # Function will raise InputError if message does not exist
    msg_check = check_message_valid(message_id)
    ch_index = msg_check['ch_index']
    msg_index = msg_check['msg_index']

    channel = valid_channel_id(ch_index)

    # Check if user is an owner of the channel, raise AccessError if not
    if user not in channel.owner_members:
        raise AccessError("User not not an owner inside desired channel")

    # check is pinned and set
    if channel.channel_messages[msg_index].is_pinned:
        channel.channel_messages[msg_index].is_pinned = False
    else:
        raise InputError(description="message wasn't pinned")

    return {}

### Hangman Functions ###
def hangman(message, channel):
    """
    The main function for hangman, initalises the data and returns the new message through
    calling other functions

    Parameters:
        message (str): The message of the user
        index_channel (int): the channal_id

    Return:
        message (str): The message new message to show to the user
    """
    if message == "/hangman start":
        channel.hangman.start(str(get_word()))

    else:
        if message.isalpha():
            channel.hangman.add_guess(message)
        else:
            channel = None

    return hangman_change_message(hangman_get_info(channel))

def hangman_change_message(info):
    """
    Using the given input creates the message to display

    Parameters:
        info (dict): A dictionary containing "incorrect", "guess_string",
        "incorrect_string" and "definition"

    Return:
        message (str): The message new message to show to the user
    """
    if info['incorrect'] == 0:
        message = f"""
        HANGMAN MODE!!
        Guess a letter

        word: {info["guess_string"]}
        """
    elif info['incorrect'] == 1:
        message = f"""
        HANGMAN MODE!!





        ________

        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 2:
        message = f"""
        HANGMAN MODE!!

                |
                |
                |
                |
        ____|____

        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 3:
        message = f"""
        HANGMAN MODE!!
                 _____
                |
                |
                |
                |
        ____|____

        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 4:
        message = f"""
        HANGMAN MODE!!
                 _____
                |         |
                |
                |
                |
        ____|____

        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 5:
        message = f"""
        HANGMAN MODE!!
                 _____
                |         |
                |         0
                |
                |
        ____|____
        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 6:
        message = f"""
        HANGMAN MODE!!
                 _____
                |         |
                |         0
                |         /
                |
        ____|____
        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 7:
        message = f"""
        HANGMAN MODE!!
                 _____
                |         |
                |         0
                |         /|
                |
        ____|____
        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 8:
        message = f"""
        HANGMAN MODE!!
                 _____
                |         |
                |         0
                |         /|\\
                |
        ____|____
        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 9:
        message = f"""
        HANGMAN MODE!!
                 _____
                |         |
                |         0
                |         /|\\
                |         /
        ____|____
        word: {info["guess_string"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == 10:
        message = f"""
        HANGMAN MODE!!
        YOU LOOSE :(
                 _____
                |         |
                |         0
                |         /|\\
                |         / \\
        ____|____

        The word was: {info["guess_string"]}
        definition: {info["definition"]}
        """
    elif info['incorrect'] == -1:
        message = f"""
        HANGMAN MODE COMPLETE!!
        WELL DONE!

        word: {info["guess_string"]}
        definition: {info["definition"]}
        incorrect: {info["incorrect_string"]}
        """
    elif info['incorrect'] == -2:
        message = f"""
        PLEASE ENTER A LETTER
        """
    return message

def get_word():
    """
    Gets a word from the english_words_lower_alpha_set

    Parameters:
        None

    Return:
        word (str): The word the user will use to guess
    """
    word = random.choice(list(english_words_lower_alpha_set))
    return word

def hangman_get_info(channel):
    """
    Gets all the data needed by hangman_change_message

    Parameters:
        index_channel (int): the channal_id

    Return:{
        incorrect (int): a number representing how many times the user has guessed incorreclty,
        guess_string (str): all the correct guesses the user has made inside the word
                            with the still unknown letters represented as _,
        incorrect_string (str): all the incorect guesses the user has made,
        definition (str): the definition of the word
    }
    """
    guess_string = ""
    incorrect_string = ""
    definition = ""
    incorrect = 0
    if channel != None:
        details = channel.hangman.get_details()
        still_to_guess = False
        for letter in details['word']:
            if letter in details['guesses']:
                guess_string += letter + ' '
            else:
                guess_string += '_ '
                still_to_guess = True

        for guess in details['guesses']:
            if guess not in details['word']:
                incorrect += 1
                incorrect_string += guess + ' '


        dictionary = PyDictionary()
        if incorrect == 10:
            definition = dictionary.meaning(details['word'], disable_errors=True)
            if definition is None:
                definition = "No definition found."
            channel.hangman.end()
            guess_string = details['word']

        if not still_to_guess:
            incorrect = -1
            definition = dictionary.meaning(details['word'], disable_errors=True)
            if definition is None:
                definition = "No definition found."
            channel.hangman.end()
    else:
        incorrect = -2

    return {
        "incorrect": incorrect,
        "guess_string": guess_string,
        "incorrect_string": incorrect_string,
        "definition": definition
    }
