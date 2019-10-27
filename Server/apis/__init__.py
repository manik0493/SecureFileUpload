from flask_restplus import Api

from .public_key_exchange_api import api as pke

api = Api(
    title='FileUpload Server',
    version='1.0',
    description="Secure File upload protocol")

api.add_namespace(pke)
