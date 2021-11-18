import hashlib
from datetime import datetime

class Transaction():
    def __init__(self,sender,receiver,amount):
        self.sender=sender
        self.receiver=receiver
        self.amount=amount
    
    def calculateHash(self):
        return(hashlib.sha256((self.sender+self.receiver+str(self.amount)).encode()).hexdigest())

    def signTransaction(self,signingKey):
        self.signingKey=signingKey
        if signingKey.getPublic() != self.sender:
            raise Exception("You cannot sign transactions for other wallets")
        hash=self.calculateHash()
        self.signature=signingKey.sign(hash)

    def isValid(self):
        if self.sender=="Reward":   # since miners getting rewarded is also a transaction, we declare it as a valid transaction
            return True
        if not self.signature or len(self.signature)==0:
            raise Exception("No signature in this transaction!")
        
        return(self.signingKey.verify(self.signature,self.calculateHash()))
        


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
    
    def hasValidTransactions(self):                       # to verify all transactions in this block are valid
        for transaction in self.transactions:
            if self.transactions.isValid(transaction.signingKey) == False:
                return False
        
        return True



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
        #print("Mined Block: ",block.hash)
        self.chain.append(block)
        self.pending=[Transaction('Reward',rewardAddress,self.reward)]
    
    def addTransaction(self,transaction):
        if not transaction.sender or not transaction.receiver:
            raise Exception("Transaction must include sender and receiver address")
        #print(transaction.isValid(transaction.signingKey))
        if transaction.isValid()==False:
            raise Exception("Cannot add invalid transaction to the chain")
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
    
    def validate(self):
        for x in range(1,len(self.chain)):
            current=self.chain[x]
            prev=self.chain[x-1]
            if current.hasValidTransactions == False:
                return False
            if current.hash !=current.calculateHash():
                return False
            if current.prevHash!=prev.hash:
                return False
        return True



