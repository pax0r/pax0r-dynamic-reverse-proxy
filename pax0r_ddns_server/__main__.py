from pax0r_ddns_server import dns_server, http_server
from pax0r_ddns_server.containers import Container

container = Container()
container.config.from_yaml('config.yaml')
container.wire(modules=[dns_server, http_server])

dns = dns_server.create_server()
dns.start_thread()

http_server.start_server(container)
