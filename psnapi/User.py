import simplejson
import json
import urllib
import requests
import urllib.request
import urllib.parse
import os

class User:

    oauth = None
    refresh_token = None

    USERS_ENDPOINT  = 'https://us-prof.np.community.playstation.net/userProfile/v1/users/'
    GAMES_ENDPOINT  = 'https://gamelist.api.playstation.com/v1/'
    TROPHY_ENDPOINT = 'https://us-tpy.np.community.playstation.net/trophy/v1/'
    TROPHY_ENDPOINT_CN = 'https://cn-tpy.np.community.playstation.net/trophy/v1/'

    def __init__(self, tokens):
        self.oauth = tokens['oauth']
        self.refresh_token = tokens['refresh']

    def userinfo(self, nickname='me'):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        endpoint = '%s/profile2?fields=npId,onlineId,avatarUrls,plus,aboutMe,languagesUsed,trophySummary(@default,progress,earnedTrophies),isOfficiallyVerified,personalDetail(@default,profilePictureUrls),personalDetailSharing,personalDetailSharingRequestMessageFlag,primaryOnlineStatus,presences(@titleInfo,hasBroadcastData),friendRelation,requestMessageFlag,blocking,mutualFriendsCount,following,followerCount,friendsCount,followingUsersCount&avatarSizes=m,xl&profilePictureSizes=m,xl&languagesUsedLanguageSet=set3&psVitaTitleIcon=circled&titleIconSize=s'
        endpoint = endpoint % nickname
        request = urllib.request.Request(self.USERS_ENDPOINT+endpoint, headers=header)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))

        return data
    
    def gamesinfo(self, nickname='me', limit=100):
        header = {
            'Authorization': 'Bearer '+self.oauth,
        }

        endpoint = 'users/%s/titles'
        endpoint = endpoint % nickname

        param = {
            'type' : 'played',
            'app'  : 'richProfile',
            'sort' : '-lastPlayedDate',
            'limit': limit,
            'iw'   : 240, 
            'ih'   : 240  
        }

        params = "?"
        for key in param:
            params = params + key + "=" + str(param[key]) + "&"

        # print(params)
        # params = '?type=played&app=richProfile&sort=-lastPlayedDate&limit=100&iw=240&ih=240'
        # https://gamelist.api.playstation.com/v1/users/%s/titles

        response = requests.get(self.GAMES_ENDPOINT+endpoint+params, headers=header).text
        print(response)

        request = urllib.request.Request(self.GAMES_ENDPOINT+endpoint+params, headers=header)
        data = []
        try:
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(e)
        return data

    def friendsinfo(self, nickname='me'):
        header = {
            'Authorization': 'Bearer '+self.oauth,
        }
        endpoint = '%s/friends/profiles2'
        endpoint = endpoint % nickname

        param = {
            'fields' : 'onlineId,accountId,avatarUrls,plus,trophySummary(@default),isOfficiallyVerified,personalDetail(@default,profilePictureUrls),presences(@titleInfo,hasBroadcastData,lastOnlineDate),presences(@titleInfo),friendRelation,consoleAvailability',
            'offset' : 0,
            'limit' : 36,
            'profilePictureSizes' : 'm',
            'avatarSizes' : 'm',
            'titleIconSize' : 's',
            'sort' : 'onlineStatus'
        }

        params = "?"
        for key in param:
            params = params + key + "=" + str(param[key]) + "&"

        request = urllib.request.Request(self.USERS_ENDPOINT+endpoint+params, headers=header)
        data = []
        try:
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(e)
        return data

    def trophyinfo(self, nickname='hello1348qwer', limit=12, offset=0):
        header = {
            'Authorization': 'Bearer '+self.oauth,
        }
        endpoint = 'trophyTitles'

        param = {
            # 'npTitleIds' : $this->titleId,
            'fields' : '@default,trophyTitleSmallIconUrl',
            'npLanguage' : 'en',
            'platform' : 'PS3%2CPS4%2CPSVITA'
        }
        params = "?"
        for key in param:
            params = params + key + "=" + str(param[key]) + "&"
        # request = urllib.request.Request(self.TROPHY_ENDPOINT+endpoint+params, headers=header)
        # response = urllib.request.urlopen(request)
        
        # data = json.loads(response.read().decode('utf-8'))

        url = 'https://cn-tpy.np.community.playstation.net/trophy/v1/trophyTitles?fields=%40default%2CtrophyTitleSmallIconUrl&platform=PS3%2CPS4%2CPSVITA&'
        params = 'limit=%s&offset=%s&comparedUser=%s&npLanguage=zh-CN' % (limit, offset, nickname)

        request = urllib.request.Request(url+params, headers=header)
        response = urllib.request.urlopen(request)
        
        data = json.loads(response.read().decode('utf-8'))

        return data

    def trophy_info_by_id(self, nickname='onnkei', npCommunicationId='NPWR10172_00'):
        header = {
            'Authorization': 'Bearer '+self.oauth,
        }

        url = 'https://cn-tpy.np.community.playstation.net/trophy/v1/trophyTitles/%s' % npCommunicationId
        params = '?comparedUser=%s&npLanguage=zh-CN' % nickname

        request = urllib.request.Request(url+params, headers=header)
        response = urllib.request.urlopen(request)
        
        data = json.loads(response.read().decode('utf-8'))
        return data

    def trophy_all(self, nickname='onnkei', npCommunicationId='NPWR10172_00'):
        header = {
            'Authorization': 'Bearer '+self.oauth,
        }
        endpoint = 'trophyTitles/%s/trophyGroups/all/trophies' % npCommunicationId
        param = {
            'fields' : '@default,trophyRare,trophyEarnedRate,hasTrophyGroups,trophySmallIconUrl',
            'iconSize' : 'm',
            'visibleType' : 1,
            'npLanguage' : 'zh-CN',
            'comparedUser' : nickname
        }
        params = "?"
        for key in param:
            params = params + key + "=" + str(param[key]) + "&"
        url = self.TROPHY_ENDPOINT_CN + endpoint

        request = urllib.request.Request(url+params, headers=header)
        response = urllib.request.urlopen(request)
        
        data = json.loads(response.read().decode('utf-8'))
        return data
