from data import data, user, channel
from other import clear

def test_resets_user_fields():
    # Force fields to be changed
    data.new_user(user("email@test.com", "password", "name_first", "name_last"))

    assert data.users[0].u_id == 0

    data.tokens = ['token1', 'token2', 'token3', 'token4']


    clear()
    assert data.num_users() == 0
    assert data.users == []
    assert data.tokens == []

def test_resets_channel_fields():
    data.channels.append(channel("channel1", True))
    data.channels.append(channel("channel2", True))
    assert data.num_channels() == 2

    clear()
    assert data.channels == []
    assert data.num_channels() == 0
