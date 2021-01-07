from sanic import Sanic

from config.app_config import ApplicationConfig
from context import Context
from hooks import init_db
from transport.routes import get_routes


def configure_app(config: ApplicationConfig, context: Context):
    init_db(config.database, context)

    app = Sanic(__name__)

    for handler in get_routes(config.sanic, context):
        app.add_route(
            handler=handler,
            uri=handler.uri,
            methods=handler.methods,
            strict_slashes=True
        )

    return app
