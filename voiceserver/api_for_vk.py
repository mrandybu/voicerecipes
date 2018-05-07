import vk_api
import json


class GetVkApi(object):
    def __init__(self, domain=None, query=None, count=None):
        self.login = GetVkApi._get_auth_from_file(self)[0]
        self.password = GetVkApi._get_auth_from_file(self)[1]
        self.domain = domain
        self.query = query.encode('utf-8')
        self.count = count

    def _get_domain_list(self):
        return self._get_from_subfile('domains')

    def _get_auth_from_file(self):
        vk_auth = self._get_from_subfile('vk_auth')
        login = vk_auth['login']
        password = vk_auth['password']
        return login, password

    @staticmethod
    def _get_from_subfile(param):
        with open('subfile.json') as subfile:
            content = json.load(subfile)
        return content[param]

    def _get_vk_session(self):
        vk_session = vk_api.VkApi(self.login, self.password)

        try:
            vk_session.auth()
        except vk_api.AuthError as err_msg:
            return err_msg

        vk = vk_session.get_api()
        return vk

    def search_recipes(self):
        vk = self._get_vk_session()
        domains = self._get_domain_list()
        recipes = []
        for domain in domains:
            request = vk.wall.search(domain=domain, query=self.query, count=self.count)
            if request['items']:
                recipes_text = request['items']
                recipes.append(recipes_text)
            else:
                return 'Error of recipe search :('
        return recipes
