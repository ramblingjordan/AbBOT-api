import os
from flask import Flask
from flask_restful import Resource, Api
from text_model import create_anonymous_form_batch

HOST = os.environ.get('API_HOST', '0.0.0.0')
PORT = os.environ.get('API_PORT', 5000)

app = Flask(__name__)
api = Api(app)


class AnonymousFormBatchResource(Resource):
  def get(self):
    try:
      results = {'data': create_anonymous_form_batch(), 'msg': 'Successfully created anonymous form batch!', 'status': 200}
    except Exception:
      results = {'data': {}, 'msg': 'Failed to create anonymous form batch!', 'status': 500}
    return results


api.add_resource(AnonymousFormBatchResource, '/getFormBatch')

if __name__ == '__main__':
  app.run(debug=True, host=HOST, port=PORT)
