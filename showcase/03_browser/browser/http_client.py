"""Host HTTP client for Vākya Mini Browser.

Handles network requests for http://, https://, and local file:// schemes.
"""

import os
import urllib.request
import urllib.error
from typing import Dict, Optional, Tuple


def fetch_url(url: str, timeout: int = 5) -> Tuple[int, str, Dict[str, str]]:
    """
    Fetch raw HTML/text content from a URL.
    Returns (status_code, body_text, headers_dict).
    """
    url = url.strip()
    if not url:
        return 400, "<html><body><h1>400 Bad Request</h1><p>Empty URL provided.</p></body></html>", {}

    if url.startswith("file://"):
        file_path = url[7:]
        # On Windows, normalize file path if needed
        if file_path.startswith("/") and len(file_path) > 2 and file_path[2] == ":":
            file_path = file_path[1:]
        if not os.path.exists(file_path):
            return 404, f"<html><body><h1>404 Not Found</h1><p>Local file not found: {file_path}</p></body></html>", {}
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return 200, content, {"content-type": "text/html"}
        except Exception as e:
            return 500, f"<html><body><h1>500 Internal Error</h1><p>Failed to read file: {e}</p></body></html>", {}

    if not url.startswith("http://") and not url.startswith("https://"):
        # Auto-prefix http
        url = "https://" + url

    headers = {
        "User-Agent": "VakyaMiniBrowser/0.2.0 (Educational Browser Engine; Sanskrit-Inspired Architecture)"
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset, errors="replace")
            res_headers = dict(response.headers)
            return status_code, body, res_headers
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return e.code, body, dict(e.headers) if hasattr(e, "headers") else {}
    except urllib.error.URLError as e:
        return 502, f"<html><body><h1>502 Bad Gateway</h1><p>Connection failed: {e.reason}</p></body></html>", {}
    except Exception as e:
        return 500, f"<html><body><h1>500 Internal Server Error</h1><p>{str(e)}</p></body></html>", {}
