import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import logging
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall


class TestErrorCase(unittest.TestCase):
    def setUp(self):
        file = open("logs.txt", "w")
        file.flush()
        file.close()
        
        logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')
    
    def test_wildcard_and_ranges(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()

        ruleList = [["*","*","3","alpha"],    
                   ["0","2","*","beta"],
                   ["*","2","3","delta"],    
                   ["*","*","*","gamma"]
                   ]
        self.initListAndTreeFirewalls(ruleList)
        packet = ["8","2","3"]

        codeword = self.policyFactory.retriveCodeword(packet)
        
        logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
        if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
            self.logDifference(packet, codeword)

        logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))

        self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])


    def test_permutations(self):
            self.init3Trees()
            self.listFirewall = listFirewall.ListFirewall()

            ruleList = [
                       ['*', '5', '2', 'beta'],
                        ['3', '*', '*', 'alpha'],
                        ['0', '3', '4', 'alpha'],
                        ['*', '*', '0', 'beta'],

                       ]
            self.initListAndTreeFirewalls(ruleList)
            packet = ["5","3","0"]

            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)

            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))

            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])

        

    def test_superset(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
        ['*', '5', '2', 'beta'], 
        ['*', '*', '2', 'alpha'], 
        ['*', '3', '0', 'beta'], 
        #['*', '*', '*', 'hotel'],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [#['0', '3', '4'],                         
        ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("last codeword test: " + str(codeword))
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])
    
    def test_new_rule_is_subset(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()        
        ruleList = [
        #['0', '5', '3', 'beta'],
        #['1', '*', '0', 'alpha'],
        #['*', '*', '1', 'alpha'],
        #['*', '0', '*', 'beta'],
        #['*', '0', '3', 'beta'],
        #['*', '5', '2', 'beta'],
        ['3', '*', '*', 'alpha'],
        ['0', '3', '4', 'alpha'],
        ['3', '5', '5', 'beta']
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [#['2', '4', '4'], 
        ['3', '5', '5']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("last codeword test: " + str(codeword))
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])


    def test_errorcase(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
        ['1', '*', '0', 'alpha'],
        ['*', '*', '2', 'alpha'],
        ['*', '*', '*', 'hotel'],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [#['0', '3', '4'],  
        ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])


    def test_errorcase_next(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
        ['*', '5', '2', 'beta'],
        ['3', '*', '*', 'alpha'],
        ['0', '3', '4', 'alpha'],
        
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [['0', '3', '4']]#,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])


    def test_errorcase_next2(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
        ['0', '5', '3', 'beta'],
        ['1', '*', '0', 'alpha'],
        ['*', '*', '1', 'alpha'],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [['2', '5', '1']]#,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])


    def test_very_basic(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
        ['*', '0', '*', 'beta'],
        ['*', '*', '4', 'alpha'],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [['2', '0', '4']]#,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])



    def test_perm_exists_of_newrule(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
                ['1', '*', '0', 'alpha'],
                ['*', '0', '3', 'beta'],
                ['*', '*', '0', 'beta'],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [['5', '1', '0']]#,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])


    def test_tryRemoveLast_rule(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ['*', '5', '2', 'beta'],
            ['*', '*', '2', 'alpha'],
            ['2', '*', '*', 'alpha']
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [['2', '1', '2']]#,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])


    def test_subRanges(self):
        self.init3Trees(treeDepth = 4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ['10*', '1', '1', 'alpha'],
            ['1*', '1', '1', 'beta'],
            ['*', '*', '*', 'gamma']
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [['8', '1', '1'], ['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])
    

    def test_errorcaseTEMP(self):
        self.init3Trees(treeDepth = 4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ['0*', '*', '5', 'gamma'],
            ['3', '0', '101*', 'gamma'],
            ['*', '*', '*', 'charlie'],

        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [['3', '4', '5']]#,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)
    
            logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])



    def logDifference(self, packet, codeword):
        logging.debug("hashtable lookup"+str(self.hashTable.lookup(["8","2","3"])))
        logging.debug(self.policyFactory.getRuleTuple())
        logging.debug("codeword: "+str(codeword)+" for packet "+str(packet))
        logging.debug("packet: "+str(packet))
        logging.debug("hashTableValue: "+str(self.hashTable.lookup(codeword)))
        self.policyFactory.writeCodewords()
        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        logging.debug("Tree0's codeword "+str(self.tree0.getCodeword(packet[0])))
        logging.debug("Tree1's codeword "+str(self.tree1.getCodeword(packet[1])))
        logging.debug("Tree2's codeword "+str(self.tree2.getCodeword(packet[2])))

    def initListAndTreeFirewalls(self, ruleList):
        for rule in ruleList:
            logging.debug("New inserted rule: " + str(rule))
            self.policyFactory.insertRule(rule)
            self.listFirewall.insertRule(rule)    
            
        self.hashTable = CuckooHashTable.CuckooHashTable()
        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1],rule[0])

        self.policyFactory.writeCodewords()

    def init3Trees(self, treeDepth = 16):
       self.tree0 = policyTrieTree.PolicyTrieTree()
       self.tree0.treeDepth = treeDepth
       self.tree1 = policyTrieTree.PolicyTrieTree()
       self.tree1.treeDepth = treeDepth
       self.tree2 = policyTrieTree.PolicyTrieTree()
       self.tree2.treeDepth = treeDepth 

       treeList = [self.tree0,self.tree1,self.tree2]
       
       self.policyFactory = PolicyBuilder.PolicyBuilder(treeList)
       self.policyFactory.setSeed(311415)