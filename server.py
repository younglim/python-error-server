#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = 'localhost'
PORT = 8000

# Map paths → status codes
STATUS_CODES = {
    'page301': 301,
    'page302': 302,
    'page303': 303,
    'page307': 307,
    'page308': 308,
    'page400': 400,
    'page401': 401,
    'page403': 403,
    'page404': 404,
    'page500': 500,
    'page502': 502,
    'page503': 503,
    'page504': 504,
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # (1) gracefully ignore browser favicon requests
        if self.path == '/favicon.ico':
            try:
                self.send_response(204)  # No Content
                self.end_headers()
            except BrokenPipeError:
                pass
            return

        # Serve the sitemap
        if self.path == '/sitemap.xml':
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'application/xml; charset=utf-8')
                self.end_headers()

                urls = "\n".join(
                    f"  <url><loc>http://{HOST}:{PORT}/{p}</loc></url>"
                    for p in STATUS_CODES
                )
                sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
                self.wfile.write(sitemap.encode('utf-8'))
            except BrokenPipeError:
                pass
            return

        # Handle each fake page with its status code
        key = self.path.lstrip('/')
        if key in STATUS_CODES:
            code = STATUS_CODES[key]
            try:
                self.send_response(code)
                # for redirects, point back to root
                if code in (301, 302, 303, 307, 308):
                    self.send_header('Location', f'http://{HOST}:{PORT}/')
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                body = f"This is {self.path!r}, returning HTTP {code}"
                self.wfile.write(body.encode('utf-8'))
            except BrokenPipeError:
                pass
            return

        # Serve a simple home page so redirects to “/” don’t 404
        if self.path == '/' or self.path == '':
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()

                links = "\n".join(
                    f'<li><a href="/{p}">/{p} → HTTP {STATUS_CODES[p]}</a></li>'
                    for p in sorted(STATUS_CODES)
                )
                homepage = f"""
<html>
  <head><title>Home</title></head>
  <body>
    <h1>Welcome</h1>
    <p>Try your <a href="/sitemap.xml">sitemap</a> or one of the /pageXXX URLs below:</p>
    <ul>
      {links}
    </ul>
  </body>
</html>
"""
                self.wfile.write(homepage.encode('utf-8'))
            except BrokenPipeError:
                pass
            return

        # Fallback for any other path
        try:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'Not found')
        except BrokenPipeError:
            pass

if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Serving on http://{HOST}:{PORT}/  (CTRL+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
