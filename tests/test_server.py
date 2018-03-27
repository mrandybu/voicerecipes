import requests
import json
import io


def set_data():
    ip_file = open('vk_auth.l')
    ip = ip_file.read().split('\n')[2]
    data = 'каша'.encode('utf-8')
    res = requests.post(ip, data)
    if res.ok:
        s = res.text
        print(s)
    else:
        print('error')


if __name__ == '__main__':
    set_data()
