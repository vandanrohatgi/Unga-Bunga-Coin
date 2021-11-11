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
        while (self.hash[0:difficulty]!='0'*difficulty):  #brute force for a hash for the block that matches the given target, here target is five 0's at the start of hash
            self.nonce+=1
            self.hash=self.calculateHash()
        print("Mined block  : "+self.hash)



# class for chain of blocks
class BlockChain():
    def __init__(self):
        # Genesis block is the first block of every block chain and can contain random data
        first=Block('0','9/11/2021','Genesis Block','0001')
        self.chain=[first]
        self.difficulty=5 # The target that each block hash should follow, Higher the difficulty longer it will take to mine each block

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
print('\n Mining Block 1...')
obj.addBlock(Block('1',"9/11/2021",{'amount':4})) # add block of data to chain
print('\nMining Block 2...\n')
obj.addBlock(Block('2',"9/12/2021",{'amount':12}))
print('\nMining Block 3...\n')
obj.addBlock(Block('3',"10/1/2022",{'amount':15}))

[print(str({'index':x.index,'time':x.time,'data':x.data,'previous hash':x.prevHash,'hash':x.hash,'nonce':x.nonce})+"\n") for x in obj.chain] # print the blockchain nicely
print("Is the chain valid? "+str(obj.validate())) #check for irregularity

obj.chain[1].data={'amount':100} # manipulate block data and calculate and update hashes of all consequent blocks to bypass irregularity check
for i in range(1,len(obj.chain)):       # commenting this for loop block will show that the chain is not valid 
    obj.chain[i].hash='randomValue'     # we do this because we need to reset the previous hash value so that it can be calculated again,(look at the condition in the mineBlock() function, it was not working because the previous hash already satisfied the target)
    obj.chain[i].mineBlock(obj.difficulty) # We will need to mine all the subsequent blocks again if we want to modify something in a block
    newHash=obj.chain[i].hash
    try:
        obj.chain[i+1].prevHash=newHash
    except:
        pass

[print(str({'index':x.index,'time':x.time,'data':x.data,'previous hash':x.prevHash,'hash':x.hash,'nonce':x.nonce})+"\n") for x in obj.chain] # print the blockchain nicely

print("Is the chain valid? "+str(obj.validate())) # After manipulating one block, it is significantly more harder to bypass the irregularity checks since it takes a long time to re-generate new hashes