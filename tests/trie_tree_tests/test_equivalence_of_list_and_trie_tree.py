import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable

import random
import logging
import cProfile
import pstats

class TestEquivalenceOfListAndTrietree(unittest.TestCase):
    def setUp(self):
        self.tree0 = policyTrieTree.PolicyTrieTree()
        self.tree1 = policyTrieTree.PolicyTrieTree()
        self.tree2 = policyTrieTree.PolicyTrieTree()
        treeList = [self.tree0, self.tree1, self.tree2]

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
        level=logging.INFO,
        filename='logs.txt')

    def test_samePacketsInBoth(self):
        rule0 = ("5", "5", "12", "alpha")
        rule1 = ("*","*","*","beta")
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
            
        self.listFirewall.insertRule(rule0)
        self.listFirewall.insertRule(rule1)
        
        #1ST TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("1","1","1"))

        logging.debug("codeword!: " + str(codeword))

        self.policyBuilder.writeCodewords()
        self.assertEqual(self.listFirewall.lookup(("1","1","1")), self.hashTable.lookup(codeword)[0][3])

        #2ND TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("1","7","11"))
        self.assertEqual(self.listFirewall.lookup(("1","7","11")), self.hashTable.lookup(codeword)[0][3])
        logging.debug("codeword!: " + str(codeword))
        
        #3RD TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("255","255","255"))
        logging.debug("codeword!: " + str(codeword))

        self.assertEqual(self.listFirewall.lookup(("255","255","255")), self.hashTable.lookup(codeword)[0][3])
        
    def test_randomPackets_with_ranges(self): # Test 500 random packages vs firewall list
        import cProfile
        pr = cProfile.Profile()
        pr.enable()

        ruleList = []
        random.seed(311415)
        for k in range(0,10):
         
            rule = ["","","",""]
            for i in range(0,3):
                chance = random.randint(0,50) #CHANCE
                if chance <= 6:
                    rule[i] = str(random.randint(0,2**16))
                elif chance > 6 and chance <= 10:
                    rule[i] = "*"
                elif chance > 10:
                    rule[i] = format(random.randint(0,2**16),'b') + "*"
                    #rule[i] = bin(random.randint(0,1000))[2:].zfill(10) + "*"
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
        file = open("rule_list_for_random_test.txt", "w")
        
        for rule in ruleList:
            #if rule[:2] == ['*', '*', '*']:
             #   logging.debug("Throwing out ***" + str(rule))
              #  continue
            logging.debug("New inserted packet: " + str(rule))
            file.write(str(rule)+"\n")
            self.policyBuilder.insertRule(rule)
            self.listFirewall.insertRule(rule)
        file.close()

        self.listFirewall.insertRule(('*', '*', '*', 'delta'))
        self.hashTable.defualtRule = ['*', '*', '*', 'delta']

        
        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
        
        #self.tree0.drawGraph(html = True)
        packetList = []
        self.policyBuilder.writeCodewords()

        for i in range(0,500):
            packet = (str(random.randint(0,2**16)),str(random.randint(0,2**16)),str(random.randint(0,2**16)))
            
            logging.debug("")
            logging.debug("NEW PACKET:       packetnum: " + str(i))
            
            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                logging.debug("codeword is none" + str(self.hashTable.defualtRule))
                self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.defualtRule[3])
                logging.debug("(codeword) " + str(codeword))
                logging.debug("looking up packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
                logging.debug("looking up hash op: "+str(self.hashTable.lookup(codeword)))
                packetList.append(packet)
                logging.debug("packetnumber: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))
                continue
                
            logging.debug("(codeword) " + str(codeword))
            logging.debug("looking up packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("looking up hash op: "+str(self.hashTable.lookup(codeword)))
            packetList.append(packet)
            logging.debug("packetnumber: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))
            
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])
        
        pr.disable()
        pr.print_stats(sort='time')



    def test_randomPackets(self): # Test 500 random packages vs firewall list
        ruleList = []
        random.seed(311415)
        for _ in range(0,100):
            rule = ["","","",""]
            for i in range(0,3):
                chance = random.randint(0,100)
                if chance <= 50:
                    rule[i] = str(random.randint(0,5))
                elif chance > 50 and chance <= 55:
                    rule[i] = "*"
                elif chance > 55:
                    rule[i] = str(random.randint(0,5))
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

        file = open("rule_list_for_random_test.txt", "w")
        for rule in ruleList:
            if all(x == '*' for x in rule[:-1]):
                logging.debug("Throwing out ***" + str(rule))
                continue
            logging.debug("New inserted packet: " + str(rule))
            file.write(str(rule)+"\n")
            self.policyBuilder.insertRule(rule)
            self.listFirewall.insertRule(rule)
        file.close()
        self.policyBuilder.insertRule(('*', '*', '*', 'delta'))
        self.listFirewall.insertRule(('*', '*', '*', 'delta'))
        
        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        file.close()
        
        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
        
        packetList = []
        for i in range(0,10):
            packet = (str(random.randint(0,5)),str(random.randint(0,5)),str(random.randint(0,5)))
            
            logging.debug("")
            logging.debug("NEW PACKET:       packetnum: " + str(i))
            
            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][3]            
            logging.debug("(codeword) " + str(codeword))
                
            logging.debug("looking up packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("looking up hash op: "+str(self.hashTable.lookup(codeword)))

            self.policyBuilder.writeCodewords()

            packetList.append(packet)
            logging.debug("packetnumber: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))
            
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3])

    def test_performance(self):
        ruleList = []
        random.seed(311415)
        for k in range(0,80):
            
            rule = ["","","",""]
            for i in range(0,3):
                chance = random.randint(0,100)
                if chance <= 2:
                    rule[i] = str(random.randint(0,2**16))
                elif chance > 2 and chance <= 4:
                    rule[i] = "*"
                elif chance > 4:
                    rule[i] = format(random.randint(0,2**16),'b') + "*"
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
            if rule[:3] == ['*', '*', '*']:
                logging.debug("Throwing out ***" + str(rule))
                continue
            logging.debug("New inserted packet: " + str(rule))
            # file.write(str(rule)+"\n")
            self.policyBuilder.insertRule(rule)
            
        # file.close()
        self.policyBuilder.insertRule(('*', '*', '*', 'delta'))
        
        # file = open("list_firewall.txt", "w")
        # file.write(self.listFirewall.getRules())
        # file.close()
        
        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))
        
        #self.tree0.drawGraph(html = True)
        packetList = []
        for i in range(0,100):
            packet = (str(random.randint(0,25)), str(random.randint(0,25)), str(random.randint(0,25)))
            
            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][3]            

            self.policyBuilder.writeCodewords()

            packetList.append(packet)
            self.policyBuilder.retriveCodeword(packet)
            

