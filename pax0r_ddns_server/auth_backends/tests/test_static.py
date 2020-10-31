from unittest import mock
from wsgiref.headers import Headers

import pytest

from pax0r_ddns_server.auth_backends.static import StaticAuth


@pytest.fixture
def static_auth():
    return StaticAuth("test")


def test_auth_ok(static_auth):
    request = mock.Mock()
    request.headers = Headers([("authorization", "Bearer test")])
    assert static_auth.is_authorized(request)


def test_no_auth_header(static_auth):
    request = mock.Mock()
    request.headers = Headers([])
    assert not static_auth.is_authorized(request)


def test_wrong_token(static_auth):
    request = mock.Mock()
    request.headers = Headers([("authorization", "Bearer wrong")])
    assert not static_auth.is_authorized(request)
