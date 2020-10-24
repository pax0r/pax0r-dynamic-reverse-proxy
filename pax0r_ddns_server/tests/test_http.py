from unittest import mock

import pytest

from pax0r_ddns_server import http_server
from pax0r_ddns_server.auth_backends.base import AuthBase
from pax0r_ddns_server.containers import Container
from pax0r_ddns_server.http_server import create_app


@pytest.fixture
def mock_auth():
    auth = mock.Mock(spec=AuthBase)
    auth.is_authorized.return_value = True
    return auth


@pytest.fixture
def app(mock_auth):
    container = Container()
    container.wire([http_server])
    with container.auth_backend.override(mock_auth):
        app = create_app(container)
        yield app
    container.unwire()


async def test_get_ip(app, dns_backend_mock):
    dns_backend_mock.get_ip.return_value = "1.2.3.4"
    with app.container.dns_backend.override(dns_backend_mock):
        async with app.asgi_client as client:
            _, response = await client.get('/example.com')

    assert response.status == 200
    data = response.json()
    assert data['ip'] == "1.2.3.4"


async def test_post_ip(app, dns_backend_mock):
    dns_backend_mock.get_ip.return_value = "1.2.3.4"
    with app.container.dns_backend.override(dns_backend_mock):
        async with app.asgi_client as client:
            _, response = await client.post('/example.com', data={})

    assert response.status == 200
    dns_backend_mock.set_ip.assert_called_with('example.com', 'mockserver')


async def test_auth_decorator_not_authorized(app, mock_auth):
    mock_auth.is_authorized.return_value = False
    async with app.asgi_client as client:
        _, response = await client.get('/example.com')

    assert response.status == 401
