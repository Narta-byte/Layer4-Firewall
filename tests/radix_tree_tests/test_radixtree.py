import unittest
import Parallel_tree_algorithm.python.Radix_tree.PolicyRadixTree as policyRadixTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import logging
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable


class TestRadixTree(unittest.TestCase):
    def setUp(self):
        self.tree0 = policyRadixTree.PolicyRadixTree()
        self.tree1 = policyRadixTree.PolicyRadixTree()
        self.tree2 = policyRadixTree.PolicyRadixTree()
        treeList = [self.tree0,self.tree1,self.tree2]

        self.policyBuilder = PolicyBuilder.PolicyBuilder(treeList)
        self.policyBuilder.setSeed(311415)
        self.policyBuilder.codewordLength = 8
        
        file = open("logs.txt", "w")
        file.flush()
        file.close()
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')
      
        
    def test_3Trees_overlap(self):
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        self.policyBuilder.insertRange(rule0)
        self.policyBuilder.insertRange(rule1)
        self.policyBuilder.writeCodewords()
        
        # self.tree0.drawGraph(html=True)
        # self.tree1.drawGraph(html=True)
        # self.tree2.drawGraph(html=True)
        
        expectedOutput =open("tests/expectedOutput/test_3Trees_overlap.txt","r")
        
        logging.debug("ruleTuple" + self.policyBuilder.getRuleTuple())
        logging.debug("expectedOutput" +expectedOutput.read())
        
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())
    
    
    # it does not pass even though the output is correct🥴
    def test_3Trees_overlap_with_default_rule(self):
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        defualtRule = ["*","*","*","delta"]
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)
        self.policyBuilder.insertRule(defualtRule)
        self.policyBuilder.writeCodewords()
    
        self.policyBuilder.getRuleTuple()

        expectedOutput =open("tests/expectedOutput/test_3Trees_overlap_with_default_rule.txt","r")
        logging.debug("ruleTuple" + self.policyBuilder.getRuleTuple().strip())
        logging.debug("expectedOutput" +expectedOutput.read().strip())
        self.assertEqual(self.policyBuilder.getRuleTuple().strip(),expectedOutput.read().strip())
        

    def test_sameRule_twice(self):
       rule0 = ["1","1","*","alpha"]
       rule1 = ["1","1","*","beta"]
       self.policyBuilder.insertRule(rule0)
       self.policyBuilder.insertRule(rule1)
       self.policyBuilder.writeCodewords()
       
       expectedOutput =open("tests/expectedOutput/test_sameRule_twice.txt","r")
       self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())
    
    
    def test_simple_rule(self):
        rule0 = ["1","1","*","alpha"]
        rule1 = ["1","1","1","beta"]
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)
        self.policyBuilder.writeCodewords()

        expectedOutput =open("tests/expectedOutput/test_simple_rule.txt","r")
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())
        
        
    def test_specific_ranges_with_second_field(self):
        rule0 = ["1","2-3","4-5","alpha"]
        rule1 = ["1","*","4-6","beta"]
        
        self.policyBuilder.insertRange(rule0)
        self.policyBuilder.insertRange(rule1)

        self.policyBuilder.writeCodewords()
        
        self.tree0.drawGraph(html=True)
        self.tree1.drawGraph(html=True)
        self.tree2.drawGraph(html=True)
        expectedOutput = open("tests/expectedOutput/test_specific_ranges_with_second_field.txt","r")
      
        self.assertEqual(self.policyBuilder.getRuleTuple(),expectedOutput.read())

