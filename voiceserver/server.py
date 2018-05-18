from flask import Flask
from voiceserver.server_func import ServerFunctions


class Server(object):
    def __init__(self, query=None):
        self.query = query

    def request_to_vk(self):
        get_server = ServerFunctions(self.query)
        recipes_list = get_server.preprocessing_recipe_text()
        return recipes_list


app = Flask(__name__)


@app.route('/recipes/<recipe_name>')
def get_request(recipe_name=None):
    server = Server(recipe_name)
    return server.request_to_vk()


if __name__ == '__main__':
    app.run()
