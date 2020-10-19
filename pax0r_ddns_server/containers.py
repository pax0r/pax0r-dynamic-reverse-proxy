from dependency_injector import containers, providers

from pax0r_ddns_server.dns_backends.base import BackendBase
from pax0r_ddns_server.dns_backends.memory import MemoryBackend


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    dns_backend = providers.Singleton(MemoryBackend)
