from future import standard_library

standard_library.install_aliases()
from builtins import object
import platform
import requests
from requests_file import FileAdapter


class HttpConnection(object):
    def __init__(self):
        self.user_agent = "%s-%s" % ("BuildNotify", platform.platform())

    def connect(self, server, timeout):
        credentials = (server.username, server.password) if server.has_creds() else None
        s = requests.Session()
        s.mount('file://', FileAdapter())

        with s:
            response = s.get(server.url, auth=credentials, verify=server.skip_ssl_verification,
                             headers={'User-Agent': self.user_agent}, timeout=timeout)
            if response.encoding is None:
                response.encoding = 'utf-8'
            response.raise_for_status()
            return response.text
