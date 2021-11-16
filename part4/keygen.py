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
        self.signature=self.private_key.sign(hash.encode(),ec.ECDSA(hashes.SHA256()))
        return(binascii.hexlify(self.signature).decode())
    
    def getPublic(self):
        key=self.public_key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return(binascii.hexlify(key).decode())
    
    def verify(self,signature,data):
        if binascii.unhexlify(signature.encode())!=self.signature:
            return False
        try:
            self.public_key.verify(self.signature,data.encode(),ec.ECDSA(hashes.SHA256()))
        except:
            return(False)
        return True
