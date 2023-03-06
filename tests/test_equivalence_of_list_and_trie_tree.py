import unittest
import Parallel_tree_algorithm.python.TrieTree.PolicyTrieTree as portnumbertrie
import Parallel_tree_algorithm.python.TrieTree.policyBuilder as policyBuilder
import Parallel_tree_algorithm.python.listFirewall.listFirewall as listFirewall
import Parallel_tree_algorithm.python.hashTable.cuckooHashTable as cuckooHashTable

import random
import logging


class TestEquivalenceOfListAndTrietree(unittest.TestCase):
    def setUp(self):
        self.tree0 = portnumbertrie.PortNumberTrieTree()
        self.tree1 = portnumbertrie.PortNumberTrieTree()
        self.tree2 = portnumbertrie.PortNumberTrieTree()
        treeList = [self.tree0,self.tree1,self.tree2]

        self.policyFactory = policyBuilder.PolicyBuilder(treeList)
        self.policyFactory.setSeed(311415)
        
        self.hashTable = cuckooHashTable.CuckooHashTable()
        
        self.listFirewall = listFirewall.ListFirewall()
        
        #deleting all the logs
        file = open("logs.txt", "w")
        file.flush()
        file.close()
        
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.INFO,
        filename='logs.txt')

    def test_samePacketsInBoth(self):
        rule0 = ["1-5", "6-10", "10-12", "alpha"] 
        rule1 = ["*","*","*","beta"]
        self.policyFactory.insertRange(rule0)
        self.policyFactory.insertRange(rule1)

        for rank, rule in enumerate(self.policyFactory.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
            
        self.listFirewall.insertRange(rule0)
        self.listFirewall.insert(rule1)
        
        #1ST TEST
        codeword = ""
        anwserList = self.policyFactory.retriveCodeword(["1","1","1"])
        bestAnswer = ""
        oldRank = 10000000000000000
        for answer in anwserList:
            thisAnswer = self.hashTable.lookup(answer)
            logging.debug("answer thisAnswer: " + str(thisAnswer))
            if thisAnswer[0] != self.hashTable.defualtRule:
                logging.debug("codeword!: " + str(thisAnswer))
                if int(thisAnswer[1]) < oldRank:
                    logging.debug("current best answer: " + str(thisAnswer))  
                    bestAnswer = answer
                    oldRank = thisAnswer[1]
        codeword = bestAnswer

        logging.debug("codeword!: " + str(codeword))

        self.policyFactory.writeCodewords()
        self.assertEqual(self.listFirewall.lookup(["1","1","1"]), self.hashTable.lookup(codeword)[0][3])

        #2ND TEST
        codeword = ""
        anwserList = self.policyFactory.retriveCodeword(["1","7","11"])
        bestAnswer = ""
        oldRank = 10000000000000000
        for answer in anwserList:
            thisAnswer = self.hashTable.lookup(answer)
            logging.debug("answer thisAnswer: " + str(thisAnswer))
            if thisAnswer[0] != self.hashTable.defualtRule:
                if thisAnswer[1] < oldRank:
                    logging.debug("current best answer: " + str(thisAnswer))  
                    bestAnswer = answer
                    oldRank = thisAnswer[1]
        codeword = bestAnswer
        self.assertEqual(self.listFirewall.lookup(["1","7","11"]), self.hashTable.lookup(codeword)[0][3])
        
        #3RD TEST
        codeword = ""
        anwserList = self.policyFactory.retriveCodeword(["255","255","255"])
        bestAnswer = ""
        oldRank = 10000000000000000
        for answer in anwserList:
            thisAnswer = self.hashTable.lookup(answer)
            logging.debug("answer thisAnswer: " + str(thisAnswer))
            if thisAnswer[0] != self.hashTable.defualtRule:
                if thisAnswer[1] < oldRank:
                    logging.debug("current best answer: " + str(thisAnswer))  
                    bestAnswer = answer
                    oldRank = thisAnswer[1]
        codeword = bestAnswer
        

        self.assertEqual(self.listFirewall.lookup(["255","255","255"]), self.hashTable.lookup(codeword)[0][3])
        
    def test_randomPackets(self): # Test 1000 random packages vs firewall list
        ruleList = []
        ruleList.append(['0', '*', '*', 'beta'])
        random.seed(311415)
        for _ in range(0,100):
            rule = ["","","",""]
            for i in range(0,3):
                chance = random.randint(0,100)
                if chance <= 50:
                    rule[i] = str(random.randint(0,255))
                elif chance > 50 and chance < 55:
                    if rule[0] == "*" and rule[1] == "*":
                        rule[i] = str(random.randint(0,255))
                    else:
                        rule[i] = "*"
                elif chance >= 55:
                    rule[i] = str(random.randint(1,2)) + "-" + str(random.randint(3,4))
            chance = random.randint(0,100)
            if chance <= 33:
                rule[3] = "alpha"
            elif chance > 33 and chance < 66:
                rule[3] = "beta"
            elif chance >= 66:
                rule[3] = "gamma"
            ruleList.append(rule)
        
        for rule in ruleList:
            self.policyFactory.insertRange(rule)
            self.listFirewall.insertRange(rule)
        self.policyFactory.insertRange(["*","*","*","delta"])
        self.listFirewall.insertRange(["*","*","*","delta"])
        
        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        file.close()
        
        for rank, rule in enumerate(self.policyFactory.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
        
        packetList = []
        for i in range(0,1000):
            packet = ["","",""]
            for j in range(0,3):
                packet[j] = str(random.randint(0,255))
            
            logging.info("")
            logging.info("NEW PACKET:       packetnum: " + str(i))
            
            codeword = ""
            anwserList = self.policyFactory.retriveCodeword(packet)
            bestAnswer = ""
            oldRank = 10000000000000000
            for answer in anwserList:
                thisAnswer = self.hashTable.lookup(answer)
                logging.debug("answer thisAnswer: " + str(thisAnswer))
                if thisAnswer[0] != self.hashTable.defualtRule:
                    if thisAnswer[1] < oldRank:
                        logging.debug("current best answer: " + str(thisAnswer))
                        bestAnswer = answer
                        oldRank = thisAnswer[1]
            codeword = bestAnswer
            logging.debug("answer table lookup: " + str(self.hashTable.lookup(bestAnswer)))
            
            logging.debug("(codeword) " + str(codeword))

        # Debug statements for testing
                
            logging.debug("lookingup packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("lookingup hashen op: "+str(self.hashTable.lookup(codeword)))

            self.policyFactory.writeCodewords()

            packetList.append(packet)
            logging.debug("packetnumber: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3])
    
