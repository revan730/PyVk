import requests

class Vk:

    def __init__(self, token):
        '''
        Initialize self with access token.
        '''
        self.token = token
        self.apiUrl = 'https://api.vk.com/method/'
        self.methods = {'mget': 'messages.get', 'msend': 'messages.send'}

    def token_сheck(self):
        '''
        Checks if access token is usable or not.
        :return: True or None
        '''
        p = {'access_token': self.token}
        r = requests.get(self.apiUrl + 'messages.get', params=p)
        j = r.json()
        print(j)
        if 'response' in j.keys():
            return True
        else:
            return None

    def messages_get(self):
        '''
        :return: list of Vk message objects.
        '''
        p = {'access_token': self.token}
        r = requests.get(self.apiUrl + self.methods['mget'], params=p)
        j = r.json()
        if 'response' in j.keys():
            return j['items']
        elif 'error' in j.keys():
            raise ApiException('Cannot get message: ' + j['error']['error_msg'])


class ApiException(BaseException):
    ''' Raised when some API specific error occures (expired token,premission error etc.) '''
    def __init__(self,value):
        self.value = value

    def __str__(self):
        repr(self.value)

if __name__ == '__main__':
    print('This module cannot be used as standalone program')