import os
from hashlib import sha256
from random import choice, randint
from datetime import datetime
import json
from textwrap import indent

class CreateBlockChain():

    def __init__(self,fileName, newChain=True,difficultyLevel=2):
        self.fileName = fileName
        self.newChain = newChain
        self.difficultyLevel = difficultyLevel
        self.BlockChain = []
        self.HandleJson()
        self.AddBlock("GENESIS BLOCK","","") if self.BlockChain == [] else None

    def HandleJson(self):
        if not self.newChain:
            try:
                with open(self.fileName) as f:
                    self.BlockChain = json.load(f)
            except Exception as e:
                print(f"Error: {e}")

    #generate block
    def CreateBlock(self,sname,rollno,marks):
        block = {}
        block["student name"] = sname
        block["student rollno"]=rollno
        block["student marks"] = marks
        block["index"]= str(len(self.BlockChain))
        block["timeStamp"] = str(datetime.utcnow())
        block["previousHash"] = self.BlockChain[0]["currentHash"] if self.BlockChain != [] else "x"
        block["currentHash"], block["nounce"] = self.miner(
            block["student name"]+block["student rollno"]+block["student marks"]+block["index"]+block["timeStamp"]+block["previousHash"]
        )

        return block

    def miner(self,dataString):

        while True:
            nounce = str(randint(0,1E10))
            hash = sha256(str(dataString+nounce).encode()).hexdigest()
            if hash[:self.difficultyLevel]=="0"*self.difficultyLevel:
                return hash,nounce

    #add new block to BlockChain
    def AddBlock(self,sname,rollno,marks):
        self.BlockChain = [self.CreateBlock(sname,rollno,marks)]+self.BlockChain 

        with open(self.fileName,"w") as f:    #opens output blockchain file
            json.dump(self.BlockChain,f,indent=4)
        



BlockChainFileName = "S_output_Data_BlockChain.json"   #output file containing blockchain
Transaction = CreateBlockChain(BlockChainFileName,newChain=False,difficultyLevel=2)

while True:
     sname= input("Enter student name : ")
     rollno= input("Enter student rollno : ")
     marks=input("Enter marks: ")
     Transaction.AddBlock(sname,rollno,marks)
     os.system(BlockChainFileName)
    


#close the output json file after giving input for adding of each block to avoid invalid data in json file