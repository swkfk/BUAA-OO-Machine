import re

from src.core.settings.GlobalSettings import Globals

server_config = Globals("server")

def get_ws_addr(host, port):
    if port != "":
        host += ":" + port
    reg = re.compile('^http://|https://')
    addr = reg.sub('ws://', host)
    if not addr.startswith("ws://"):
        addr = "ws://" + addr
    return addr
