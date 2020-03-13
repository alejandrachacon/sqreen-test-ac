import logging
import slack


class INotifier(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return callable(subclass.send_message)


class NotifierService(metaclass=INotifier):
    notifier = ''

    def __init__(self, sender):
        print(f"Notifier Instance Up ", type(sender))
        self.notifier = sender

    def send_message(self, msg):
        print(msg)
        self.notifier.send(msg)

    @staticmethod
    def hello_world():
        return 'Hello World from Notifier'


class SlackNotifierService(NotifierService):

    class SlackNotifier:
        channel = 'general'
        token = 'xoxp-973929692242-986262486724-987762198995-7dbb397fa399d773e3d93a6e672cf30e'

        def __init__(self):
            print("Init Slack Notifier Inner Class")

        def send(self, message):
            client = slack.WebClient(self.token, timeout=30)
            client.chat_postMessage(
                channel=self.channel,
                text=message)
            print("slack msg sent.")

    def __init__(self):
        super().__init__(self.SlackNotifier())


class LogNotifierService(NotifierService):
    class LogNotifier:
        def __init__(self):
            print("Init Log Notifier Inner Class")

        def send(self, message):
            logging.info(message)

    def __init__(self):
        super().__init__(self.LogNotifier())



