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
        endpoint = '%s/profile2?fields=npId,onlineId,avatarUrls,plus,aboutMe,languagesUsed,trophySummary(@default,progress,earnedTrophies),isOfficiallyVerified,personalDetail(@default,profilePictureUrls),personalDetailSharing,personalDetailSharingRequestMessageFlag,primaryOnlineStatus,presences(@titleInfo,hasBroadcastData),friendRelation,requestMessageFlag,blocking,mutualFriendsCount,following,followerCount,friendsCount,followingUsersCount&avatarSizes=m,xl&profilePictureSizes=m,xl&languagesUsedLanguageSet=set3&psVitaTitleIcon=circled&titleIconSize=s'
        endpoint = endpoint % nickname
        return self.get_data(self.USERS_ENDPOINT+endpoint)
    
    def gamesinfo(self, nickname='me', limit=100):
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
        return self.get_data(self.GAMES_ENDPOINT+endpoint+params)

    def friendsinfo(self, nickname='me'):
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
        return self.get_data(self.USERS_ENDPOINT+endpoint+params)

    def trophyinfo(self, nickname='hello1348qwer', limit=12, offset=0):
        param = {
            # 'npTitleIds' : $this->titleId,
            'fields' : '@default,trophyTitleSmallIconUrl',
            'npLanguage' : 'en',
            'platform' : 'PS3%2CPS4%2CPSVITA'
        }
        params = "?"
        for key in param:
            params = params + key + "=" + str(param[key]) + "&"
        url = 'https://cn-tpy.np.community.playstation.net/trophy/v1/trophyTitles?fields=%40default%2CtrophyTitleSmallIconUrl&platform=PS3%2CPS4%2CPSVITA&'
        params = 'limit=%s&offset=%s&comparedUser=%s&npLanguage=zh-CN' % (limit, offset, nickname)
        return self.get_data(url+params)

    def trophy_all(self, nickname='onnkei', npCommunicationId='NPWR10172_00'):
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
        return self.get_data(url+params)

    def trophy_detail_list(self, npCommunicationId='NPWR10172_00'):
        endpoint = 'trophyTitles/%s/trophyGroups/all/trophies' % npCommunicationId
        param = {
            'fields' : '@default,trophyRare,trophyEarnedRate,trophySmallIconUrl',
            'iconSize' : 'm',
            'visibleType' : 1,
            'npLanguage' : 'zh-CN',
        }
        params = "?"
        for key in param:
            params = params + key + "=" + str(param[key]) + "&"
        url = self.TROPHY_ENDPOINT_CN + endpoint
        return self.get_data(url+params)
    
    def get_data(self, url, timeout=5):
        header = {
            'Authorization': 'Bearer '+self.oauth,
        }
        try:
            request = urllib.request.Request(url, headers=header)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print('get_data err : %s' % e)
            return False
        return data

