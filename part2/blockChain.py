import hashlib

# Class for blocks containing transaction data
class Block():
    def __init__(self,index,time,data,prevHash=''):
            self.index=index
            self.time=time
            self.data=data
            self.prevHash=prevHash
            self.nonce=0
            self.hash=self.calculateHash()
    #Calculate hash of a block
    def calculateHash(self):
        return(hashlib.sha256((self.index+self.time+str(self.data)+self.prevHash+str(self.nonce)).encode()).hexdigest())
    
    def mineBlock(self,difficulty):
        while (self.hash[0:difficulty]!='0'*difficulty):
            self.nonce+=1
            self.hash=self.calculateHash()
        print("Mined block : "+self.hash)



# class for chain of blocks
class BlockChain():
    def __init__(self):
        # Genesis block is the first block of every block chain and can contain random data
        first=Block('0','9/11/2021','Genesis Block','0001')
        self.chain=[first]
        self.difficulty=3

    # get the last block in the chain
    def getLatestBlock(self):
        return(self.chain[-1])

    def addBlock(self,newBlock):
        newBlock.prevHash=self.getLatestBlock().hash
        #newBlock.hash=newBlock.calculateHash()
        newBlock.mineBlock(self.difficulty)
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
print('Mining Block 1...\n')
obj.addBlock(Block('1',"9/11/2021",{'amount':4})) # add block of data to chain
print('Mining Block 2...\n')
obj.addBlock(Block('2',"9/12/2021",{'amount':12}))
print('Mining Block 3...\n')
obj.addBlock(Block('3',"10/1/2022",{'amount':15}))

[print(str({'index':x.index,'time':x.time,'data':x.data,'previous hash':x.prevHash,'hash':x.hash})+"\n") for x in obj.chain] # print the blockchain nicely
print("Is the chain valid? "+str(obj.validate())) #check for irregularity

obj.chain[1].data={'amount':100} # manipulate block data and calculate and update hashes of all consequent blocks to bypass irregularity check
for i in range(1,len(obj.chain)):       # commenting this for loop block will show that the chain is not valid 
    obj.chain[i].mineBlock(obj.difficulty) # We will need to mine all the subsequent blocks again if we want to modify something in a block
    newHash=obj.chain[i].hash
    try:
        obj.chain[i+1].prevHash=newHash
    except:
        pass

[print(str({'index':x.index,'time':x.time,'data':x.data,'previous hash':x.prevHash,'hash':x.hash})+"\n") for x in obj.chain] # print the blockchain nicely


print("Is the chain valid? "+str(obj.validate())) #check for irregularity