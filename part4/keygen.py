from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
import binascii

class blockchain_cryptography():
    def __init__(self):
        self.private_key=ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.public_key=self.private_key.public_key()
    
    #def hash(self):

    def sign(self,hash,format):
        #pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
        #print(pem)
        #public_key=private_key.public_key()
        #pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
        #print(pem)
        return(binascii.hexlify(self.private_key.sign(hash,ec.ECDSA(hashes.SHA256()))))
    
    def getPublic(self):
        key=self.public_key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return(binascii.hexlify(key).decode())
