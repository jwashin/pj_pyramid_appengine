from pyramid_rpc.jsonrpc import jsonrpc_method

class EchoService(object):
    def __init__(self, request):
        self.request = request

    @jsonrpc_method(endpoint='echoservice')
    def echo(self, msg):
        return msg


    @jsonrpc_method(endpoint='echoservice')
    def reverse(self, msg):
        return msg[::-1]


    @jsonrpc_method(endpoint='echoservice')
    def uppercase(self, msg):
        return msg.upper()


    @jsonrpc_method(endpoint='echoservice')
    def lowercase(self, msg):
        return msg.lower()
