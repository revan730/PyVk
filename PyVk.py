import requests


class Vk:

    def __init__(self, token):
        """
        Initialize self with access token.
        """
        self.token = token
        self.apiUrl = 'https://api.vk.com/method/'
        self.methods = {'mget': 'messages.get', 'msend': 'messages.send', 'mgetdg': 'messages.getDialogs',
                        'mgetbid': 'messages.getById', 'msearch': 'messages.search', 'mgeth': 'messages.getHistory'}
        self.apiVer = '5.50'
        self.commonParams = {'access_token': self.token, 'v': self.apiVer}

    def token_сheck(self):
        """
        Checks if access token is usable or not.
        :return: True or None
        """
        j = self.__execute('mget', {})
        print(j)
        if 'response' in j.keys():
            return True
        else:
            return None

    def messages_get(self, out=0, count=20):
        """
        Get messages.
        :param out: get sent messages (0 or 1)
        :param count: number of messages to get
        :return: list of message objects.
        """
        j = self.__execute('mget', {'out': out, 'count': count})
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot get message: ' + j['error']['error_msg'])

    def messages_send(self, user_id, message, attachments=None):
        """
        Sends message to peer.
        :param user_id: receiving users identifier
        :param message: message's body
        :param attachments: comma-separated attachments in format <type><owner_id>_<media_id>
        :return: message's identifier if operation was successful
        """
        j = self.__execute('msend', {'user_id': user_id, 'message': message, 'attachment': attachments})
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot send message: ' + j['error']['error_msg'])

    def messages_get_dialogs(self, count=20, unread=0):
        """
        Get user's dialogs list.
        :param count: number of dialogs to get
        :param unread: get dialogs with unread messages only (1 or 0)
        :return: list of dialog objects
        """
        j = self.__execute('mgetdg', {'count': count, 'unread': unread})
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot get dialogs: ' + j['error']['error_msg'])

    def messages_get_by_id(self, message_ids, preview_length=0):
        """
        Get messages by their id.
        :param message_ids: list of message id's,comma-separated
        :param preview_length: length of message preview
        :return: list of message objects
        """
        j = self.__execute('mgetbid', {'message_ids': message_ids, 'preview_length': preview_length})
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot get message(s) by id: ' + j['error']['error_msg'])

    def messages_search(self, q, preview_length=0, count=20):
        """
        Search messages by substring.
        :param q: searched substring
        :param preview_length: length of message preview
        :param count: number of messages to get
        :return: list of message objects
        """
        j = self.__execute('msearch', {'q': q, 'preview_length': preview_length, 'count': count})
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot find message(s): ' + j['error']['error_msg'])

    def messages_get_history(self, user_id, count=20, rev=0):
        """
        Gets message history with specified user.
        :param user_id: user's identifier
        :param count: number of messages to get
        :param rev: Chronological or reversed order (1 or 0)
        :return: list of message objects
        """
        j = self.__execute('mgeth', {'user_id': user_id, 'count': count, 'rev': rev})
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot get message history: ' + j['error']['error_msg'])

    def __execute(self, method, args):
        """
        Execute API method.
        :param method: key of method name from methods dictionary
        :param args: dictionary of method arguments
        :return: json object
        """
        p = self.commonParams.copy()
        p.update(args)
        p = dict((k, v) for k, v in p.items() if v)
        r = requests.get(self.apiUrl + self.methods[method], params=p)
        return r.json()


class ApiError(BaseException):
    """ Raised when some API specific error occurs (expired token,permission error etc.) """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    print('This module cannot be used as standalone program')
