from ctypes import util
from email import utils
import codecs
import ecdsa
import subprocess
import os

from aries_cloudagent.wallet.util import b58_to_bytes, bytes_to_b58, random_seed

seed = os.urandom(ecdsa.SECP256k1.baselen)
print(seed)
secexp = ecdsa.util.randrange_from_seed__trytryagain(seed,ecdsa.SECP256k1.order)
print(secexp)
sk = ecdsa.SigningKey.from_secret_exponent(secexp, curve=ecdsa.SECP256k1)
#sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

#sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
#d in base 64 (43 bytes)
d = codecs.encode(codecs.decode(sk.to_string().hex(), 'hex'), 'base64').decode()[:43]

vk = sk.get_verifying_key()
# x and y coordinates in base 64 (43 bytes)
x = codecs.encode(codecs.decode(vk.to_string().hex()[:64], 'hex'), 'base64').decode()[:43]
y = codecs.encode(codecs.decode(vk.to_string().hex()[64:], 'hex'), 'base64').decode()[:43]


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

# call ION create.js
did = subprocess.check_output(["node", "create.js", x, y]).decode('utf-8')
print(did)


