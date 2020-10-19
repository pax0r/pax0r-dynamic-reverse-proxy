from pax0r_ddns_server.dns_backends.base import BackendBase


class MemoryBackend(BackendBase):
    def __init__(self):
        self._memory = {}

    def get_ip(self, domain):
        return self._memory.get(domain)

    def set_ip(self, domain, ip):
        self._memory[domain] = ip
