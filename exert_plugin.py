from pandare import PyPlugin
class Server(PyPlugin):
    def __init__(self, panda):
        pass

    @PyPlugin.ppp_export
    def do_add(self, x):
        return x+1

class Client(PyPlugin):
    def __init__(self, panda):
        print(self.ppp.Server.do_add(1))