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
        
        codeword = self.policyFactory.getCodewordPolicyFactory(["1","1","1"])
        
        self.policyFactory.writeCodewords()
        self.assertEqual(self.listFirewall.lookup(["1","1","1"]), self.hashTable.lookup(codeword)[3])
        
        codeword = self.policyFactory.getCodewordPolicyFactory(["1","7","11"])
        self.assertEqual(self.listFirewall.lookup(["1","7","11"]), self.hashTable.lookup(codeword)[3])
        
        
        codeword = self.policyFactory.getCodewordPolicyFactory(["255","255","255"])
        self.assertEqual(self.listFirewall.lookup(["255","255","255"]), self.hashTable.lookup(codeword)[3])
        
        
    def test_randomPackets(self): # TEST BRANCH CREATION... Now?adwawd
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
            logging.info("NEW PACKET: ")
            #time.sleep(0.0001)
            
            #codeword = self.policyFactory.getCodewordPolicyFactory(packet)
            #codeword = self.policyFactory.getCodewordtest(packet)
            codeword = ""
            #words = self.policyFactory.getCodewordtest(packet)
            words = self.policyFactory.getCodewordtest2(packet)
            #words = self.policyFactory.getCodewordtest3(packet)

            for correctword in words:
                if self.listFirewall.lookup(packet) == self.hashTable.lookup(correctword)[3]:
                    codeword = correctword
            
            logging.debug("(codeword) " + codeword)

        #Insert debug statements here for testing
            """ logging.debug("packetnum: " + str(i) + " firewalll: "+str(packet) + str(self.listFirewall.lookup(packet)))
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
            file.write(prettyPacketList) """
                
            logging.info("packetnum: "+str(i))
            logging.debug(" Slår packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("Slår hashen op: "+str(self.hashTable.lookup(codeword)))



            self.policyFactory.writeCodewords()

            packetList.append(packet)

            
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])
            #time.sleep(0.5)
    




            ### DEBUG TESTS ABOVE ###

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
                
            logging.info("packetnum: "+str(i))
            logging.debug(" Slår packet op: "+str(packet) + str(self.listFirewall.lookup(packet)))
            logging.debug("Slår hashen op: "+str(self.hashTable.lookup(codeword)))



            self.policyFactory.writeCodewords()

            packetList.append(packet)
















        
    def test_sample_of_errorcase0(self):
        ruleList = [['0-4', '1-4', '*', 'beta'],
                   ['16', '4', '2-3', 'alpha'],
                   ['18', '2', '1-4', 'alpha'],
                   ['*', '*', '2-3', 'beta'],
                   ['0-4', '2-3', '*', 'alpha'],
                   ['13', '16', '*', 'beta'],
                   ['*', '16', '2-3', 'beta'],
                   ['*', '1-3', '5', 'beta'],
                   ['5', '*', '1-4', 'beta'],
                   ['1-4', '17', '1-4', 'alpha']]
        for rule in ruleList:
            self.policyFactory.insertRange(rule)
            self.listFirewall.insertRange(rule)
        self.policyFactory.insertRange(["*","*","*","delta"])
        self.listFirewall.insertRange(["*","*","*","delta"])
        
        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
            
        random.seed(311415)
        packetList = []
        for i in range(0,1000):
            packet = ["","",""]
            for j in range(0,3):
                packet[j] = str(random.randint(0,20))
            
            codeword = self.policyFactory.getCodewordPolicyFactory(packet)

            self.policyFactory.writeCodewords()
            
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
                logging.debug("packetnum: "+str(i)+" packet: "+str(packet))
                logging.debug("hashTableValue: "+str(self.hashTable.lookup(codeword)))
                self.policyFactory.writeCodewords()
                file = open("list_firewall.txt", "w")
                file.write(self.listFirewall.getRules())
                logging.debug("Tree0's codeword "+str(self.tree0.getCodeword(packet[0])))
                logging.debug("Tree1's codeword "+str(self.tree1.getCodeword(packet[1])))
                logging.debug("Tree2's codeword "+str(self.tree2.getCodeword(packet[2])))
                
                
                codeword = self.policyFactory.getCodewordPolicyFactory(packet)
                
                
                logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
                
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


            
            
            packetList.append(packet)
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])
        # packet = ["1","2","4"]
        # codeword = self.policyFactory.getCodewordPolicyFactory(packet)
        # self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])