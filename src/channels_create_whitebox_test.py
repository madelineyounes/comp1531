""" commented out as they are whitebox tests from when the other functions weren't implemented
from data import data
from other import clear
from expected_data import expected_data3, expected_data4
from channels import channels_create
from auth import auth_register

def test_channels_create_simple():
    clear()
    user = auth_register('MarioKart@yahoo.org', '123abc!@#', 'Lugi', 'Mario')
    channels_create(user['token'], 'testchannelname', True)

    assert data['channels'][0]['channel_id'] == expected_data3['channels'][0]['channel_id']
    assert data['channels'][0]['name'] == expected_data3['channels'][0]['name']
    assert data['channels'][0]['is_public'] == expected_data3['channels'][0]['is_public']

    assert data['channels'][0]['owner_members'][0]['u_id'] == expected_data3['channels'][0]['owner_members'][0]['u_id']
    assert data['channels'][0]['owner_members'][0]['name_first'] == expected_data3['channels'][0]['owner_members'][0]['name_first']
    assert data['channels'][0]['owner_members'][0]['name_last'] == expected_data3['channels'][0]['owner_members'][0]['name_last']

    assert data['channels'][0]['all_members'][0]['u_id'] == expected_data3['channels'][0]['all_members'][0]['u_id']
    assert data['channels'][0]['all_members'][0]['name_first'] == expected_data3['channels'][0]['all_members'][0]['name_first']
    assert data['channels'][0]['all_members'][0]['name_last'] == expected_data3['channels'][0]['all_members'][0]['name_last']

    assert data['channels'][0]['channel_messages'] == []


def test_channels_create_multiple_channels():
    clear()
    user = auth_register('MarioKart@yahoo.org', '123abc!@#', 'Lugi', 'Mario')
    channels_create(user['token'], 'testchannelname1', True)
    channels_create(user['token'], 'testchannelname2', False)

    assert data['channels'][0]['channel_id'] == expected_data4['channels'][0]['channel_id']
    assert data['channels'][0]['name'] == expected_data4['channels'][0]['name']
    assert data['channels'][0]['is_public'] == expected_data4['channels'][0]['is_public']

    assert data['channels'][0]['owner_members'][0]['u_id'] == expected_data4['channels'][0]['owner_members'][0]['u_id']
    assert data['channels'][0]['owner_members'][0]['name_first'] == expected_data4['channels'][0]['owner_members'][0]['name_first']
    assert data['channels'][0]['owner_members'][0]['name_last'] == expected_data4['channels'][0]['owner_members'][0]['name_last']

    assert data['channels'][0]['all_members'][0]['u_id'] == expected_data4['channels'][0]['all_members'][0]['u_id']
    assert data['channels'][0]['all_members'][0]['name_first'] == expected_data4['channels'][0]['all_members'][0]['name_first']
    assert data['channels'][0]['all_members'][0]['name_last'] == expected_data4['channels'][0]['all_members'][0]['name_last']

    assert data['channels'][0]['channel_messages'] == []


    assert data['channels'][1]['channel_id'] == expected_data4['channels'][1]['channel_id']
    assert data['channels'][1]['name'] == expected_data4['channels'][1]['name']
    assert data['channels'][1]['is_public'] == expected_data4['channels'][1]['is_public']


    assert data['channels'][1]['owner_members'][0]['u_id'] == expected_data4['channels'][1]['owner_members'][0]['u_id']
    assert data['channels'][1]['owner_members'][0]['name_first'] == expected_data4['channels'][1]['owner_members'][0]['name_first']
    assert data['channels'][1]['owner_members'][0]['name_last'] == expected_data4['channels'][1]['owner_members'][0]['name_last']

    assert data['channels'][1]['all_members'][0]['u_id'] == expected_data4['channels'][1]['all_members'][0]['u_id']
    assert data['channels'][1]['all_members'][0]['name_first'] == expected_data4['channels'][1]['all_members'][0]['name_first']
    assert data['channels'][1]['all_members'][0]['name_last'] == expected_data4['channels'][1]['all_members'][0]['name_last']

    assert data['channels'][1]['channel_messages'] == []
"""
