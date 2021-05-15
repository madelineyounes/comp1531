'''
data = {
    'numUsers': 0,
    'users': [
        {
            'u_id': ,                           #(integer)
            'email': ,                          #(string)
            'password': ,                       #(string)
            'name_first': ,                     #(string)
            'name_last': ,                      #(string)
            'handle_str': ,                     #(string)
            'permission_id': ,                  #(integer)
            'profile_img_url': ,                #(str)
        },
    ],
    'tokens': [],
    'numChannels': 0,
    'channels': [
        {
            'hangman_mode': ,                   #(bool)
            'hangman_word': ,                   #(str)
            'hangman_guesses': [],              #(list of str)
            'channel_id': ,                     #(integer)
            'name': ,                           #(string)
            'is_public': ,                      #(boolen)
            'owner_members': [
                {
                    'u_id': ,                   #(integer)
                    'name_first': ,             #(string)
                    'name_last':  ,             #(string)
                }
            ],
            'all_members': [
                   {
                    'u_id':  ,                  #(integer)
                    'name_first': ,             #(string)
                    'name_last':  ,             #(string)
                }
            ],
            'channel_messages':
                {
                    'messages': [
                        {
                            'message_id': ,     #(integer)
                            'u_id': ,           #(integer)
                            'message': ,        #(string)
                            'time_created': ,   #(integer UNIX time stamp)
                        }
                    ],
                    'counter': ,                  #(integer)
                },
        }
    ],
}
'''
