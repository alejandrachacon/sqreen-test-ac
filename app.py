from flask import Flask
from flask import request
import hmac
import hashlib
from flask_injector import FlaskInjector
from injector import inject

from Services.NotifierService import SlackNotifierService, LogNotifierService

from dependencies import configure

app = Flask(__name__)
FlaskInjector(app=app, modules=[configure])


def check_signature(secret_key, request_signature, request_body):
    hasher = hmac.new(secret_key, request_body, hashlib.sha256)
    dig = hasher.hexdigest()

    return hmac.compare_digest(dig, request_signature)


@app.route('/hello')
def hello_world():
    return 'hello world from sqreen redirect'


@inject
@app.route('/', methods=['POST'])
def web_hook(slack_notifier: SlackNotifierService, log_notifier: LogNotifierService):
    request_body = request.get_data()
    request_signature = request.headers['X-Sqreen-Integrity']

    check = check_signature(b'e7a40d9c8a66f45092a291b890aa915e19996412e5a1cf8cb8721c4363f1d70d',
                            request_signature, bytes(request_body))
    status = 200 if check else 401


    log_notifier.send_message("hey, you seem to have a problem - log")
    slack_notifier.send_message("hey, you seem to have a problem - slack")
    return request_body, int(status)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8081"), debug=True)

