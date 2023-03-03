import unittest
import trie_tree_parser.python.TrieTree.portNumberTrieTree as portnumbertrie
import trie_tree_parser.python.TrieTree.policyFactory as policyFactory
import logging
import trie_tree_parser.python.hashTable.cuckooHashTable as cuckooHashTable

class TestPortNumberRange(unittest.TestCase):
    def setUp(self):
        self.tree = portnumbertrie.PortNumberTrieTree()
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')
        
    def test_3Trees_overlap(self):
        self.init3Trees()
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        self.policyFactory.insertRange(rule0)
        self.policyFactory.insertRange(rule1)
        self.policyFactory.writeCodewords()
        
        expectedOutput =open("tests/expectedOutput/test_3Trees_overlap.txt","r")
        self.assertEqual(self.policyFactory.getRuleTuple(),expectedOutput.read())
        
    def test_3Trees_overlap_with_default_rule(self):
        self.init3Trees()
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        defualtRule = ["*","*","*","delta"]
        self.policyFactory.insertRule(rule0)
        self.policyFactory.insertRule(rule1)
        self.policyFactory.insertRule(defualtRule)
        self.policyFactory.writeCodewords()
        
        self.policyFactory.getRuleTuple()

        expectedOutput =open("tests/expectedOutput/test_3Trees_overlap_with_default_rule.txt","r")
        self.assertEqual(self.policyFactory.getRuleTuple(),expectedOutput.read())
        
    def test_sameRule_twice(self):
        self.init3Trees()
        rule0 = ["1","1","*","alpha"]
        rule1 = ["1","1","*","beta"]
        self.policyFactory.insertRule(rule0)
        self.policyFactory.insertRule(rule1)
        self.policyFactory.writeCodewords()
        
        expectedOutput =open("tests/expectedOutput/test_sameRule_twice.txt","r")
        self.assertEqual(self.policyFactory.getRuleTuple(),expectedOutput.read())


        
    def test_simple_rule(self):
        self.init3Trees()
        rule0 = ["1","1","*","alpha"]
        rule1 = ["1","1","1","beta"]
        self.policyFactory.insertRule(rule0)
        self.policyFactory.insertRule(rule1)
        self.policyFactory.writeCodewords()
        
        #self.policyFactory.getRuleTuple()


        expectedOutput =open("tests/expectedOutput/test_simple_rule.txt","r")
        #logging.info(expectedOutput.read())
        self.assertEqual(self.policyFactory.getRuleTuple(),expectedOutput.read())
        
    def test_specific_ranges_with_second_field(self):
        self.init3Trees()
        rule0 = ["1","2-3","4-5","alpha"]
        rule1 = ["1","*","4-6","beta"]
        
        self.policyFactory.insertRange(rule0)
        self.policyFactory.insertRange(rule1)

        self.policyFactory.writeCodewords()
        
        self.tree0.drawGraph(html=True)
        self.tree1.drawGraph(html=True)
        self.tree2.drawGraph(html=True)
        expectedOutput = open("tests/expectedOutput/test_specific_ranges_with_second_field.txt","r")
      
        self.assertEqual(self.policyFactory.getRuleTuple(),expectedOutput.read())


        
    def init3Trees(self):
       self.tree0 = portnumbertrie.PortNumberTrieTree()
       self.tree1 = portnumbertrie.PortNumberTrieTree()
       self.tree2 = portnumbertrie.PortNumberTrieTree()
       treeList = [self.tree0,self.tree1,self.tree2]
       
       self.policyFactory = policyFactory.PolicyFactory(treeList)
       self.policyFactory.setSeed(311415)