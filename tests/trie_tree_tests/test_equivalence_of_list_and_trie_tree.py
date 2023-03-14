import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable

import random
import logging


class TestEquivalenceOfListAndTrietree(unittest.TestCase):
    def setUp(self):
        self.tree0 = policyTrieTree.PolicyTrieTree()
        self.tree1 = policyTrieTree.PolicyTrieTree()
        self.tree2 = policyTrieTree.PolicyTrieTree()
        treeList = [self.tree0,self.tree1,self.tree2]

        self.policyFactory = PolicyBuilder.PolicyBuilder(treeList)
        self.policyFactory.setSeed(311415)
        
        self.hashTable = CuckooHashTable.CuckooHashTable()
        
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
        codeword = self.policyFactory.retriveCodeword(["1","1","1"])

        logging.debug("codeword!: " + str(codeword))

        self.policyFactory.writeCodewords()
        self.assertEqual(self.listFirewall.lookup(["1","1","1"]), self.hashTable.lookup(codeword)[0][3])

        #2ND TEST
        codeword = ""
        codeword = self.policyFactory.retriveCodeword(["1","7","11"])
        self.assertEqual(self.listFirewall.lookup(["1","7","11"]), self.hashTable.lookup(codeword)[0][3])
        logging.debug("codeword!: " + str(codeword))
        
        #3RD TEST
        codeword = ""
        codeword = self.policyFactory.retriveCodeword(["255","255","255"])
        logging.debug("codeword!: " + str(codeword))

        self.assertEqual(self.listFirewall.lookup(["255","255","255"]), self.hashTable.lookup(codeword)[0][3])
        
    def test_randomPackets(self): # Test 1000 random packages vs firewall list
        ruleList = []
        random.seed(311415)
        for _ in range(0,100):
            rule = ["","","",""]
            for i in range(0,3):
                chance = random.randint(0,100)
                if chance <= 33:
                    rule[i] = str(random.randint(0,20))
                elif chance > 33 and chance < 66:
                    if rule[0] == "*" and rule[1] == "*":
                        rule[i] = str(random.randint(0,20))
                    else:
                        rule[i] = "*"
                elif chance >= 66:
                    rule[i] = str(random.randint(1,2)) + "-" + str(random.randint(3,4))
            chance = random.randint(0,100)
            if chance < 25:
                rule[3] = "alpha"
            elif chance >= 25 and chance <= 50:
                rule[3] = "beta"
            elif chance > 50 and chance < 75:
                rule[3] = "gamma"
            elif chance >= 75:
                rule[3] = "hotel"
            ruleList.append(rule)
        
        for rule in ruleList:
            logging.debug("regel: " +  str(rule))
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
                packet[j] = str(random.randint(0,20))
            
            logging.info("")
            logging.info("NEW PACKET:       packetnum: " + str(i))
            
            codeword = self.policyFactory.retriveCodeword(packet)            
            logging.debug("(codeword) " + str(codeword))
                
            logging.debug("lookingup packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("lookingup hashen op: "+str(self.hashTable.lookup(codeword)))

            self.policyFactory.writeCodewords()
            self.policyFactory.writePrettyString()

            packetList.append(packet)
            logging.debug("packetnumber: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))

            
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3])
