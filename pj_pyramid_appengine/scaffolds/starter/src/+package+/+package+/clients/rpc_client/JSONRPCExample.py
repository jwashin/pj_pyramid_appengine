import pyjd # dummy in pyjs
from pyjamas import DOM
from pyjamas.ui.Widget import Widget
from pyjamas.ui.InnerText import InnerText
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.Button import Button
from pyjamas.ui.HTML import HTML
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.ListBox import ListBox
from pyjamas.JSONService import JSONProxy

class PreFormatted(Widget, InnerText):
    def __init__(self):
        Widget.__init__(self, Element=DOM.createElement('pre'))
        self.addStyleName('preformatted')


class JSONRPCExample:
    def onModuleLoad(self):
        self.TEXT_WAITING = "Waiting for response..."
        self.TEXT_ERROR = "Server Error"
        self.METHOD_ECHO = "Echo"
        self.METHOD_REVERSE = "Reverse"
        self.METHOD_UPPERCASE = "UPPERCASE"
        self.METHOD_LOWERCASE = "lowercase"
        self.METHOD_NONEXISTANT = "Non existant"
        self.methods = [self.METHOD_ECHO, self.METHOD_REVERSE,
                        self.METHOD_UPPERCASE, self.METHOD_LOWERCASE,
                        self.METHOD_NONEXISTANT]

        self.remote_py = EchoServicePython()

        self.status = PreFormatted()
        self.text_area = TextArea()
        self.text_area.setText("""{'Test'} [\"String\"]
\tTest Tab
Test Newline\n
after newline
""" + r"""Literal String:
{'Test'} [\"String\"]
""")
        self.text_area.setCharacterWidth(80)
        self.text_area.setVisibleLines(8)

        self.method_list = ListBox()
        self.method_list.setName("hello")
        self.method_list.setVisibleItemCount(1)
        for method in self.methods:
            self.method_list.addItem(method)
        self.method_list.setSelectedIndex(0)

        method_panel = HorizontalPanel()
        method_panel.add(HTML("Remote string method to call: "))
        method_panel.add(self.method_list)
        method_panel.setSpacing(8)

        #       self.button_php = Button("Send to PHP Service", self)
        self.button_py = Button("Send to Python Service", self)

        buttons = HorizontalPanel()
        #        buttons.add(self.button_php)
        buttons.add(self.button_py)
        buttons.setSpacing(8)

        info = """<h2>JSON-RPC Example</h2>
        <p>This example demonstrates the calling of server services with
           <a href="http://json-rpc.org/">JSON-RPC</a>.
        </p>
        <p>Enter some text below, and press a button to send the text
           to an Echo service on your server. An echo service simply sends the exact same text back that it receives.
           </p>"""

        panel = VerticalPanel()
        panel.add(HTML(info))
        panel.add(self.text_area)
        panel.add(method_panel)
        panel.add(buttons)
        panel.add(self.status)

        RootPanel().add(panel)

    def setStatus(self, text):
        self.status.setText(text)

    def onClick(self, sender):
        self.setStatus(self.TEXT_WAITING)
        method = self.methods[self.method_list.getSelectedIndex()]
        text = self.text_area.getText()

        # demonstrate proxy & callMethod()
        if sender == self.button_py:
            if method == self.METHOD_ECHO:
                self.remote_py.echo(text, self)
            elif method == self.METHOD_REVERSE:
                self.remote_py.reverse(text, self)
            elif method == self.METHOD_UPPERCASE:
                self.remote_py.uppercase(text, self)
            elif method == self.METHOD_LOWERCASE:
                self.remote_py.lowercase(text, self)
            elif method == self.METHOD_NONEXISTANT:
                self.remote_py.nonexistant(text, self)

    def onRemoteResponse(self, response, request_info):
        self.setStatus(response)

    def onRemoteError(self, code, errobj, request_info):
        # onRemoteError gets the HTTP error code or 0 and
        # errobj is an jsonrpc 2.0 error dict:
        #     {
        #       'code': jsonrpc-error-code (integer) ,
        #       'message': jsonrpc-error-message (string) ,
        #       'data' : extra-error-data
        #     }
        message = errobj['message']
        if code:
            self.setStatus("HTTP error %d: %s" %
                           (code, message))
        else:
            code = errobj['code']
            self.setStatus("JSONRPC Error %s: %s" %
                           (code, message))


class EchoServicePython(JSONProxy):
    def __init__(self):
        JSONProxy.__init__(self, "/echo",
            ["echo", "reverse", "uppercase", "lowercase", "nonexistant"])

if __name__ == '__main__':
    # for pyjd, set up a web server and load the HTML from there:
    # this convinces the browser engine that the AJAX will be loaded
    # from the same URI base as the URL, it's all a bit messy...
    pyjd.setup("http://localhost:8080/static/JSONRPCExample_gtk.html")
    app = JSONRPCExample()
    app.onModuleLoad()
    pyjd.run()

