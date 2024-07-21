import requests
import os
from urllib.parse import urlparse, unquote

def extract_file_url(url):
    # Remove any query parameters or fragments
    url = url.split('?')[0].split('#')[0]
    if url.endswith('/'):
        return 'index.html'  # Default to 'index.html' if URL ends with a slash
    filename = url[url.rfind('/') + 1:]
    return filename if filename else 'index.html'  # Default to 'index.html' if no filename is found

def get_website_name(url):
    # Extract the website name from the URL including subdomains, using dots (e.g., phw.servegame.com -> phw.servegame.com)
    domain = urlparse(url).netloc
    return domain  # Keep the domain with dots

def clean_url_path(path):
    # Decode URL encoding and make it suitable for file paths
    # Remove leading slashes and replace URL-encoded slashes with OS-specific separators
    return unquote(path).lstrip('/').replace('/', os.sep).replace('\\', os.sep)

def status_code_message(status):
    status_messages = {
        200: "200 - OK",
        201: "201 - Created",
        202: "202 - Accepted",
        203: "203 - Non-Authoritative Information",
        204: "204 - No Content",
        205: "205 - Reset Content",
        206: "206 - Partial Content",
        300: "300 - Multiple Choices",
        301: "301 - Moved Permanently",
        302: "302 - Found",
        303: "303 - See Other",
        304: "304 - Not Modified",
        305: "305 - Use Proxy",
        307: "307 - Temporary Redirect",
        308: "308 - Permanent Redirect",
        400: "400 - Bad Request",
        401: "401 - Unauthorized",
        402: "402 - Payment Required",
        403: "403 - Forbidden",
        404: "404 - Not Found",
        405: "405 - Method Not Allowed",
        406: "406 - Not Acceptable",
        407: "407 - Proxy Authentication Required",
        408: "408 - Request Timeout",
        409: "409 - Conflict",
        410: "410 - Gone",
        411: "411 - Length Required",
        412: "412 - Precondition Failed",
        413: "413 - Payload Too Large",
        414: "414 - URI Too Long",
        415: "415 - Unsupported Media Type",
        416: "416 - Range Not Satisfiable",
        417: "417 - Expectation Failed",
        418: "418 - I'm a teapot",  # Fun Easter egg status code
        421: "421 - Misdirected Request",
        422: "422 - Unprocessable Entity",
        423: "423 - Locked",
        424: "424 - Failed Dependency",
        425: "425 - Too Early",
        426: "426 - Upgrade Required",
        428: "428 - Precondition Required",
        429: "429 - Too Many Requests",
        431: "431 - Request Header Fields Too Large",
        451: "451 - Unavailable For Legal Reasons",
        500: "500 - Internal Server Error",
        501: "501 - Not Implemented",
        502: "502 - Bad Gateway",
        503: "503 - Service Unavailable",
        504: "504 - Gateway Timeout",
        505: "505 - HTTP Version Not Supported",
        506: "506 - Variant Also Negotiates",
        507: "507 - Insufficient Storage",
        508: "508 - Loop Detected",
        510: "510 - Not Extended",
        511: "511 - Network Authentication Required"
    }
    return status_messages.get(status, f"{status} - Status not in program dictionary")

while True:
    URL = input('Please input URL without the "HTTPS://" or "HTTP://": ').strip()
    
    try:
        full_url = f"http://{URL}"
        r = requests.get(full_url)

        status = r.status_code
        print(f"Status Code: {status_code_message(status)}")

        if status == 200:  # Only process if the request was successful
            website_name = get_website_name(full_url)
            base_path = website_name

            # Construct the file path based on the URL path
            url_path = urlparse(r.url).path
            file_path = os.path.join(base_path, clean_url_path(url_path))
            
            # Default to 'index.html' if file_path is a directory (i.e., path ends with a separator)
            if not file_path or file_path.endswith(os.sep):
                file_path = os.path.join(file_path, 'index.html')

            # Ensure the directory structure exists
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # Write the content to the file
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"File saved successfully: {file_path}")
        else:
            print(f"Request failed with status code {status}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
