import unittest
import trie_tree_parser.python.TrieTree.portNumberTrieTree as portnumbertrie
import trie_tree_parser.python.TrieTree.policyFactory as policyFactory
import logging
import trie_tree_parser.python.hashTable.cuckooHashTable as cuckooHashTable


class TestErrorCase(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    def test_wildcard_and_ranges(self):
        self.init3Trees()
        rule0 = ["*","*","3","alpha"]    
        rule1 = ["0","2","*","beta"]    
        rule2 = ["*","*","*","gamma"]    
        self.policyFactory.insertRange(rule0)
        self.policyFactory.insertRange(rule1)
        self.policyFactory.insertRange(rule2)

        self.policyFactory.writeCodewords()
        self.hashTable = cuckooHashTable.CuckooHashTable()
        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1],rule[0])

        logging.debug("hashtable lookup"+str(self.hashTable.lookup(["8","2","3"])))
        logging.debug(self.policyFactory.getRuleTuple())
        
        
    def init3Trees(self):
       self.tree0 = portnumbertrie.PortNumberTrieTree()
       self.tree1 = portnumbertrie.PortNumberTrieTree()
       self.tree2 = portnumbertrie.PortNumberTrieTree()
       treeList = [self.tree0,self.tree1,self.tree2]
       
       self.policyFactory = policyFactory.PolicyFactory(treeList)
       self.policyFactory.setSeed(311415)