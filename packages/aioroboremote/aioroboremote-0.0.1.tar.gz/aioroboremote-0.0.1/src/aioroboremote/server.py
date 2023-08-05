import aiohttp.web

from .library import RoboLibraryBase
from aioroboremote.internal.view import XmlRpcView


__slots__ = ['RoboServer']


class RoboServer(object):
    def __init__(self, libraries: dict[str, RoboLibraryBase] | RoboLibraryBase):
        app = aiohttp.web.Application()

        if isinstance(libraries, dict):
            for path, library in libraries.items():
                app.router.add_route('*', f'/{path}', self._make_handler(library))
        elif isinstance(libraries, RoboLibraryBase):
            app.router.add_route('*', '/RPC2', self._make_handler(libraries))
        else:
            raise TypeError(f"invalid type for 'libraries'")

        self._app = app

    def serve(self, host: str = "127.0.0.1", port: int = 8270):
        aiohttp.web.run_app(self._app, host=host, port=port)

    def _make_handler(self, library):
        async def f(request):
            return await XmlRpcView(library, request)
        return f
