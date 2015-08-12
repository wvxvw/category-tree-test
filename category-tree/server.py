#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
from os import path
from urlparse import urlparse

from category_tree import category_tree

class PTDevHandler(BaseHTTPRequestHandler):

    web = path.join(path.dirname(path.realpath(__file__)), '../web/')
    
    statics = { '.html' : 'text/html',
                '.htm' : 'text/html',
                '.jpg' : 'image/jpg',
                '.jpeg' : 'image/jpg',
                '.png' : 'image/png',
                '.mp3' : 'audio/mpeg',
                '.xml' : 'text/xml',
                '.swf' : 'application/x-shockwave-flash',
                '.gif' : 'image/gif',
                '.js' : 'application/javascript',
                '.css' : 'text/css' }

    tree = category_tree()

    def serve_static(self, file, mime):
        '''The handler for static files'''
        try:
            with open(path.join(self.web, file), 'r') as served:
                self.send_response(200)
                self.send_header('Content-type', mime)
                self.end_headers()
                self.wfile.write(served.read())
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def fail(self):
        self.send_error(500, 'Don\'t know what to do with: %s' % self.path)
        
    def do_GET(self):
        '''Mandatory GET handler'''
        url = urlparse(self.path)
        extension = path.splitext(url.path)[1] or '.html'
        if self.path == '/':
            self.serve_static('index.html', self.statics['.html'])
        elif extension.lower() in self.statics:
            self.serve_static(url.path[1:], self.statics[extension.lower()])
        else: self.fail()

    def send_preamble(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_POST(self):
        length = int(self.headers['content-length'])
        data = self.rfile.read(length).split('/')
        print 'got post request: %s, %s' % (self.path, data)
        if self.path == '/categories/get':
            self.send_preamble()
            self.wfile.write(str(self.tree))
        elif self.path == '/categories/put':
            prefix, last = data[:-1], data[-1]
            self.tree.add('/'.join(prefix), last)
            self.wfile.write(str(self.tree))
        else: self.fail()
                
if __name__ == '__main__':
    try:
        parser = OptionParser()
        parser.add_option(
            '-p', '--port', dest = 'port', default = 8080,
            help = '''The port operated by HTTP server.
            Defaults to 8080.''')

        options, args = parser.parse_args()
        server = HTTPServer(('', int(options.port)), PTDevHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()