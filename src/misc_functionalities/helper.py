import re
def ping_to_id(ping):
    return re.sub("\D", "", ping)