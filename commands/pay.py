from .runner import Runner
import database


class PayCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "pay_command"

    def do(self):
        super().do()
        if len(self.args) == 2:
            user = self.message.mentions[0]
            if database.get_user(user.id) is None:
                return "That user did not type !start, leave him alone"
            if user is self.sender:
                return "sad lawl trying to pay yourself (didn't work)"
            pay_amount = int(self.args[1])
            if pay_amount < 0:
                return ":thinking:"
            if database.get_balance(self.sender) - pay_amount < 0:
                return "not allowed to give yourself debt"
            if database.add_balance(self.sender, -pay_amount) and database.add_balance(user, pay_amount):
                return f"Transaction completed: you paid {pay_amount} from you to {user.mention}"
            else:
                return "forgot to do !start"
        else:
            return f"command {self.name} has too many or too little arguments ( {self.args})"
