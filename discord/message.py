from munch import Munch

class Message(Munch):
    def __init__(self, message):
        super(Message, self).__init__(message)