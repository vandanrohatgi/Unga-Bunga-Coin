from blockChain import BlockChain,Transaction
from keygen import blockchain_cryptography

newKey=blockchain_cryptography()    
myWallet=newKey.getPublic()     #generate wallet address, which is also the public key


transx1=Transaction(myWallet,'someonesPublicKey',20)   # transfer 20 coins to someones wallet
transx1.signTransaction(newKey)

obj=BlockChain()

obj.addTransaction(transx1)

print("Mining...")
obj.minePendingTransactions(myWallet)
obj.minePendingTransactions(myWallet) # we need this transaction again because, the process of us getting a reward is also a transaction and we need to mine it. So we call this transaction so that the above transaction is processed

print("\n UngaBunga Coins in Vandan's account:{} \n".format(obj.getBalance(myWallet)))


[print(str({'time':x.time,'data':[{'sender':y.sender,'receiver':y.receiver,'amount ':y.amount} for y in x.transactions],'previous hash':x.prevHash,'hash':x.hash,'nonce':x.nonce})+"\n") for x in obj.chain[1:]] # Printing the whole blockchain is a bit messy now since one block contains multiple transactions