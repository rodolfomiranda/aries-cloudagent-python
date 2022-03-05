from ctypes import util
from email import utils
import codecs
import ecdsa
import subprocess
import os
import base64
import json

from aries_cloudagent.wallet.util import b58_to_bytes, bytes_to_b58, random_seed

seed = os.urandom(ecdsa.SECP256k1.baselen)
secexp = ecdsa.util.randrange_from_seed__trytryagain(seed,ecdsa.SECP256k1.order)
sk = ecdsa.SigningKey.from_secret_exponent(secexp, curve=ecdsa.SECP256k1)

#d in base 64 (43 bytes)
d = codecs.encode(codecs.decode(sk.to_string().hex(), 'hex'), 'base64').decode()[:43]

vk = sk.get_verifying_key()
# x and y coordinates in base 64 (43 bytes)
x = codecs.encode(codecs.decode(vk.to_string().hex()[:64], 'hex'), 'base64').decode()[:43]
y = codecs.encode(codecs.decode(vk.to_string().hex()[64:], 'hex'), 'base64').decode()[:43]


####### TEST SSIGN VERIFY
# secret2  = sk.to_string().hex()
# sk2 = ecdsa.SigningKey.from_string(bytes.fromhex(secret2), curve=ecdsa.SECP256k1)
# sig = sk.sign(b"pepe")
# verkey2 = vk.to_string().hex()
# vk2 = ecdsa.VerifyingKey.from_string(bytes.fromhex(verkey2), curve=ecdsa.SECP256k1)
# print(vk.verify(sig, b"pepse"))



# key in a JWK format style
keyJWK = {
    "publicJwk": {
      "kty": 'EC',
      "crv": 'secp256k1',
      "x": codecs.encode(codecs.decode(vk.to_string().hex()[:64], 'hex'), 'base64').decode()[:43],
      "y": codecs.encode(codecs.decode(vk.to_string().hex()[64:], 'hex'), 'base64').decode()[:43]
    },
    "privateJwk": {
      "kty": 'EC',
      "crv": 'secp256k1',
      "d": codecs.encode(codecs.decode(sk.to_string().hex(), 'hex'), 'base64').decode()[:43],
      "x": codecs.encode(codecs.decode(vk.to_string().hex()[:64], 'hex'), 'base64').decode()[:43],
      "y": codecs.encode(codecs.decode(vk.to_string().hex()[64:], 'hex'), 'base64').decode()[:43]
    }
  }

# create a W3C DID Document
diddoc = {
    "services": [
      {
      "id": 'domain-1',
        "type": 'LinkedDomains',
        "serviceEndpoint": 'https://foo.example.com'
       }
     ]
}
diddocbase64 = base64.encodebytes(json.dumps(diddoc).encode())

# call ION create.js
did = subprocess.check_output(["node", "./aries_cloudagent/wallet/sidetree-cardano/create.js", x, y, diddocbase64]).decode('utf-8')
print(did)


