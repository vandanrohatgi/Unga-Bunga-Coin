import hashlib
from datetime import datetime
from time import sleep

class Transaction():
    def __init__(self,sender,receiver,amount):
        self.sender=sender
        self.receiver=receiver
        self.amount=amount


# Class for blocks containing transaction data
class Block():
    def __init__(self,time,transactions,prevHash=''):
            self.time=time
            self.transactions=transactions
            self.prevHash=prevHash
            self.nonce=0
            self.hash=self.calculateHash()

    #Calculate hash of a block
    def calculateHash(self):
        return(hashlib.sha256((str(self.time)+str(self.transactions)+self.prevHash+str(self.nonce)).encode()).hexdigest())
    
    def mineBlock(self,difficulty):
        while (self.hash[0:difficulty]!='0'*difficulty):  #brute force for a hash for the block that matches the given target, here target is five 0's at the start of hash
            self.nonce+=1
            self.hash=self.calculateHash()
        print("Mined block  : "+self.hash)



# class for chain of blocks
class BlockChain():
    def __init__(self):
        # Genesis block is the first block of every block chain and can contain random data
        first=Block('9/11/2021','Genesis Block','0001')
        self.chain=[first]
        self.difficulty=2 # The target that each block hash should follow, Higher the difficulty longer it will take to mine each block
        self.pending=[]
        self.reward=100

    # get the last block in the chain
    def getLatestBlock(self):
        return(self.chain[-1])

    def minePendingTransactions(self,rewardAddress):
        block=Block(datetime.today().strftime('%d-%m-%Y-%H:%M:%S'),self.pending)
        block.prevHash=self.getLatestBlock().hash
        block.mineBlock(self.difficulty)
        print("Mined Block: ",block.hash)
        self.chain.append(block)
        self.pending=[Transaction('Reward',rewardAddress,self.reward)]
    
    def createTransaction(self,transaction):
        self.pending.append(transaction)
    
    def getBalance(self,address):
        balance=0
        for block in self.chain[1:]: #Exclude the genesis Block
            for trans in block.transactions:
                if trans.sender==address:
                    balance-=trans.amount
                elif trans.receiver==address:
                    balance+=trans.amount
        return balance


obj=BlockChain()
obj.createTransaction(Transaction('address1','address2',100))
obj.createTransaction(Transaction('address2','address1',50))

print("Mining...")
obj.minePendingTransactions('vandan')
sleep(3)
obj.minePendingTransactions('vandan') # we need this transaction again because, the process of us getting a reward is also a transaction and we need to mine it. So we call this transaction so that the above transaction is processed
print("\n UngaBunga Coins in Vandan's account:{} \n".format(obj.getBalance('vandan')))

[print(str({'time':x.time,'data':[{'sender':y.sender,'receiver':y.receiver,'amount ':y.amount} for y in x.transactions],'previous hash':x.prevHash,'hash':x.hash,'nonce':x.nonce})+"\n") for x in obj.chain[1:]] # Printing the whole blockchain is a bit messy now since one block contains multiple transactions