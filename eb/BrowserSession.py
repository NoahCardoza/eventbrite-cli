from typing import Dict, Optional
from requests import Session
from eb.CachedCookieJar import CachedCookieJar

CHROMIUM_HEADERS = {
    'Pragma': 'no-cache',
    'Sec-Ch-Ua': '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-Gpc': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

class BrowserSession:
    def __init__(self, cached_cookie_jar: CachedCookieJar, headers: Optional[Dict[str, str]] = None):
        self.cached_cookie_jar = cached_cookie_jar
        self.headers = headers

    def __enter__(self):
        cookies_jar = self.cached_cookie_jar.__enter__()
        self.session = Session()
        
        self.session.headers.update(CHROMIUM_HEADERS)
        if self.headers:
            self.session.headers.update(self.headers)

        self.session.cookies = cookies_jar
        
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cached_cookie_jar.__exit__(exc_type, exc_val, exc_tb)
        self.session.close()