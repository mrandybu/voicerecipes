from voiceserver.api_for_vk import GetVkApi


class FakeServer(object):
    def __init__(self, query):
        self.query = query

    def _get_recipes(self):
        request = GetVkApi(query=self.query, count=10)
        get_recipes = request.search_recipes()
        return get_recipes

    def response_to_json(self, response):
        response = self._get_recipes()
        return response
