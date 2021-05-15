import data
from data import data
from other import clear
from expected_data import expected_data1, expected_data2
from auth import auth_register

def test_auth_register_several_users_white_box():
    clear()
    auth_register('WICKEDER@yahoo.org', '123abc!@#', 'Cosmo', 'Kearns')
    auth_register('RenameLHC@yahoo.org', '123abc!@#', 'Abida', 'Zhang')
    auth_register("repeatin-rifle@yahoo.org", '123abc!@#', 'Brenden', 'Partridge')
    assert data.num_users() == expected_data1['numUsers']
    assert [{'u_id': user.u_id, 'email': user.email, 'password': user.password,\
             'name_first': user.name_first, 'name_last': user.name_last,\
             'handle_str': user.handle_str, 'profile_img_url': user.profile_img_url, \
             'permission_id': user.permission_id} for user in data.users] == expected_data1['users']

def test_auth_register_handle_too_long():
    clear()
    auth_register('hello@yahoo.org', '12sdf3abcsf!@#', 'sudifhsdfhssdsdfsoifusdfs', 'Arsdfsdfwxefefchsdfsdsdfer')
    assert data.num_users() == expected_data2['numUsers']
    assert [{'u_id': user.u_id, 'email': user.email, 'password': user.password,\
             'name_first': user.name_first, 'name_last': user.name_last,\
             'handle_str': user.handle_str, 'profile_img_url': user.profile_img_url, \
             'permission_id': user.permission_id} for user in data.users] == expected_data2['users']

def test_auth_register_handle_the_same():
    clear()
    auth_register('hllo@yahoo.org', '12sdf3abcsf!@#', 'sudifhsdfhssdsdfsoifusdfs', 'Arsdfsdfwxefefchsdfsdsdfer')
    auth_register('heldsglo@yahoo.org', '12sdf3abcsf!@#', 'sudifhsdfhssdsdfsoifusdfs', 'Arsdfsdfwxefefchsdfsdsdfer')
    auth_register('helsdfslo@yahoo.org', '12sdf3abcsf!@#', 'sudifhsdfhssdsdfsoifusdfs', 'Arsdfsdfwxefefchsdfsdsdfer')
    assert data.users[0].handle_str == 'sudifhsdfhssdsdfsoif'
    assert data.users[1].handle_str != 'sudifhsdfhssdsdfsoif'
    assert data.users[2].handle_str != 'sudifhsdfhssdsdfsoif'
    assert data.users[2].handle_str != data.users[1].handle_str
