import http.server
import mimetypes
import os
import sys
import urllib.parse

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

mimetypes.add_type('image/avif', '.avif')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

class PortfolioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Language routing
        if path in ('/id', '/id/'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(os.path.join(DIRECTORY, 'id.html'), 'rb') as f:
                self.wfile.write(f.read())
            return

        if path in ('/', '/en', '/en/'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(os.path.join(DIRECTORY, 'index.html'), 'rb') as f:
                self.wfile.write(f.read())
            return

        if path.startswith('/cdn-cgi/l/email-protection'):
            self.send_response(204)
            self.end_headers()
            return

        # Handle Next.js image optimizer endpoint: /_next/image?url=...
        if path == '/_next/image':
            query = urllib.parse.parse_qs(parsed.query)
            if 'url' in query:
                img_path = query['url'][0].lstrip('/')
                full_path = os.path.join(DIRECTORY, img_path)
                if not os.path.exists(full_path):
                    base, ext = os.path.splitext(img_path)
                    for alt_ext in ['.svg', '.webp', '.avif', '.png', '.jpg']:
                        if os.path.exists(os.path.join(DIRECTORY, base + alt_ext)):
                            img_path = base + alt_ext
                            break
                self.path = '/' + img_path
                return super().do_GET()

        return super().do_GET()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), PortfolioHandler)
    url = f'http://localhost:{PORT}'
    print(f'Portfolio server running at: {url}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
