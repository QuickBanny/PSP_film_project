from config.app_config import ApplicationConfig
from transport.configure_sanic import configure_app
from context import Context


def main():

    config = ApplicationConfig()
    context = Context()
    app = configure_app(config, context)

    app.run(
        host=config.sanic.host,
        port=config.sanic.port,
        workers=config.sanic.workers,
        debug=config.sanic.debug
    )


if __name__ == '__main__':
    main()