from http import HTTPStatus
from typing import Iterable

from config.app_config import ApplicationConfig
from sanic.request import Request
from sanic.response import BaseHTTPResponse

from PSP_film_project.api_server.context import Context


class SanicEndpoint:

    def __init__(self, config: ApplicationConfig, context: Context, uri: str, methods: Iterable, *args, **kwargs):
        self.uri = uri
        self.config = config
        self.context = context
        self.methods = methods
        self.__name__ = self.__class__.__name__

    async def __call__(self, *args, **kwargs):
        return await self.handler(*args, **kwargs)

    @staticmethod
    async def make_response_json(
            body: dict = None, status: int = 200, messages: str = None, error_code: int = None
    ) -> BaseHTTPResponse:
        pass

    @staticmethod
    def import_body_json(request: Request):
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    @staticmethod
    def import_body_headers(request: Request):
        return {
            header: value
            for header, value in request.headers.items()
            if header.lower().startswith('x-')
        }

    async def headers(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        body = {}

        body.update(self.import_body_json(request))
        body.update(self.import_body_headers(request))

        return await self._method(request, body, *args, **kwargs)

    async def _method(self, request: Request, body: dict, *args, **kwargs):
        method = request.method.lower()
        func_name = f'method_{method}'

        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return await func(request, body, *args, **kwargs)
        return await self.method_not_impl(method=method)

    async def method_not_impl(self, method: str) -> BaseHTTPResponse:
        return await self.make_response_json(status=500, messages=f'Method {method.upper()} not implemented')

    async def method_get(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='GET')

    async def method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='POST')

    async def method_patch(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='PATCH')

    async def method_delete(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='DELETE')

