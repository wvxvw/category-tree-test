#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
from os import path
from urlparse import urlparse

from category_tree import category_tree

def Handler(impl='recursive'):
    '''
    Factory for generating CategoryTreeHandler with different
    CategoryTree implementations.
    impl - see `help(category_tree)', type argument.
    '''
    class CategoryTreeHandler(BaseHTTPRequestHandler):

        web = path.join(path.dirname(path.realpath(__file__)), '../web/')
    
        statics = { '.html' : 'text/html',
                    '.htm' : 'text/html',
                    '.js' : 'application/javascript',
                    '.css' : 'text/css' }

        tree = category_tree(type=impl)

        def serve_static(self, file, mime):
            '''
            Serves static files with given mime-type.
            '''
            try:
                with open(path.join(self.web, file), 'r') as served:
                    self.send_response(200)
                    self.send_header('Content-type', mime)
                    self.end_headers()
                    self.wfile.write(served.read())
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)

        def fail(self):
            '''
            Sends internal server error message.
            '''
            self.send_error(500, 'Don\'t know what to do with: %s' % self.path)
        
        def do_GET(self):
            '''
            Handles HTTP GET requests.
            '''
            url = urlparse(self.path)
            extension = path.splitext(url.path)[1] or '.html'
            if self.path == '/':
                self.serve_static('index.html', self.statics['.html'])
            elif extension.lower() in self.statics:
                self.serve_static(url.path[1:], self.statics[extension.lower()])
            else: self.fail()

        def send_preamble(self):
            '''
            Starts sending success message.
            '''
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        
        def do_POST(self):
            '''
            Hanles AJAX requests.
            '''
            length = int(self.headers['content-length'])
            data = self.rfile.read(length)
            if self.path == '/categories/get':
                self.send_preamble()
                self.wfile.write(str(self.tree))
            elif self.path == '/categories/put':
                self.tree.add(data)
                self.wfile.write(str(self.tree))
            else: self.fail()
    return CategoryTreeHandler
                
if __name__ == '__main__':
    try:
        parser = OptionParser()
        parser.add_option(
            '-p', '--port', dest = 'port', default = 8080,
            help = '''The port operated by HTTP server.
            Defaults to 8080.''')
        parser.add_option(
            '-i', '--implementation', dest = 'implementation',
            default = 'recursive', help = 'CategoryTree implementation.')

        options, args = parser.parse_args()
        server = HTTPServer(('', int(options.port)),
                            Handler(options.implementation))
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
