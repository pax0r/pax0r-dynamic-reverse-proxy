from dependency_injector.wiring import Provide
from dnslib import RR, DNSRecord, RCODE
from dnslib.server import DNSServer

from pax0r_ddns_server.dns_backends.base import BackendBase
from pax0r_ddns_server.containers import Container


class DynamicResolver:
    def __init__(self, backend: BackendBase = Provide[Container.dns_backend]):
        self.backend = backend
        self.ttl = 60

    def resolve(self, request: DNSRecord, handler):
        qname = request.q.qname
        domain = str(qname).strip(".")
        ip = self.backend.get_ip(domain)
        reply = request.reply()
        if ip:
            zone = "{} {} A {}".format(qname, self.ttl, ip)
            reply.add_answer(*RR.fromZone(zone))
        else:
            reply.header.rcode = getattr(RCODE, 'NXDOMAIN')
        return reply


def create_server(bind_host: str = Provide[Container.config.dns_host], bind_port: int = Provide[Container.config.dns_port]):
    return DNSServer(DynamicResolver(), port=bind_port, address=bind_host)
