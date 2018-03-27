import vk_api


class GetVkApi(object):
    def __init__(self, domain='great.food', query=None, count=None):
        self.login = GetVkApi._get_auth_from_file()[0]
        self.password = GetVkApi._get_auth_from_file()[1]
        self.domain = domain
        self.query = query
        self.count = count

    @staticmethod
    def _get_vk_session(self):
        vk_session = vk_api.VkApi(self.login, self.password)

        try:
            vk_session.auth()
        except vk_api.AuthError as err_msg:
            print(err_msg)

        vk = vk_session.get_api()
        return vk

    def search_recipes(self):
        vk = self._get_vk_session(self)
        response = vk.wall.search(domain=self.domain, query=self.query, count=self.count)

        if response['items']:
            return response['items']

    @staticmethod
    def _get_auth_from_file():
        f_auth = open('vk_auth.l', 'r')
        login, password = f_auth.read().split('\n')
        return login, password
