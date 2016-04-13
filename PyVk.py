import requests


class Vk:
    def __init__(self, token):
        """
        Initialize self with access token.
        """
        self.token = token
        self.apiUrl = 'https://api.vk.com/method/'
        self.methods = {'mget': 'messages.get', 'msend': 'messages.send', 'mgetdg': 'messages.getDialogs',
                        'mgetbid': 'messages.getById', 'msearch': 'messages.search', 'mgeth': 'messages.getHistory',
                        'mgetha': 'messages.getHistoryAttachments', 'mdel': 'messages.delete',
                        'mdeld': 'messages.deleteDialog', 'mrestore': 'messages.restore',
                        'mmread': 'messages.markAsRead', 'mmimportant': 'messages.markAsImportant',
                        'uget': 'users.get', 'fget': 'friends.get'}
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

    def messages_get_history_a(self, peer_id, media_type, count):
        """
        Gets attachments of dialog.
        :param peer_id: peer identifier
        :param media_type: type of attachments
        :param count: number of attachments to get
        :return: list of attachment objects
        """
        j = self.__execute('mgetha', {'peer_id': peer_id, 'media_type': media_type, 'count': count})
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
            raise ApiError('Cannot get attachment history: ' + j['error']['error_msg'])

    def messages_delete(self, message_ids):
        """
        Delete specified message(s).
        :param message_ids: message identifiers,comma-separated
        :return: 1 if operation was successful
        """
        j = self.__execute('mdel', {'message_ids': message_ids})
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot delete message(s): ' + j['error']['error_msg'])

    def messages_delete_dialog(self, user_id):
        """
        Delete dialog with user.
        :param user_id: user identifier
        :return: 1 if operation was successful
        """
        j = self.__execute('mdeld', {'user_id': user_id})
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot delete dialog: ' + j['error']['error_msg'])

    def messages_restore(self, message_id):
        """
        Restore deleted message.
        :param message_id: message identifier
        :return: 1 if operation successful
        """
        j = self.__execute('mrestore', {'message_id': message_id})
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot restore message: ' + j['error']['error_msg'])

    def messages_mark_as_read(self, message_ids):
        """
        Marks messages as read.
        :param message_ids: identifiers of messages,comma-separated
        :return: 1 if operation was successful
        """
        j = self.__execute('mmread', {'message_ids': message_ids})
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot mark as read: ' + j['error']['error_msg'])

    def messages_mark_as_important(self, message_ids, important=1):
        """
        Checks messages as important
        :param message_ids: identifiers of messages, comma-separated
        :param important: 1 to check,0 to uncheck
        :return: list of marked messages identifiers
        """
        j = self.__execute('mmimportant', {'message_ids': message_ids, 'important': important})
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot mark as important: ' + j['error']['error_msg'])

    def users_get(self, user_ids, fields=None, name_case=None):
        """
        Gets information about user.
        :param user_ids: identifier of users, comma-separated
        :param fields: list of additional fields
        :param name_case: case to show user name
        :return: list of user objects
        """
        j = self.__execute('uget', {'user_ids': user_ids, 'fields': fields, 'name_case': name_case})
        if 'response' in j.keys():
            return j['response']
        elif 'error' in j.keys():
            raise ApiError('Cannot get user: ' + j['error']['error_msg'])

    def friends_get(self, user_id=None, order='hints', count=None, fields=None , name_case=None):
        """
        Get specified user's friends identifiers and information.
        :param user_id: identifier of specified user
        :param order: order for list sorting (default - as in browser version)
        :param count: number of friends to get
        :param fields: additional fields to return
        :param name_case: case to show user name
        :return: list of identifiers if no fields specified, or list of friend objects
        """
        j = self.__execute('fget',{'user_id': user_id, 'order': order, 'count': count, 'fields': fields, 'name_case': name_case})
        if 'response' in j.keys():
            return j['response']['items']
        elif 'error' in j.keys():
                raise ApiError('Cannot get friends: ' + j['error']['error_msg'])

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
    """
    Raised when some API specific error occurs (expired token,permission error etc.)
    :return: string with error message
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    print('This module cannot be used as standalone program')
