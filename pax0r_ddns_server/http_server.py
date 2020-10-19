import sys

from dependency_injector.wiring import Provide
from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView

from pax0r_ddns_server.backends.base import BackendBase
from pax0r_ddns_server.containers import Container


class SimpleView(HTTPMethodView):
    def __init__(self, dns_backend: BackendBase = Provide[Container.dns_backend],):
        self.dns_backend = dns_backend

    def get(self, request, domain):
        return json({
            "ip": self.dns_backend.get_ip(domain)
        })

    def post(self, request, domain):
        data = request.json
        self.dns_backend.set_ip(domain, request.ip)
        return self.get(request, domain)


def create_app(container) -> Sanic:
    """Create and return Sanic application."""
    app = Sanic("pax0r_ddns_server")
    app.container = container
    app.add_route(SimpleView.as_view(), '/<domain:path>')
    return app


def start_server(container, host: str = Provide[Container.config.http_host], port: int = Provide[Container.config.http_port]):
    app = create_app(container)
    app.run(host=host, port=port)
