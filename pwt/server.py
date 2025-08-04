from http.server import SimpleHTTPRequestHandler, HTTPServer
import mimetypes

# Add custom MIME type for .hta
mimetypes.add_type('text/html', '.hta')

class HTAHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')  # Optional, disable caching
        SimpleHTTPRequestHandler.end_headers(self)

PORT = 8000

httpd = HTTPServer(('0.0.0.0', PORT), HTAHandler)
print(f"Serving on port {PORT}...")
httpd.serve_forever()
