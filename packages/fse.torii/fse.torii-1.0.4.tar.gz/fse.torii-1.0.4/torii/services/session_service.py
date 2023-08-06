import sys

from torii.exception import ToriiException
from torii.services.torii_service import ToriiService
from torii.data.torii_object import ToriiObject


class SessionService(ToriiService):

    def __init__(self, torii):
        """
        Create the session service
        """
        ToriiService.__init__(self, torii=torii, name='sessions', object_class=ToriiObject)


    def check_auth(self, username=None, password=None):
        credentials = SessionService._build_credentials(username, password)

        try:
            json = self.request('POST', path='login', json=credentials)
        except Exception as e:
            raise ToriiException('Failed to log as {0} on {1} : {2}'
                               .format(username, self._torii.properties['base_url'], e)).with_traceback(sys.exc_info()[2])

        session = ToriiObject(json, self)
        self._logger.info('User logged as {0} on {1}'.format(session.user.name, self._torii.properties['base_url']))

        return session


    def login(self, username=None, password=None, timeout=30):
        credentials = SessionService._build_credentials(username, password)

        try:
            json = self.request_post(path='login', json=credentials, timeout=timeout)
        except Exception as e:
            raise ToriiException('Failed to log as {0} on {1} : {2}'
                               .format(username, self._torii.properties['base_url'], e)).with_traceback(sys.exc_info()[2])

        session = ToriiObject(json, self)

        self._logger.info('User logged as {0} on {1}'.format(session.user.name, self._torii.properties['base_url']))

        return session


    def su(self, user):
        if isinstance(user, ToriiObject):
            params = {'userId': user.id}
        else:
            params = {'userId': user}

        try:
            json = self.request_post(path='su', params=params)
        except Exception as e:
            raise ToriiException('Failed to switch user with {} : {}'
                               .format(user, e)).with_traceback(sys.exc_info()[2])

        session = ToriiObject(json, self)

        self._logger.info('User logged as {0} on {1}'.format(session.user.name, self._torii.properties['base_url']))
        self._torii.session = session

        return session


    def logout(self):
        try:
            self.request_post(path='logout')
        except Exception as e:
            raise ToriiException('Failed to logout : {}'
                               .format(self._torii.properties['base_url'], e))\
                .with_traceback(sys.exc_info()[2])

        self._logger.info('User logged out from {}'.format(self._torii.properties['base_url']))


    def check(self, session_id=None):
        if session_id:
            params = {'ToriiSessionId': session_id}
        else:
            params = None

        try:
            json = self.request_get(path='check', params=params)
        except Exception as e:
            self._logger.warn('No active session {} on {}'.format(session_id, self._torii.properties['base_url']))
            return None

        session = ToriiObject(json, self)
        self._logger.info('User {0} has an active session on {1} (id={2})'
                          .format(session.user.name, self._torii.properties['base_url'], session.id))

        return session

    @staticmethod
    def _build_credentials(username: str, password: str):
        username = username.strip()
        password = password.strip()

        return {
            'userName': username,
            'password': password
        }
