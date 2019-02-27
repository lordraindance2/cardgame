from .runner import Runner
from database import c, connect
execute = c.execute
fetch = c.fetchall


class SqlCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "sql_command"

    def do(self):
        super().do()
        if int(self.sender.id) != 223212153207783435:
            return f"{self.sender.mention} isn't allowed to do that :D"
        try:
            if self.args[0] == "save":
                connect.commit()
                return "I think it saved"
            else:
                e = " ".join(self.args[0:])
                execute(e)
                a = c.fetchall()
                print(a)
                return str(a)
        except Exception:
            return Exception
