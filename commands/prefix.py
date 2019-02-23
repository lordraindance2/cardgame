from .runner import Runner
from database import get_prefix, set_prefix


class PrefixCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "prefix_command"

    def do(self):
        super().do()
        server_id = int(self.server.id)
        my_id = 223212153207783435
        if len(self.args) == 0:
            return f"Current Prefix: {get_prefix(server_id)}"
        elif len(self.args) == 1:
            print(f"{int(self.sender.id)} is {my_id} {my_id != int(self.sender.id)}")
            if int(self.sender.id) != my_id:
                if not self.sender.server_permissions.administrator or \
                        self.sender != self.server.owner:
                    return "You must be the server owner to set this"
            former = get_prefix(server_id)
            set_prefix(server_id, self.args[0])
            return f"Prefix changed from {former} to {get_prefix(server_id)}"
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
