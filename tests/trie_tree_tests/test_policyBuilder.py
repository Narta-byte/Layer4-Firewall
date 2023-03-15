import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import logging
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable

class TestPolicyBuilder(unittest.TestCase):
    def setUp(self):
        self.tree = policyTrieTree.PolicyTrieTree()
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')
        
    def test_3Trees_overlap(self):
        self.init3Trees()
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)
        self.policyBuilder.writeCodewords()
        
        expectedOutput =open("tests/expectedOutput/test_3Trees_overlap.txt","r")
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())
        
    def test_3Trees_overlap_with_default_rule(self):
        self.init3Trees()
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        defualtRule = ["*","*","*","delta"]
        self.policyBuilder.insertRuleHelper(rule0)
        self.policyBuilder.insertRuleHelper(rule1)
        self.policyBuilder.insertRuleHelper(defualtRule)
        self.policyBuilder.writeCodewords()
        
        self.policyBuilder.getRuleTuple()

        expectedOutput =open("tests/expectedOutput/test_3Trees_overlap_with_default_rule.txt","r")
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())
        
    def test_sameRule_twice(self):
        self.init3Trees()
        rule0 = ["1","1","*","alpha"]
        rule1 = ["1","1","*","beta"]
        self.policyBuilder.insertRuleHelper(rule0)
        self.policyBuilder.insertRuleHelper(rule1)
        self.policyBuilder.writeCodewords()
        
        expectedOutput =open("tests/expectedOutput/test_sameRule_twice.txt","r")
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())


        
    def test_simple_rule(self):
        self.init3Trees()
        rule0 = ["1","1","*","alpha"]
        rule1 = ["1","1","1","beta"]

        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)
        self.policyBuilder.writeCodewords()
        
        #self.policyFactory.getRuleTuple()


        expectedOutput =open("tests/expectedOutput/test_simple_rule.txt","r")
        #logging.info(expectedOutput.read())
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())
        
    def test_specific_ranges_with_second_field(self):
        self.init3Trees()
      
        ruleList = [["*","*","3","alpha"],
        ["0","2","*","beta"],
        ["*","2","3","delta"],
        ["*","*","*","gamma"] ]
   
        for rules in ruleList:
            self.policyBuilder.insertRuleHelper(rules)

        self.policyBuilder.writeCodewords()
        
        # self.tree0.drawGraph(html=True)
        # self.tree1.drawGraph(html=True)
        # self.tree2.drawGraph(html=True)
        expectedOutput = open("tests/expectedOutput/test_specific_ranges_with_second_field.txt","r")
      
        #self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())


        
    def init3Trees(self):
       self.tree0 = policyTrieTree.PolicyTrieTree()
       self.tree1 = policyTrieTree.PolicyTrieTree()
       self.tree2 = policyTrieTree.PolicyTrieTree()
       treeList = [self.tree0, self.tree1, self.tree2]
       
       self.policyBuilder = PolicyBuilder.PolicyBuilder(treeList)
       self.policyBuilder.setSeed(311415)
       self.policyBuilder.codewordLength = 8



    """ rule0 = ["1","2-3","4-5","alpha"]
    rule1 = ["1","*","4-6","beta"] """