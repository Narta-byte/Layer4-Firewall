import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as portnumbertrie
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import logging
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall


class TestErrorCase(unittest.TestCase):
    def setUp(self):
        file = open("logs.txt", "w")
        file.flush()
        file.close()
        
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
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

        codeword = ""
        words = self.policyFactory.retriveCodeword(packet)
        for correctword in words:
            if self.listFirewall.lookup(packet) == self.hashTable.lookup(correctword)[3]:
                codeword = correctword
    
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
            self.policyFactory.insertRange(rule)
            self.listFirewall.insertRange(rule)    
            
        self.hashTable = CuckooHashTable.CuckooHashTable()
        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1],rule[0])

        self.policyFactory.writeCodewords()

    def init3Trees(self):
       self.tree0 = portnumbertrie.PolicyTrieTree()
       self.tree1 = portnumbertrie.PolicyTrieTree()
       self.tree2 = portnumbertrie.PolicyTrieTree()
       treeList = [self.tree0,self.tree1,self.tree2]
       
       self.policyFactory = PolicyBuilder.PolicyBuilder(treeList)
       self.policyFactory.setSeed(311415)