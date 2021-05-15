import hashlib

expected_data1 = {
    'numUsers': 3,
    'users': [
        {
            'u_id': 0,
            'email': 'WICKEDER@yahoo.org',
            'password': hashlib.sha256('123abc!@#'.encode()).hexdigest(),
            'name_first': 'Cosmo',
            'name_last': 'Kearns',
            'handle_str': 'cosmokearns',
            'profile_img_url': "",
            'permission_id': 1,
        },
        {
            'u_id': 1,
            'email': 'RenameLHC@yahoo.org',
            'password': hashlib.sha256('123abc!@#'.encode()).hexdigest(),
            'name_first': 'Abida',
            'name_last': 'Zhang',
            'handle_str': 'abidazhang',
            'profile_img_url': "",
            'permission_id': 2,
        },
        {
            'u_id': 2,
            'email': "repeatin-rifle@yahoo.org",
            'password': hashlib.sha256('123abc!@#'.encode()).hexdigest(),
            'name_first': 'Brenden',
            'name_last': 'Partridge',
            'handle_str': 'brendenpartridge',
            'profile_img_url': "",
            'permission_id': 2,
        },
    ],
}

expected_data2 = {
    'numUsers': 1,
    'users': [
        {
            'u_id': 0,
            'email': 'hello@yahoo.org',
            'password': hashlib.sha256('12sdf3abcsf!@#'.encode()).hexdigest(),
            'name_first': 'sudifhsdfhssdsdfsoifusdfs',
            'name_last': 'Arsdfsdfwxefefchsdfsdsdfer',
            'handle_str': 'sudifhsdfhssdsdfsoif',
            'profile_img_url': "",
            'permission_id': 1,
        },
    ],
}

expected_data3 = {
    'numUsers': 1,
    'users': [
        {
            'u_id': 0,
            'email': 'MarioKart@yahoo.org',
            'password': hashlib.sha256('123abc!@#'.encode()).hexdigest(),
            'name_first': 'Lugi',
            'name_last': 'Mario',
            'handle_str': 'lugiKart',
            'profile_img_url': "",
            'permission_id': 1,
        }
    ],
    'tokens': [],
    'numChannels': 1,
    'channels': [
        {
            'channel_id': 0,
            'name': 'testchannelname',
            'is_public': True,
            'owner_members': [
                {
                    'u_id': 0,
                    'name_first': 'Lugi',
                    'name_last': 'Mario',
                }
            ],
            'all_members': [
                {
                   'u_id': 0,
                   'name_first': 'Lugi',
                   'name_last': 'Mario',
                }
            ],
            'channel_messages': [
                {}
            ]
        }
    ],
}

expected_data4 = {
    'numUsers': 1,
    'users': [
        {
            'u_id': 0,
            'email': 'MarioKart@yahoo.org',
            'password': hashlib.sha256('123abc!@#'.encode()).hexdigest(),
            'name_first': 'Lugi',
            'name_last': 'Mario',
            'handle_str': 'lugiKart',
        }
    ],
    'tokens': [],
    'numChannels': 1,
    'channels': [
        {
            'channel_id': 0,
            'name': 'testchannelname1',
            'is_public': True,
            'owner_members': [
                {
                    'u_id': 0,
                    'name_first': 'Lugi',
                    'name_last': 'Mario',
                }
            ],
            'all_members': [
                {
                   'u_id': 0,
                   'name_first': 'Lugi',
                   'name_last': 'Mario',
                }
            ],
            'channel_messages': [
                {}
            ]
        },
        {
            'channel_id': 1,
            'name': 'testchannelname2',
            'is_public': False,
            'owner_members': [
                {
                    'u_id': 0,
                    'name_first': 'Lugi',
                    'name_last': 'Mario',
                }
            ],
            'all_members': [
                {
                   'u_id': 0,
                   'name_first': 'Lugi',
                   'name_last': 'Mario',
                }
            ],
            'channel_messages': [
                {}
            ]
        }
    ],
}

expected_data5 = {
    'users': [
        {
            'u_id': 0,
            'email': 'WICKEDER@yahoo.org',
            'name_first': 'Cosmo',
            'name_last': 'Kearns',
            'handle_str': 'cosmokearns',
            'permission_id': 1,
            'profile_img_url': ""
        },
        {
            'u_id': 1,
            'email': 'RenameLHC@yahoo.org',
            'name_first': 'Abida',
            'name_last': 'Zhang',
            'handle_str': 'abidazhang',
            'permission_id': 2,
            'profile_img_url': ""
        },
        {
            'u_id': 2,
            'email': "repeatin-rifle@yahoo.org",
            'name_first': 'Brenden',
            'name_last': 'Partridge',
            'handle_str': 'brendenpartridge',
            'permission_id': 2,
            'profile_img_url': ""
        },
    ],
}

expected_data6 = {
    'users': [
        {
            'u_id': 0,
            'email': 'hello@yahoo.org',
            'name_first': 'sudifhsdfhssdsdfsoifusdfs',
            'name_last': 'Arsdfsdfwxefefchsdfsdsdfer',
            'handle_str': 'sudifhsdfhssdsdfsoif',
            'profile_img_url': ""
        }
    ],
}

expected_data7 = {
    'numUsers': 3,
    'users': [
        {
            'u_id': 0,
            'email': 'owner@gmail.com',
            'password': hashlib.sha256('IJFB73d'.encode()).hexdigest(),
            'name_first': 'Johnny',
            'name_last': 'Mack',
            'handle_string': 'johnnymack',
            'permission_id': 1,
        },
        {
            'u_id': 1,
            'email': 'memeber@mails.com',
            'password': hashlib.sha256('JHFJSDJ083'.encode()).hexdigest(),
            'name_first': 'Thomas',
            'name_last': 'Dean',
            'handle_string': 'thomasdean',
            'permission_id': 1,
        },
        {
            'u_id': 2,
            'email': 'anothermemeber@mailbox.com',
            'password': hashlib.sha256('IJU83bdsH'.encode()).hexdigest(),
            'name_first': 'Meradith',
            'name_last': 'Indiana',
            'handle_string': 'meradithindiana',
            'permission_id': 2,
        }
    ],
}

expected_data8 = {
    'numUsers': 3,
    'users': [
        {
            'u_id': 0,
            'email': 'owner@gmail.com',
            'password': hashlib.sha256('IJFB73d'.encode()).hexdigest(),
            'name_first': 'Johnny',
            'name_last': 'Mack',
            'handle_string': 'johnnymack',
            'permission_id': 2,
        },
        {
            'u_id': 1,
            'email': 'memeber@mails.com',
            'password': hashlib.sha256('JHFJSDJ083'.encode()).hexdigest(),
            'name_first': 'Thomas',
            'name_last': 'Dean',
            'handle_string': 'thomasdean',
            'permission_id': 1,
        },
        {
            'u_id': 2,
            'email': 'anothermemeber@mailbox.com',
            'password': hashlib.sha256('IJU83bdsH'.encode()).hexdigest(),
            'name_first': 'Meradith',
            'name_last': 'Indiana',
            'handle_string': 'meradithindiana',
            'permission_id': 2,
        }
    ],
}

expected_data9 = {
    'numUsers': 3,
    'users': [
        {
            'u_id': 0,
            'email': 'owner@gmail.com',
            'password': hashlib.sha256('IJU83bdsH'.encode()).hexdigest(),
            'name_first': 'Johnny',
            'name_last': 'Mack',
            'handle_string': 'johnnymack',
            'permission_id': 2,
        },
        {
            'u_id': 1,
            'email': 'memeber@mails.com',
            'password': hashlib.sha256('JHFJSDJ083'.encode()).hexdigest(),
            'name_first': 'Thomas',
            'name_last': 'Dean',
            'handle_string': 'thomasdean',
            'permission_id': 1,
        },
        {
            'u_id': 2,
            'email': 'anothermemeber@mailbox.com',
            'password': hashlib.sha256('IJU83bdsH'.encode()).hexdigest(),
            'name_first': 'Meradith',
            'name_last': 'Indiana',
            'handle_string': 'meradithindiana',
            'permission_id': 1,
        }
    ],
}
