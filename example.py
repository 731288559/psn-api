#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psnapi.Auth import Auth
from psnapi.Friend import Friend
from psnapi.User import User
from psnapi.Messaging import Messaging
import json

with open('tokens', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

new_token_pair = Auth.GrabNewTokens(data['refresh'])

tokens = {
    "oauth": new_token_pair[0],
    "refresh": new_token_pair[1],
    "npsso": data['npsso'] # saved above!
}
print(tokens)

friend = Friend(tokens)
friend_list = friend.my_friends()
# print(friend.my_friends(nickname='onnkei'))

friend_string = ''
if bool(friend_list):
    for key, value in friend_list.items():
        if value is not "":
            friend_string += key+' is playing '+value+"\n"
        else:
            friend_string += key+' is online'+"\n"
else:
    friend_string = 'No friends online'

# print(friend_string.replace('ÂŽ', ''))

user = User(tokens)

# print(user.userinfo())
# print(user.userinfo('haruhi2728'))
# print(friend.get_info('onnkei'))

# print(user.gamesinfo())               # HTTP Error 403: Forbidden
# print(user.gamesinfo('haruhi2728'))   # HTTP Error 403: Forbidden

# print(user.friendsinfo())
# print(user.friendsinfo('hello1348qwer'))
# print(user.friendsinfo('onnkei'))     # HTTP Error 403: Forbidden

# print(user.trophyinfo('onnkei'))

# print(user.trophy_all())
