from .runner import Runner
import database
import json
from numbers import Number
import os
import git

repo = git.Repo(os.getcwd())
_git = repo.git


class GitCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "git_command"

    def do(self):
        super().do()
        if int(self.sender.id) != 223212153207783435:
            return f"{self.sender.mention} isn't allowed to do that :D"
        try:
            e = " ".join(self.args[0:])
            print(e)
            return eval(e)
        except Exception:
            return Exception
