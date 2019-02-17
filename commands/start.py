from .runner import Runner
import database


class StartCommand(Runner):

    def __init__(self, client, message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "start_command"

    def do(self):
        super().do()
        if len(self.args) == 0:
            if database.init_user(self.sender) and database.add_balance(self.sender, 25):
                return  f"hello {self.sender.mention}! Welcome to your favorite card game! \n" \
                        f"To get started, buy some packs with your newly earned 25 monay \n" \
                        f"If you need help, type !help"
            else:
                return f"perhaps you did this already ?"
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
