from os import path, environ, _exit as exit
from glob import glob
from flask import Flask
from flask_restful import Resource, Api
from typing import Callable, Mapping, NoReturn, Optional, Tuple, TypedDict
from flask_restful import HTTPException
from loguru import logger
from torch._C import Value
from werkzeug.wrappers.response import Response
from helpers.typing import JSONType

HOST: str = environ.get('API_HOST', '0.0.0.0')
PORT: int = int(environ.get('API_PORT', 5000))
ALLOWED_APIS = environ.get('ALLOWED_APIS', '*').split(',')


class UnexpectedAPIException(HTTPException):
  def __init__(self, message: str, response: Optional[Response] = None):
    super().__init__(message, response)
    self.code = 500


def create_generator_resource(name: str, api_function: Callable[[], JSONType]) -> Resource:
  class GeneratorResource(Resource):
    def get(self) -> Tuple[JSONType, int]:
      try:
        return (api_function(), 200)
      except Exception as error:
        raise UnexpectedAPIException(str(error))

  # Rename the class to the name of the API
  return type(name, (GeneratorResource, ), {})


class GeneratorAPIInfo(TypedDict):
  name: str
  api: Mapping[str, Callable[[], JSONType]]


def get_generator_api(name) -> GeneratorAPIInfo:
  module = __import__('api.generators.' + name)
  return {'name': name, 'api': module.generators.__getattribute__(name).api}


def start_server() -> NoReturn:
  app: Flask = Flask(__name__)
  api: Api = Api(app)

  @app.errorhandler(UnexpectedAPIException)
  def unexpected_api_exception(error: UnexpectedAPIException) -> Tuple[JSONType, int]:
    return ({'error': error.message}, error.code)

  @app.errorhandler(404)
  def not_found(error):
    return ({'message': f'The requested API path does not exist.'}, 404)

  # Import all of the APIs for each site from the generators directory
  api_added: bool = False
  for filepath in glob('api/generators/*.py'):
    name: str = path.basename(filepath)[:-3]
    if not '*' in ALLOWED_APIS and not name in ALLOWED_APIS:
      continue

    generator: GeneratorAPIInfo = get_generator_api(name)
    for generator_path, generator_function in generator['api'].items():
      api_path: str = f"/{generator['name']}{generator_path}"
      logger.debug(f'Setting up http://{HOST}:{PORT}{api_path}')

      api.add_resource(create_generator_resource(api_path, generator_function), api_path)
      api_added = True

  if not api_added:
    logger.debug('No APIs loaded. Exiting...')
    return

  app.run(host=HOST, port=PORT)
  exit(0)
