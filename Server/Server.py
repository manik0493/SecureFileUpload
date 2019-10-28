from flask import Flask
from apis import api
from core import Configs

from Crypto.PublicKey import RSA


pub_key =RSA.generate(1024)
f = open('mykey.pem','wb')
f.write(pub_key.publickey().export_key('PEM'))
f.close()
Configs.PUBLIC_KEY_FILE = 'mykey.pem'
Configs.PUBLIC_KEY_OBJECT = pub_key
Configs.CLIENT_SESSION_BOOK = {}

app = Flask(__name__)
api.init_app(app)

app.run(debug=True)


