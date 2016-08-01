# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2016 Christian Schwarz
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""A dummy docstring.

You should give some information about your project here.
"""

#### START MICROSERVICE CODE
from builder import make_app

def start_development_server(host, port, debug):
    app = make_app("package")
    app.run(host=host, port=port, debug=debug, threaded=True)

def start_production_server(port):
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    app = make_app("package")

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port)
    IOLoop.instance().start()
#### END MICROSERVICE CODE

if __name__=="__main__":
    print("""This code is executed, whenever the script is called directly.""")
#### START MICROSERVICE INSTANCE CREATION

    import sys
    import os

    if len(sys.argv) < 2:
        print("[Usage] package <PORT>")
        sys.exit()

    HOST  = "0.0.0.0"
    PORT  = int(sys.argv[1])

    DEBUG = not os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-2].endswith("production")

    if debug:
        # Flask's integrated server
        print ("Starting in DEVELOPMENT mode.")
        start_development_server(HOST, PORT, True)
    else:
        # Tornado Server
        print("Starting in PRODUCTION mode.")
        start_production_server(PORT)

#### END MICROSERVICE INSTANCE CREATION
