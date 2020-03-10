from flask import Flask
from flask import request
import logging
import json
import os
import hmac
import hashlib

app = Flask(__name__)


def check_signature(secret_key, request_signature, request_body):
    hasher = hmac.new(secret_key, request_body, hashlib.sha256)
    dig = hasher.hexdigest()

    return hmac.compare_digest(dig, request_signature)


@app.route('/hello')
def hello_world():
    return 'hello world from sqreen redirect'


@app.route('/', methods=['POST'])
def web_hook():
    request_body = request.get_data()
    request_signature = request.headers['X-Sqreen-Integrity']

    write_path = './sqreen_json.txt'
    mode = 'a' if os.path.exists(write_path) else 'w'
    with open(write_path, mode) as f:
        json.dump(request.json, f)
    f.close()
    logging.warning('Here result of checking signature: ')
    check = check_signature(b'e7a40d9c8a66f45092a291b890aa915e19996412e5a1cf8cb8721c4363f1d70d',
                            request_signature, bytes(request_body))
    status = 200 if check else 401
    logging.warning(status)
    return request_body, int(status)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8081"), debug=True)
