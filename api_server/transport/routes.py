from typing import Tuple

from transport.config import SanicConfig
from context import Context

from transport import endpoints

from config.app_config import ApplicationConfig


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return(
        endpoints.GetTestEndpoint(config, context, uri='/', methods=['GET']),
        endpoints.CreateUserEndpoint(config, context, uri='/user', methods=['POST'])
    )