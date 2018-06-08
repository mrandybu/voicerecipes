import vk_api
import json
import __root__


class GetVkApi(object):
    def __init__(self, domain=None, query=None, count=None):
        self._subfile = __root__.get_root_path_to_file('subfile.json')
        self._login = GetVkApi._get_auth_from_file(self)[0]
        self._password = GetVkApi._get_auth_from_file(self)[1]
        self.domain = domain
        self.query = query
        self.count = count

    def _get_domain_list(self):
        with open(self._subfile) as sbf:
            domains = json.load(sbf)
        return domains['domains']

    def _get_vk_session(self):
        vk_session = vk_api.VkApi(self._login, self._password)

        try:
            vk_session.auth()
        except vk_api.AuthError as err_msg:
            print(err_msg)

        vk = vk_session.get_api()
        return vk

    def search_recipes(self):
        vk = self._get_vk_session()
        domains = self._get_domain_list()
        recipes = []
        for domain in domains:
            response = vk.wall.search(domain=domain, query=self.query, count=self.count)
            if len(response['items']) != 0:
                text_recipes = response['items']
                recipes.append(text_recipes)
        return recipes

    def _get_auth_from_file(self):
        subfile = self._subfile
        with open(subfile) as sbf:
            auth_log_pass = json.load(sbf)
        login = auth_log_pass['vk_auth']['login']
        password = auth_log_pass['vk_auth']['password']
        return login, password
