from ...lib.entity.credential import Credential
from ...lib.util.abstract import Abstract


class CredentialCustom(Credential, Abstract):
    USER_AGENT = 'Instagram {app_version} Android ({android_version}/{android_release}; {dpi}; {resolution}; {manufacturer}; {device}; {model}; {cpu}; en_US; {version_code})'
    BLOKS = 'e097ac2261d546784637b3df264aa3275cb6281d706d91484f43c207d6661931'
    CAPABILITIES = '3brTvx0='

    def __init__(self):
        Abstract.__init__(self)
        Credential.__init__(self, self.USER_AGENT, self.BLOKS, self.CAPABILITIES)
        self.__user_id = None

    @property
    def user_id(self) -> int:
        return self.__user_id if self.__user_id else self.user_id_from_auth

    @user_id.setter
    def user_id(self, value: int):
        self.__user_id = value

    def set_auth(self, response_header: dict, bearer=None):
        self.logger.debug('Set auth from header {}'.format(response_header))
        self.authorization = {
            'x-ig-set-www-claim': response_header.get('x-ig-set-www-claim'),
            'ig-u-rur': response_header.get('ig-set-ig-u-rur'),
            'ds-user-id': response_header.get('ig-set-ig-u-ds-user-id'),
            'X-FB-TRIP-ID': response_header.get('X-FB-TRIP-ID'),
            'x-ig-origin-region': response_header.get('x-ig-origin-region'),
            'ig-set-authorization': response_header.get('ig-set-authorization') if len(
                response_header.get('ig-set-authorization', '')) > 20 else (bearer if bearer else self.bearer),
            'x-mid': response_header.get('ig-set-x-mid', '') if len(
                response_header.get('ig-set-x-mid', '')) else self.mid
        }
