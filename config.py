default_prefix = "!"
prefix = {}


def get_prefix(server_hash):
    if server_hash not in prefix.keys():
        return default_prefix
    else:
        return prefix[server_hash]


def set_prefix(server_hash, value: str):
    prefix[server_hash] = value
