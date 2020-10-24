from unittest import mock

import pytest

from pax0r_ddns_server.dns_backends.base import BackendBase


@pytest.fixture
def dns_backend_mock():
    return mock.Mock(spec=BackendBase)
