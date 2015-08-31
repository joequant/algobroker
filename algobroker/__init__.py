class AlgoBroker(object):
    def hello(self, name):
        return "Hello, %s" % name

class ports(object):
    dispatcher = "tcp://127.0.0.1:5557"
    plivo = "tcp://127.0.0.1:5558"
    alert_set_quote = "tcp://127.0.0.1:5559"
    yahoo_quoter = "tcp://127.0.0.1:5560"

