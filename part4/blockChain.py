import hashlib
from datetime import datetime

class Transaction():
    def __init__(self,sender,receiver,amount):
        self.sender=sender
        self.receiver=receiver
        self.amount=amount
    
    def calculateHash(self):
        return(hashlib.sha256(self.sender+self.receiver+str(self.amount)))

    def signTransaction(self,signingKey):
        if signingKey.getPublic() != self.sender:
            raise Exception("You cannot sign transactions for other wallets")
        hash=self.calculateHash()
        self.signature=signingKey.sign(hash,'base64')
        


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
        self.difficulty=5 # The target that each block hash should follow, Higher the difficulty longer it will take to mine each block
        self.pending=[]
        self.reward=100

    # get the last block in the chain
    def getLatestBlock(self):
        return(self.chain[-1])

    def minePendingTransactions(self,rewardAddress):                              #Takes transactions from the pending list, mines 1 block, adds it to the chain and reward the miner
        block=Block(datetime.today().strftime('%d-%m-%Y-%H:%M:%S'),self.pending)
        block.prevHash=self.getLatestBlock().hash
        block.mineBlock(self.difficulty)
        print("Mined Block: ",block.hash)
        self.chain.append(block)
        self.pending=[Transaction('Reward',rewardAddress,self.reward)]
    
    def createTransaction(self,transaction):
        self.pending.append(transaction)
    
    def getBalance(self,address):    # The balance is not stored inside a wallet, rather the balance is calculated by going over the whole chain and look for additions and subtractions from user wallet
        balance=0
        for block in self.chain[1:]: #Exclude the genesis Block
            for trans in block.transactions:
                if trans.sender==address:
                    balance-=trans.amount
                elif trans.receiver==address:
                    balance+=trans.amount
        return balance


