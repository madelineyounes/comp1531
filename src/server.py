import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError, AccessError

# import all the functions
from auth import auth_register, auth_logout, auth_login
from auth import auth_passwordreset_reset,  auth_passwordreset_request
from channel import channel_invite, channel_details, channel_messages
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create, channels_list, channels_listall
from message import message_send, message_remove, message_edit, message_sendlater, message_react, message_unreact, message_pin, message_unpin
from user import user_profile
from user import user_profile_setname, user_profile_setemail
from user import user_profile_sethandle, user_profile_uploadphoto
from other import clear, users_all, admin_userpermission_change, search
from standup import standup_start, standup_send, standup_active

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path = '/src/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

######################## auth http functions ############################

@APP.route("/auth/login", methods=['POST'])
def auth_login_http():
    data = request.get_json()
    return_dict = auth_login(data['email'], data['password'])
    return dumps(return_dict)


@APP.route("/auth/logout", methods=['POST'])
def auth_logout_http():
    data = request.get_json()
    return_dict = auth_logout(data['token'])
    return dumps(return_dict)


@APP.route("/auth/register", methods=['POST'])
def register():
    data = request.get_json()
    return_dict = auth_register(data['email'], data['password'], data['name_first'], data['name_last'])
    return dumps(return_dict)

@APP.route("/auth/passwordreset/request", methods=['POST'])
def passwordreset_request_http():
    email = request.get_json()
    return_dict = auth_passwordreset_request(email['email'])
    return dumps(return_dict)

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_passwordreset_reset_http():
    data = request.get_json()
    return_dict = auth_passwordreset_reset(data["reset_code"], data["new_password"])
    return dumps(return_dict)

######################## channel http functions ############################
@APP.route("/channel/invite", methods=['POST'])
def invite_channel():
    data = request.get_json()
    return_dict = channel_invite(data['token'], int(data['channel_id']), int(data['u_id']))
    return dumps(return_dict)


@APP.route("/channel/details", methods=['GET'])
def details_channel():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return_dict = channel_details(token, int(channel_id))
    print(return_dict)
    return dumps(return_dict)


@APP.route("/channel/messages", methods=['GET'])
def messages_channel():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    return_dict = channel_messages(token, int(channel_id), int(start))
    return dumps(return_dict)


@APP.route("/channel/leave", methods=['POST'])
def leave_channel():
    data = request.get_json()
    return_dict = channel_leave(data['token'], int(data['channel_id']))
    return dumps(return_dict)


@APP.route("/channel/join", methods=['POST'])
def join_channel():
    data = request.get_json()
    return_dict = channel_join(data['token'], int(data['channel_id']))
    return dumps(return_dict)


@APP.route("/channel/addowner", methods=['POST'])
def addowner_channel():
    data = request.get_json()
    return_dict = channel_addowner(data['token'], int(data['channel_id']), int(data['u_id']))
    return dumps(return_dict)


@APP.route("/channel/removeowner", methods=['POST'])
def removeowner_channel():
    data = request.get_json()
    return_dict = channel_removeowner(data['token'], int(data['channel_id']), int(data['u_id']))
    return dumps(return_dict)


######################## channels http functions ############################

@APP.route("/channels/create", methods=['POST'])
def create_channel():
    data = request.get_json()
    return_dict = channels_create(data['token'], data['name'], data['is_public'])
    return dumps(return_dict)


@APP.route("/channels/list", methods=['GET'])
def list_channels():
    data = request.args.get('token')
    return_dict = channels_list(data)
    return dumps(return_dict)


@APP.route("/channels/listall", methods=['GET'])
def listall_channels():
    data = request.args.get('token')
    return_dict = channels_listall(data)
    return dumps(return_dict)


######################## message http functions ############################

@APP.route("/message/send", methods = ['POST'])
def send_message():
    data = request.get_json()
    return_dict = message_send(data['token'], int(data['channel_id']), data['message'])
    return dumps(return_dict)

@APP.route("/message/edit", methods = ['PUT'])
def edit_message():
    data = request.get_json()
    return_dict = message_edit(data['token'], int(data['message_id']), data['message'])
    return dumps(return_dict)

@APP.route("/message/remove", methods = ['DELETE'])
def remove_message():
    data = request.get_json()
    return_dict = message_remove(data['token'], int(data['message_id']))
    return dumps(return_dict)

@APP.route("/message/sendlater", methods = ['POST'])
def send_later():
    data = request.get_json()
    return_dict = message_sendlater(data['token'], int(data['channel_id']), data['message'], int(data['time_sent']))
    return dumps(return_dict)

@APP.route("/message/react", methods = ['POST'])
def react_to_message():
    data = request.get_json()
    return_dict = message_react(data['token'], int(data['message_id']), int(data['react_id']))
    return dumps(return_dict)

@APP.route("/message/unreact", methods = ['POST'])
def unreact_to_message():
    data = request.get_json()
    return_dict = message_unreact(data['token'], int(data['message_id']), int(data['react_id']))
    return dumps(return_dict)

@APP.route("/message/pin",  methods = ['POST'])
def pin_message():
    data = request.get_json()
    return_dict = message_pin(data['token'], int(data['message_id']))
    return dumps(return_dict)

@APP.route("/message/unpin",  methods = ['POST'])
def unpin_message():
    data = request.get_json()
    return_dict = message_unpin(data['token'], int(data['message_id']))
    return dumps(return_dict)


######################## other http functions ############################
# The paths to implement
@APP.route("/clear", methods=['DELETE'])
def reset():
    clear()
    return {}

@APP.route("/users/all", methods=['GET'])
def get_users():
    data = request.args.get('token')
    return_dict = users_all(data)
    return dumps(return_dict)


@APP.route("/admin/userpermission/change", methods=['POST'])
def change_permissions():
    data = request.get_json()
    return_dict = admin_userpermission_change(data['token'], int(data['u_id']), int(data['permission_id']))
    return dumps(return_dict)


@APP.route("/search", methods=['GET'])
def message_search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return_dict = search(token, query_str)
    return dumps(return_dict)


######################## user http functions ############################

@APP.route("/user/profile", methods=['GET'])
def user_profile_http():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return_dict = user_profile(token, int(u_id))
    return dumps(return_dict)

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname_http():
    data = request.get_json()
    return_dict = user_profile_setname(data["token"], data["name_first"], data["name_last"])
    return dumps(return_dict)

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setmail_http():
    data = request.get_json()
    return_dict = user_profile_setemail(data["token"], data["email"])
    return dumps(return_dict)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle_http():
    data = request.get_json()
    return_dict = user_profile_sethandle(data["token"], data["handle_str"])
    return dumps(return_dict)

@APP.route("/users/all", methods=['GET'])
def users_all_http():
    token = request.args.get('token')
    return_dict = users_all(token)
    return dumps(return_dict)

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def uploadphoto():
    data = request.get_json()
    return_dict = user_profile_uploadphoto(data["token"], data["img_url"], data["x_start"], data["y_start"], data["x_end"], data["y_end"], request.host_url)
    return dumps(return_dict)

@APP.route('/src/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)


######################## standup functions ############################

@APP.route("/standup/start", methods = ['POST'])
def start_standup():
    data = request.get_json()
    return_dict = standup_start(data['token'], int(data['channel_id']), int(data['length']))
    return dumps(return_dict)

@APP.route("/standup/active", methods = ['GET'])
def check_active():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return_dict = standup_active(token, channel_id)
    return dumps(return_dict)

@APP.route("/standup/send", methods = ['POST'])
def send_standup():
    data = request.get_json()
    return_dict = standup_send(data['token'], int(data['channel_id']), data['message'])
    return dumps(return_dict)


if __name__ == "__main__":
    APP.run(port=64810) # Do not edit this port
