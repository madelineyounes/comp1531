# Assumptions

## Authentication

### auth_login:

    - We are using the user's index in the 'users' list as their u_id.

### auth_register:

    - The suggested regex for checking emails was changed slightly by allowing uppercase letters before the @ sign and added a dash and a forward slash to the separator list
    - The boundaries for names are inclusive, therefore a name of 1 character, a name of 50 characters and a password of 6 characters are all valid.
    - The method for changing a handle string that is already in use is to add a 3 digit random number to the end, if the handle is less than 18 characters in length then the numbers are added to the end, however to keep the requirements below the 20 characters if the name is 17 characters or greater already then characters 18-20 are changed to be numbers  
    - the data inside the token is the user id

## Channels

### channels_create:

    - The user with the token that was used to create the channel is the owner and member of that channel.

## Channel

### channel_invite:

    - User is who already a channel member triggers an InputError when invited.


### channel_messages:

    - The given argument "start' cannot be less than zero,
    channel_messages will raise InputError if this were to happen.
    - Each channel can only have one message stream.

### channel_leave:

    - Once the last owner is removed from a channel the channel is removed even if there are still members

### channel_join:

    - channel_join will raise AccessError if the user given is already part of the channel.

### channel_addowner:

    - channel_id's line up with the channels list indices.
    - A user must be a member of a channel to be added as an owner.

### channel_removeowner:

    - channel_id's line up with the channels list indices.
    - Assumed that valid channel_id values will not be negative.
    - The user can not remove a global owner as an owner of a channel.

## Other

### admin_userpermission_change:
    -  global owner can not change their own permission_id
