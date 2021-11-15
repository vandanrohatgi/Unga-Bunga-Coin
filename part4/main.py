from blockChain import BlockChain,Transaction

obj=BlockChain()
obj.createTransaction(Transaction('address1','address2',100))
obj.createTransaction(Transaction('address2','address1',50))

print("Mining...")
obj.minePendingTransactions('vandan')
obj.minePendingTransactions('vandan') # we need this transaction again because, the process of us getting a reward is also a transaction and we need to mine it. So we call this transaction so that the above transaction is processed
print("\n UngaBunga Coins in Vandan's account:{} \n".format(obj.getBalance('vandan')))
print("\n UngaBunga Coins in address1's account:{} \n".format(obj.getBalance('address1')))
print("\n UngaBunga Coins in address2's account:{} \n".format(obj.getBalance('address2')))

[print(str({'time':x.time,'data':[{'sender':y.sender,'receiver':y.receiver,'amount ':y.amount} for y in x.transactions],'previous hash':x.prevHash,'hash':x.hash,'nonce':x.nonce})+"\n") for x in obj.chain[1:]] # Printing the whole blockchain is a bit messy now since one block contains multiple transactions