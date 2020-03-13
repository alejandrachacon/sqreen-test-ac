from injector import singleton
from Services.NotifierService import LogNotifierService, SlackNotifierService


def configure(binder):
    binder.bind(SlackNotifierService, to=SlackNotifierService, scope=singleton)
    binder.bind(LogNotifierService, to=LogNotifierService, scope=singleton)
