
class Runner:

    def __init__(self, client,  message, sender, args):

        self.__name = "base_command"
        self.__client = client
        self.__sender = sender
        self.__message = message
        self.__args = args

    def do(self):
        return f"{self.sender.name} runs command: {self.name} with {self.args}"

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def client(self):
        return self.__client

    @property
    def message(self):
        return self.__message

    @property
    def sender(self):
        return self.__sender

    @property
    def args(self):
        return self.__args

