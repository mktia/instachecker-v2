import json
import requests
import urllib

class Utils():

    ## Constructor ##
    def __init__(self):
        self.OAUTH_HOST = 'api.instagram.com'
        self.OAUTH_ROOT = '/oauth/authorize/'
        self.TOKEN_ROOT = '/oauth/access_token'

        self.__CLIENT_ID = ''
        self.__CLIENT_SECRET = ''
        self.__access_token = ''
        self.__code = ''
        self.redirect_url = ''
        self.pagination = None

        self.basic_information = {}
        self.myself = {}


    ## functions ##
    def make_url(self):
        """
        return a link using authentication
        """
        endpoint = (
            '?client_id=' + self.__get_client_id() +
            '&redirect_uri=' + self.redirect_url +
            '&response_type=' + 'code' +
            '&scope=' + 'follower_list'
        )
        return(self.__get_oauth_url() + endpoint)

    def request_access_token(self):
        payload = {
            'client_id' : self.__get_client_id(),
            'client_secret' : self.__get_client_secret(),
            'grant_type' : 'authorization_code',
            'redirect_uri' : self.redirect_url,
            'code' : self.__get_code()
        }
        response = requests.post(self.__get_token_url(), data=payload)
        json = response.json()

        try:
            self.__set_access_token(json['access_token'])
        except Exception as e:
            return('Failed to get access token: ' + str(e))

        # 'user' dictionary includes id, username, profile_picture, full_name (nickname), bio, website, and is_business variables.
        self.myself = json['user']

        return('Success!')

    def get_follows(self):
        follows = []
        follows.extend(self.__get_follows())

        while(self.pagination != None):
            follows.extend(self.__get_follows(self.pagination))

        return(follows)

    def get_followers(self):
        followers = []
        followers.extend(self.__get_followers())

        while(self.pagination != None):
            followers.extend(self.__get_followers(self.pagination))

        return(followers)

    def get_list_of_friends(self, follows, followers):
        """
        Return the list of accounts you follow and be followed by.
        """
        friends = []

        for i in follows:
            for j in followers:
                if i['id'] == j['id']:
                    friends.append(i)
                    # if i is my friend, remove from followers
                    followers.remove(i)
                    break

        return(friends)

    def get_list_of_follows(self, friends, follows):
        """
        Return the list of accounts you follow but not be followed by.
        """
        for i in friends:
            follows.remove(i)

        return(follows)

    def get_list_of_followers(self, friends, followers):
        """
        Return the list of accounts you don't follow but be followed by.
        """
        for i in friends:
            followers.remove(i)

        return(followers)


    def __get_follows(self, url=None):
        if url == None:
            query = '?access_token=' + self.__get_access_token()
            url = 'https://' + self.OAUTH_HOST + '/v1/users/self/follows' + query
        return self.__get_users_list(url)

    def __get_followers(self, url=None):
        if url == None:
            query = '?access_token=' + self.__get_access_token()
            url = 'https://' + self.OAUTH_HOST + '/v1/users/self/followed-by' + query
        return self.__get_users_list(url)

    def __get_users_list(self, url):
        response = urllib.request.urlopen(url)
        load_data = json.loads(response.read())

        if not self.__check_http_status(load_data):
            return()

        if len(load_data['pagination']) != 0:
            self.pagination = load_data['pagination']['next_url']
        else:
            self.pagination = None

        users_list = []

        for d in load_data['data']:
            users_list.append(d)

        return(users_list)


    ## Basic functions ##
    def set_client_id(self, client_id):
        self.__CLIENT_ID = client_id

    def set_client_secret(self, client_secret):
        self.__CLIENT_SECRET = client_secret

    def set_code(self, code):
        self.__code = code

    def set_description(self, sentence):
        self.basic_information['description'] = sentence

    def set_name(self, name):
        self.basic_information['name'] = name

    def set_short_description(self, sentence):
        self.basic_information['short_description'] = sentence

    def set_url(self, url):
        self.basic_information['url'] = url

    def __check_http_status(self, obj):
        if obj['meta']['code'] == 200:
            return(True)
        else:
            print(obj['meta']['error_type'] + ': ' + obj['meta']['error_message'])
            return(False)

    def __get_access_token(self):
        return self.__access_token

    def __get_client_id(self):
        return self.__CLIENT_ID

    def __get_client_secret(self):
        return self.__CLIENT_SECRET

    def __get_code(self):
        return self.__code

    def __get_oauth_url(self):
        return('https://' + self.OAUTH_HOST + self.OAUTH_ROOT)

    def __get_token_url(self):
        return('https://' + self.OAUTH_HOST + self.TOKEN_ROOT)

    def __set_access_token(self, access_token):
        self.__access_token = access_token
