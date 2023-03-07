import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as portnumbertrie
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable
import logging


class TestCuckooHashTable(unittest.TestCase):
    def setUp(self):
        self.tree0 = portnumbertrie.PolicyTrieTree()
        self.tree1 = portnumbertrie.PolicyTrieTree()
        self.tree2 = portnumbertrie.PolicyTrieTree()
        treeList = [self.tree0,self.tree1,self.tree2]

        self.policyFactory = PolicyBuilder.PolicyBuilder(treeList)
        self.policyFactory.setSeed(311415)
        
        self.hashTable = CuckooHashTable.CuckooHashTable()
        
    def test_insert_codeword_into_table(self):
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        self.policyFactory.insertRule(rule0)
        self.policyFactory.insertRule(rule1)

        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
            
        logging.debug(self.hashTable.dictionary.values())
        
        for rule in self.policyFactory.previousRuleTuple:
            self.assertEqual(self.hashTable.lookup(rule[1])[3], rule[0][3])
        
    def test_large_input(self):
        rule0 = ["1-10","10-20","1","alpha"]
        rule1 = ["1-10","9-22","1","beta"]
        rule2 = ["5-15","9-27","1","gamma"]
        self.policyFactory.insertRange(rule0)
        self.policyFactory.insertRange(rule1)
        self.policyFactory.insertRange(rule2)
        self.policyFactory.writeCodewords()
        # self.tree0.drawGraph(html=True)
        # self.tree1.drawGraph(html=True)
        # self.tree2.drawGraph(html=True)
        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
           
        logging.debug(self.hashTable.dictionary.values())
            
        for rule in self.policyFactory.previousRuleTuple:
            self.assertEqual(self.hashTable.lookup(rule[1])[3], rule[0][3])
        
    
    