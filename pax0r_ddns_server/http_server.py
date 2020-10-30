import functools

from dependency_injector.wiring import Provide
from sanic import Sanic
from sanic.exceptions import Unauthorized
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_validation import validate_json

from pax0r_ddns_server.auth_backends.base import AuthBase
from pax0r_ddns_server.containers import Container
from pax0r_ddns_server.dns_backends.base import BackendBase
from pax0r_ddns_server.utils import method_decorator


def auth_required(**backend_kwargs):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(self, request, *args, **kwargs):
            if self.auth_backend.is_authorized(request, **backend_kwargs):
                return f(self, request, *args, **kwargs)
            raise Unauthorized("Auth required.")

        return wrapped

    return decorator


class SimpleView(HTTPMethodView):
    def __init__(
        self,
        auth_backend: AuthBase = Provide[Container.auth_backend],
        dns_backend: BackendBase = Provide[Container.dns_backend],
    ):
        self.dns_backend = dns_backend
        self.auth_backend = auth_backend

    @auth_required()
    def get(self, request, domain):
        return json({"ip": self.dns_backend.get_ip(domain)})

    @auth_required()
    @method_decorator(validate_json({
        "ip": {
            "type": "string",
            "regex": r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            "required": False,
        }
    }, clean=True))
    def post(self, request, domain, valid_json):
        ip = valid_json.get("ip")
        if not ip:
            ip = request.ip
        self.dns_backend.set_ip(domain, ip)
        return self.get(request, domain)


def create_app(container) -> Sanic:
    """Create and return Sanic application."""
    app = Sanic("pax0r_ddns_server")
    app.container = container
    app.add_route(SimpleView.as_view(), "/<domain:path>")
    return app


def start_server(
    container,
    host: str = Provide[Container.config.http_host],
    port: int = Provide[Container.config.http_port],
):
    app = create_app(container)
    app.run(host=host, port=port)
