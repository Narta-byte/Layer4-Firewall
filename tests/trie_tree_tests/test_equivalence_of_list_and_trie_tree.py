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

        self.policyBuilder = PolicyBuilder.PolicyBuilder(treeList)
        self.policyBuilder.setSeed(311415)
        
        self.hashTable = CuckooHashTable.CuckooHashTable()
        
        self.listFirewall = listFirewall.ListFirewall()
        
        #deleting all the logs
        file = open("logs.txt", "w")
        file.flush()
        file.close()
        
        logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')

    def test_samePacketsInBoth(self):
        rule0 = ["1-5", "6-5", "5-12", "alpha"] 
        rule1 = ["*","*","*","beta"]
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
            
        self.listFirewall.insertRange(rule0)
        self.listFirewall.insert(rule1)
        
        #1ST TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(["1","1","1"])

        logging.debug("codeword!: " + str(codeword))

        self.policyBuilder.writeCodewords()
        self.assertEqual(self.listFirewall.lookup(["1","1","1"]), self.hashTable.lookup(codeword)[0][3])

        #2ND TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(["1","7","11"])
        self.assertEqual(self.listFirewall.lookup(["1","7","11"]), self.hashTable.lookup(codeword)[0][3])
        logging.debug("codeword!: " + str(codeword))
        
        #3RD TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(["255","255","255"])
        logging.debug("codeword!: " + str(codeword))

        self.assertEqual(self.listFirewall.lookup(["255","255","255"]), self.hashTable.lookup(codeword)[0][3])
        
    def test_randomPackets(self): # Test 500 random packages vs firewall list
        ruleList = []
        random.seed(311415)
        for _ in range(0,2000):
            rule = ["","","",""]
            for i in range(0,3):
                chance = random.randint(0,50)
                if chance <= 33:
                    rule[i] = str(random.randint(0,5))
                elif chance > 33 and chance <= 66:
                    rule[i] = "*"
                elif chance > 66:
                    rule[i] = str(random.randint(0,1)) + "-" + str(random.randint(9,5))
            chance = random.randint(0,50)
            if chance < 25:
                rule[3] = "alpha"
            elif chance >= 25 and chance <= 50:
                rule[3] = "beta"
            elif chance > 50 and chance < 75:
                rule[3] = "gamma"
            elif chance >= 75:
                rule[3] = "hotel"
            ruleList.append(rule)

        file = open("rule_list_for_random_test.txt", "w")
        for rule in ruleList:
            if rule[:3] == ['*', '*', '*']:
                logging.debug("Throwing out ***" + str(rule))
                continue
            logging.debug("New inserted packet: " + str(rule))
            file.write(str(rule)+"\n")
            self.policyBuilder.insertRule(rule)
            self.listFirewall.insertRange(rule)
        file.close()
        self.policyBuilder.insertRule(['*', '*', '*', 'delta'])
        self.listFirewall.insertRange(['*', '*', '*', 'delta'])
        """         self.policyBuilder.insertRule(["0-5","0-5","0-5","delta"])
        self.hashTable.defualtRule = ["0-5","0-5","0-5","delta"]
        self.listFirewall.insertRange(["0-5","0-5","0-5","delta"])
        """        
        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        file.close()
        
        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
        
        packetList = []
        for i in range(0,10000):
            packet = ["","",""]
            for j in range(0,3):
                packet[j] = str(random.randint(0,5))
            
            logging.debug("")
            logging.debug("NEW PACKET:       packetnum: " + str(i))
            
            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][3]            
            logging.debug("(codeword) " + str(codeword))
                
            logging.debug("lookingup packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("lookingup hashen op: "+str(self.hashTable.lookup(codeword)))

            self.policyBuilder.writeCodewords()

            packetList.append(packet)
            logging.debug("packetnumber: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))
            
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3])


