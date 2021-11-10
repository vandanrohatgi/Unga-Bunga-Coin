import hashlib

# Class for blocks containing transaction data
class Block():
    def __init__(self,index,time,data,prevHash=''):
            self.index=index
            self.time=time
            self.data=data
            self.prevHash=prevHash
            self.hash=self.calculateHash()

    #Calculate hash of a block
    def calculateHash(self):
        return(hashlib.sha256((self.index+self.time+str(self.data)+self.prevHash).encode()).hexdigest())

# class for chain of blocks
class BlockChain():
    def __init__(self):
        # Genesis block is the first block of every block chain and can contain random data
        first=Block('0','9/11/2021','Genesis Block','0001')
        self.chain=[first]
    
    # get the last block in the chain
    def getLatestBlock(self):
        return(self.chain[-1])

    def addBlock(self,newBlock):
        newBlock.prevHash=self.getLatestBlock().hash
        newBlock.hash=newBlock.calculateHash()
        self.chain.append(newBlock)
    
    # checks to find irregularities in the blockchain
    def validate(self):
        for x in range(1,len(self.chain)):
            current=self.chain[x]
            prev=self.chain[x-1]
            if current.hash !=current.calculateHash():
                return False
            if current.prevHash!=prev.hash:
                return False
        return True

obj=BlockChain()
obj.addBlock(Block('1',"9/11/2022",{'amount':4})) # add block of data to chain
obj.addBlock(Block('2',"9/12/2022",{'amount':12}))

obj.chain[1].data={'amount':100} # manipulate block data and calculate and update hashes of all consequent blocks to bypass irregularity check
for i in range(1,len(obj.chain)):       # commenting this for loop block will show that the chain is not valid 
    newHash=obj.chain[i].calculateHash() # This mechanism only works because we have not implemented Proof-Of-Work yet
    obj.chain[i].hash=newHash
    try:
        obj.chain[i+1].prevHash=newHash
    except:
        pass

[print({'index':x.index,'time':x.time,'data':x.data,'previous hash':x.prevHash,'hash':x.hash}) for x in obj.chain] # print the blockchain nicely


print("Is the chain valid? "+str(obj.validate())) #check for irregularity