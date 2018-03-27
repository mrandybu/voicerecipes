from voiceserver.api_for_vk import GetVkApi
from flask import Flask, request


class Server(object):
    def __init__(self, query=None):
        self.query = query

    def request_to_vk(self):
        new_request = GetVkApi(query=self.query, count=10)
        res = new_request.search_recipes()
        return res


req = Server(query='fish')
print(req.request_to_vk()[0]['text'])


"""
app = Flask(__name__)


@app.route('/', methods=['POST'])
def input_request():
    if request.method == 'POST':
        req_str = request.data
        req_to_server = Server(query=req_str)
        res = req_to_server.request_to_vk()
        return res

    else:
        return 'Error request'


if __name__ == '__main__':
    app.run()
"""
