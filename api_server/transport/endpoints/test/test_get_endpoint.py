from sanic.request import Request
from sanic.response import BaseHTTPResponse
from transport.endpoints.base import BaseEndpoint


class GetTestEndpoint(BaseEndpoint):
    async def method_get(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:
        response = {
            'test': 'OK'
        }
        return await self.make_response_json(body=response, status=200)
