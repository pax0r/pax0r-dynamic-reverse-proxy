from unittest import mock

import pytest
from dnslib import DNSRecord, RCODE

from pax0r_ddns_server.dns_backends.base import BackendBase
from pax0r_ddns_server.dns_server import DynamicResolver


@pytest.fixture
def backend_mock():
    return mock.Mock(BackendBase)


@pytest.fixture
def dns_resolver(backend_mock):
    return DynamicResolver(backend_mock)


def test_resolver_backend_returns_ip(backend_mock, dns_resolver):
    backend_mock.get_ip.return_value = "1.2.3.4"
    question = DNSRecord.question("example.com")
    reply = dns_resolver.resolve(question, mock.MagicMock())
    assert str(reply.get_a()) == 'example.com.            60      IN      A       1.2.3.4'


def test_resolver_backends_returns_none(backend_mock, dns_resolver):
    backend_mock.get_ip.return_value = None
    question = DNSRecord.question("example.com")
    reply = dns_resolver.resolve(question, mock.MagicMock())
    assert reply.header.rcode == getattr(RCODE, 'NXDOMAIN')

