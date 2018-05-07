from voiceserver.api_for_vk import GetVkApi
from flask import Flask


class Server(object):
    def __init__(self, query=None):
        self.query = query

    def request_to_vk(self):
        new_request = GetVkApi(query=self.query, count=10)
        response = new_request.search_recipes()
        return response


app = Flask(__name__)


@app.route('/recipes/<recipe_name>')
def get_request(recipe_name=None):
    request_to_server = Server(recipe_name)
    response = request_to_server.request_to_vk()
    recipes_list = []
    for domain in response:
        for recipe in domain:
            recipes_list.append(recipe['text'])
    recipes_list_to_str = str(recipes_list)
    return recipes_list_to_str


if __name__ == '__main__':
    app.run()
