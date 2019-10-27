from flask_restplus import Namespace,Resource,fields,reqparse
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from core import Configs
import pickle
import json
from flask import send_file
import ast


api = Namespace('public_key_exchange_api',description = "api for exchanging public key")

@api.route('/pke')
class Pub_Key(Resource):
    def get(self):
        return send_file(Configs.PUBLIC_KEY_FILE)

@api.route('/message')
@api.doc(params={'msg': 'A message'})
class Msg(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('msg')
        args = parser.parse_args()
        decryptor = PKCS1_OAEP.new(Configs.PUBLIC_KEY_OBJECT)
        decrypted = decryptor.decrypt(ast.literal_eval(str(args.msg)))
        return decrypted








