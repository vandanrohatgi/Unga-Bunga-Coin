from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
import binascii

class blockchain_cryptography():
    def __init__(self):
        self.private_key=ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.public_key=self.private_key.public_key()
    
    def getKey(self):
        return self.private_key

    def sign(self,hash):
        #pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
        #print(pem)
        #public_key=private_key.public_key()
        #pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
        #print(pem)
        self.signature=self.private_key.sign(hash.encode(),ec.ECDSA(hashes.SHA256()))
        return(self.signature)
    
    def getPublic(self):
        key=self.public_key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return(binascii.hexlify(key).decode())   # hexify the key so it is in readable format
    
    def verify(self,signature,hash):
        #print("signature: ",signature)
        #print("self.signature: ",self.signature)
        #print(signature!=self.signature)
        if signature!=self.signature:
            return False
        try:
            self.public_key.verify(self.signature,hash.encode(),ec.ECDSA(hashes.SHA256())) # throws error if the data is not signed correctly
        except:
            return(False)
        return True
        
