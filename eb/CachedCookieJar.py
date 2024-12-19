from typing import Union
from browser_cookie3 import ChromiumBased, FirefoxBased, Brave
import pickle
import os

from requests.cookies import RequestsCookieJar

class CachedCookieJar:
    def __init__(self, domain_name, cookie_file, cache_file='cookies.pkl', loader: Union[ChromiumBased, FirefoxBased] = Brave):
        self.domain_name = domain_name
        self.cookie_file = cookie_file
        self.cache_file = cache_file
        self.loader = loader

        self.jar = RequestsCookieJar()

    def _update_jar(self, cookies):
        self.jar.clear()

        for cookie in cookies:
            self.jar.set_cookie(cookie)

    def load(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                cookies = pickle.load(f)
                self._update_jar(cookies)
        else:
            cookies = self.loader(domain_name=self.domain_name, cookie_file=self.cookie_file).load()
            self._update_jar(cookies)

    def save(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.jar, f)

    def __enter__(self):
        self.load()
        return self.jar

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
