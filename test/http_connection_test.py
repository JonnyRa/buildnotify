from future import standard_library

standard_library.install_aliases()
from builtins import object
import os
import pytest
from requests import HTTPError
import requests_mock

from buildnotifylib.core.http_connection import HttpConnection
from buildnotifylib.serverconfig import ServerConfig


def test_should_fetch_data():
    file_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "../../data/cctray.xml")
    response = HttpConnection().connect(ServerConfig('file://' + file_path, [], '', '', None, None), 10)
    assert response == open(file_path, 'r').read()


def test_should_pass_auth_if_provided():
    with requests_mock.mock() as m:
        m.get('http://url', text='content')
        response = HttpConnection().connect(ServerConfig('http://url', [], '', '', "user", "pass"), 10)
    assert response == 'content'


def test_should_ignore_bad_urls():
    with pytest.raises(HTTPError) as ex:
        HttpConnection().connect(ServerConfig('file:///url/missing/', [], '', '', "user", "pass"), 10)
    assert '404 Client Error' in str(ex.value)


class Matcher(object):
    def __init__(self, compare):
        self.compare = compare

    def __eq__(self, other):
        return self.compare(other)
