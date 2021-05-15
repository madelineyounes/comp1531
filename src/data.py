import hashlib
import random
import string
import time

class user:
    def __init__(self, email, password, name_first, name_last):
        self.u_id = data.num_users()
        self.email = email
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.name_first = name_first
        self.name_last = name_last
        self.secret_key = None
        self.profile_img_url = ""
        
        if data.num_users() == 0:
            self.permission_id = 1
        else:
            self.permission_id = 2
        
        handle_str = name_first.lower() + name_last.lower()
        if len(handle_str) > 20:
            handle_str = handle_str[:20]

        check_list_handles = [user.handle_str for user in data.users]

        while handle_str in check_list_handles:
            handle_add = ''.join(random.choice(string.digits) for i in range(3))
            if len(handle_str) < 18:
                handle_str += handle_add
            else:
                handle_str = handle_str[:18] + handle_add
        
        self.handle_str = handle_str

    
    def user_details(self):
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'profile_img_url': self.profile_img_url,
            'handle_str': self.handle_str
        }
    def member_details(self):
        return {
            'u_id': self.u_id,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'profile_img_url': self.profile_img_url
        }
    def update_profile_img_url(self, new_url):
        self.profile_img_url = new_url

class data_class:
    def __init__(self):
        self.users = []
        self.tokens = []
        self.channels = []
        self.message_index = 0

    def num_users(self):
        return len(self.users)

    def num_channels(self):
        return len(self.channels)
    
    def new_user(self, user):
        self.users.append(user)
    
    def new_channel(self, channel):
        self.channels.append(channel)

class channel:
    def __init__(self, name, is_public):
        self.name = name
        self.is_public = is_public
        self.owner_members = []
        self.all_members = []
        self.channel_messages = []
        self.channel_id = data.num_channels()
        self.standup_end = None
        self.standup_message = ""
        self.hangman = hangman()
    
    def num_messages(self):
        return len(self.channel_messages)
    
    def channel_details(self):
        return {
            'name': self.name,
            'owner_members': [user.member_details() for user in self.owner_members],
            'all_members': [user.member_details() for user in self.all_members]
        }
    
    def new_owner(self, user):
        self.owner_members.append(user)
    
    def new_member(self, user):
        self.all_members.append(user)
    
    def remove_owner(self, user):
        self.owner_members.remove(user)
    def existing_member(self, user):
        return user in self.all_members
    def remove_member(self, user):
        self.all_members.remove(user)
    def new_message(self, message):
        self.channel_messages.append(message)
    def standup_message_add(self, handle, message):
        self.standup_message = self.standup_message + handle + ": " + message + "\n"
    def standup_details(self):
        return {
        	'is_active': self.standup_end != None,
        	'time_finish': self.standup_end,
        	'message_queue': self.standup_message[:-1]
        }
    def standup_reset(self):
        self.standup_end = None
        self.standup_message = ""


class message:
    def __init__(self, message, u_id, message_id):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = int(time.time())
        self.is_pinned = False
        self.reacts = []
    
    def message_details(self):
        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created,
            'is_pinned': self.is_pinned,
            'reacts': self.reacts
        }
    def update_message(self, new_message):
        self.message = new_message

class hangman:
    def __init__(self):
        self.mode = False
        self.word = None
        self.guesses = []
    
    def start(self, word):
        self.mode = True
        self.word = word
        self.guesses = []

    def end(self):
        self.mode = False
        self.word = None

    
    def add_guess(self, guess):
        self.guesses.append(str(guess.lower()))
    
    def get_details(self):
        return {
            'word': self.word,
            'guesses': self.guesses,
            'mode': self.mode
        }

data = data_class()
