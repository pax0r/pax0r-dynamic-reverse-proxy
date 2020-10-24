from unittest import mock

import pytest
from dnslib import DNSRecord, RCODE

from pax0r_ddns_server.dns_server import DynamicResolver


@pytest.fixture
def dns_resolver(dns_backend_mock):
    return DynamicResolver(dns_backend_mock)


def test_resolver_backend_returns_ip(dns_backend_mock, dns_resolver):
    dns_backend_mock.get_ip.return_value = "1.2.3.4"
    question = DNSRecord.question("example.com")
    reply = dns_resolver.resolve(question, mock.MagicMock())
    assert (
        str(reply.get_a()) == "example.com.            60      IN      A       1.2.3.4"
    )


def test_resolver_backends_returns_none(dns_backend_mock, dns_resolver):
    dns_backend_mock.get_ip.return_value = None
    question = DNSRecord.question("example.com")
    reply = dns_resolver.resolve(question, mock.MagicMock())
    assert reply.header.rcode == getattr(RCODE, "NXDOMAIN")
