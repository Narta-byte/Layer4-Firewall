import unittest
import trie_tree_parser.python.TrieTree.portNumberTrieTree as portnumbertrie
import trie_tree_parser.python.TrieTree.policyFactory as policyFactory
import trie_tree_parser.python.listFirewall.listFirewall as listFirewall
import trie_tree_parser.python.hashTable.cuckooHashTable as cuckooHashTable

import random
import logging


class TestEquivalenceOfListAndTrietree(unittest.TestCase):
    def setUp(self):
        self.tree0 = portnumbertrie.PortNumberTrieTree()
        self.tree1 = portnumbertrie.PortNumberTrieTree()
        self.tree2 = portnumbertrie.PortNumberTrieTree()
        treeList = [self.tree0,self.tree1,self.tree2]

        self.policyFactory = policyFactory.PolicyFactory(treeList)
        self.policyFactory.setSeed(311415)
        
        self.hashTable = cuckooHashTable.CuckooHashTable()
        
        self.listFirewall = listFirewall.ListFirewall()
        
        #deleting all the logs
        file = open("logs.txt", "w")
        file.flush()
        file.close()
        
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')

    def test_samePacketsInBoth(self):
        rule0 = ["1-5", "6-10", "10-12", "alpha"] 
        rule1 = ["*","*","*","beta"]
        self.policyFactory.insertRange(rule0)
        self.policyFactory.insertRange(rule1)

        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
            
        self.listFirewall.insertRange(rule0)
        self.listFirewall.insert(rule1)
        
        codeword = ""

        ### 1ST TEST:
        word = self.policyFactory.retriveCodeword(["1","1","1"])
        for correctword in word:
            if self.listFirewall.lookup(["1","1","1"]) == self.hashTable.lookup(correctword)[3]:
                codeword = correctword
        self.policyFactory.writeCodewords()
        self.assertEqual(self.listFirewall.lookup(["1","1","1"]), self.hashTable.lookup(codeword)[3])

        ### 2ND TEST:
        word = self.policyFactory.retriveCodeword(["1","7","11"])
        for correctword in word:
            if self.listFirewall.lookup(["1","7","11"]) == self.hashTable.lookup(correctword)[3]:
                codeword = correctword
        self.assertEqual(self.listFirewall.lookup(["1","7","11"]), self.hashTable.lookup(codeword)[3])
        
        ### 3RD TEST:
        word = self.policyFactory.retriveCodeword(["255","255","255"])
        for correctword in word:
            if self.listFirewall.lookup(["255","255","255"]) == self.hashTable.lookup(correctword)[3]:
                codeword = correctword
        self.assertEqual(self.listFirewall.lookup(["255","255","255"]), self.hashTable.lookup(codeword)[3])
        
        
    def test_randomPackets(self): # Test 1000 random packages vs firewall list
        words = []
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
                    rule[i] = str(random.randint(0,2)) + "-" + str(random.randint(3,4))
            
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
        
        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        
        packetList = []
        for i in range(0,1000):
            packet = ["","",""]
            for j in range(0,3):
                packet[j] = str(random.randint(0,20))
            
            logging.info("")
            logging.info("NEW PACKET:       packetnum: " + str(i))
            
            codeword = ""
            codeword = self.policyFactory.retriveCodeword(packet)
            #logging.debug("(codeword List): " + str(words))

            """ for correctword in words:
                if self.listFirewall.lookup(packet) == self.hashTable.lookup(correctword)[3]:
                    codeword = correctword"""
            
            logging.debug("(codeword) " + str(codeword))

        #Insert debug statements here for testing
                
            logging.debug(" Slår packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("Slår hashen op: "+str(self.hashTable.lookup(codeword)))

            self.policyFactory.writeCodewords()

            packetList.append(packet)
            
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])
    


            ### DEBUG TESTS ABOVE ###

""" 
            logging.debug("packetnum: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("Lookupfirewall: " + str(self.listFirewall.lookup(packet)))
            logging.debug("Lookup hash    : " + str(self.hashTable.lookup(codeword)))
            logging.debug("(codeword) " + codeword)
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                logging.debug("fej....")
                logging.debug("codeword: "+str(codeword))
                logging.debug("packetnum: "+str(i)+" packet: "+str(packet) + str(self.listFirewall.lookup(packet)))
                logging.debug("hashTableValue0: "+str(self.hashTable.lookup(codeword)))
                logging.debug(" Slår packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
                logging.debug("Slår hashen op: "+str(self.hashTable.lookup(codeword)))
                self.policyFactory.writeCodewords()
                
            file = open("list_firewall.txt", "w")
            file.write(self.listFirewall.getRules())
            
            file = open("rule_list_for_random_test.txt", "w")
            prettyRuleList = ""
            for rule in ruleList:
                prettyRuleList += str(rule) + "\n"

            file.write(prettyRuleList)
            file = open("packet_list_for_random_test.txt", "w")
            prettyPacketList = ""
                

            for packet in packetList:
                prettyPacketList += str(packet) + "\n"
            file.write(prettyPacketList)
 """