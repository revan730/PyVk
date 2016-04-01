import requests


class Vk:

    def __init__(self, token):
        """
        Initialize self with access token.
        """
        self.token = token
        self.apiUrl = 'https://api.vk.com/method/'
        self.methods = {'mget': 'messages.get', 'msend': 'messages.send', 'mgetdg': 'messages.getDialogs'}
        self.apiVer = '5.50'
        self.commonParams = {'access_token': self.token, 'v': self.apiVer}

    def token_сheck(self):
        """
        Checks if access token is usable or not.
        :return: True or None
        """
        r = requests.get(self.apiUrl + 'messages.get', params=self.commonParams)
        j = r.json()
        print(j)
        if 'response' in j.keys():
            return True
        else:
            return None

    def messages_get(self, out=0, count=20):
        """
        :param out: get sent messages (0 or 1)
        :param count: number of messages to get
        :return: list of message objects.
        """
        p = self.commonParams.copy()
        p['out'] = out
        p['count'] = count
        r = requests.get(self.apiUrl + self.methods['mget'], params=p)
        j = r.json()
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot get message: ' + j['error']['error_msg'])

    def messages_send(self, user_id, message, attachments=None):
        """
        Sends message to peer
        :param user_id: receiving users identifier
        :param message: message's body
        :param attachments: comma-separated attachments in format <type><owner_id>_<media_id>
        :return: message's identifier if operation was successful
        """
        p = self.commonParams.copy()
        p['user_id'] = user_id
        p['message'] = message
        if attachments:
            p['attachment'] = attachments
        r = requests.get(self.apiUrl + self.methods['msend'], params=p)
        j = r.json()
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot send message: ' + j['error']['error_msg'])

    def messages_get_dialogs(self, count=20, unread=0):
        """
        Get user's dialogs list
        :param count: number of dialogs to get
        :param unread: get dialogs with unread messages only (1 or 0)
        :return: list of dialog objects
        """
        p = self.commonParams.copy()
        p['count'] = count
        p['unread'] = unread
        r = requests.get(self.apiUrl + self.methods['mgetdg'], params=p)
        j = r.json()
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot get dialogs: ' + j['error']['error_msg'])


class ApiError(BaseException):
    """ Raised when some API specific error occurs (expired token,permission error etc.) """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        repr(self.value)

if __name__ == '__main__':
    print('This module cannot be used as standalone program')
