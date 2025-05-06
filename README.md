# python-error-server
A simple Python HTTP server that serves a `sitemap.xml` and a collection of test pages returning various HTTP status codes. Useful for testing crawlers, error handling, and redirect logic in web applications.

## Features

* **sitemap.xml**: Lists all test pages.
* **Home page `(/)`**: A basic HTML welcome page.
* **Test pages `(/pageXXX)`**: Each path returns its configured HTTP status code. Redirect codes (3xx) redirect back to `/`.
* **Fallback**: Any other path returns a 404 Not Found.

## Requirements

* Python 3.6 or higher

## Installation

1. Clone or download this repository.
2. Ensure you have Python 3 installed.

## Usage

1. Save the server script as `server.py`.
2. Run the server:

   ```bash
   python3 server.py
   ```
3. Open your browser or use `curl` to explore:

   * Home page: [http://localhost:8000/](http://localhost:8000/)
   * Sitemap: [http://localhost:8000/sitemap.xml](http://localhost:8000/sitemap.xml)
   * Test pages:

     ```
     http://localhost:8000/page301  # 301 Moved Permanently
     http://localhost:8000/page302  # 302 Found
     http://localhost:8000/page303  # 303 See Other
     http://localhost:8000/page307  # 307 Temporary Redirect
     http://localhost:8000/page308  # 308 Permanent Redirect
     http://localhost:8000/page400  # 400 Bad Request
     http://localhost:8000/page401  # 401 Unauthorized
     http://localhost:8000/page403  # 403 Forbidden
     http://localhost:8000/page404  # 404 Not Found
     http://localhost:8000/page500  # 500 Internal Server Error
     http://localhost:8000/page502  # 502 Bad Gateway
     http://localhost:8000/page503  # 503 Service Unavailable
     http://localhost:8000/page504  # 504 Gateway Timeout
     ```
   * Any other path returns `404 Not Found`.

## Configuration

* **HOST** and **PORT** are defined at the top of `server.py`. You can change them as needed:

  ```python
  HOST = 'localhost'
  PORT = 8000
  ```

* **STATUS\_CODES** mapping in `server.py` controls which paths exist and their response codes.

## Extending

* Add more test pages by updating the `STATUS_CODES` dictionary.
* Customize the sitemap or home page HTML as desired.

## License

This project is released under the MIT License.
