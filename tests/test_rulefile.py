import Parallel_tree_algorithm.python.ACL_builder.ACLbuilder as ACLbuilder
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable
import unittest
import logging
import random


class TestRuleFile(unittest.TestCase):
    def setUp(self):
        file = open("logs.txt", "w")
        file.flush()
        file.close()
        
        logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')
        
        self.treeList = []
        self.numberOfTrees = 3
        for _ in range(self.numberOfTrees):
            self.treeList.append(policyTrieTree.PolicyTrieTree())
        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.hashTable = CuckooHashTable.CuckooHashTable()

        ruleList = self.createRuleList(10)
        for rule in ruleList:
           self.policyBuilder.insertRule(rule)
        for rule in self.policyBuilder.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        self.policyBuilder.writeCodewords()
        
        self.hashTable.defualtRule = ['*', '*', '*', 'default']

        self.aclBuilder = ACLbuilder.ACLBuilder(self.treeList, self.policyBuilder,  self.hashTable)
        
    def createRuleList(self, numberOfRules = 10):
        ruleList = []
        random.seed(311415)
        for _ in range(0,numberOfRules):
            rule = [""]*(self.numberOfTrees+1)
            for i in range(0, len(rule)):
                chance = random.randint(0,50) 
                rule[i] = format(random.randint(0,2**16),'b') + "*"
            chance = random.randint(0,100)
            if chance < 20:
                rule[len(rule)-1] = "alpha"
            elif chance >= 20 and chance <= 40:
                rule[len(rule)-1] = "beta"
            elif chance > 40 and chance < 60:
                rule[len(rule)-1] = "gamma"
            elif chance > 60 and chance < 80:
                rule[len(rule)-1] = "delta"
            elif chance >= 100:
                rule[len(rule)-1] = "epsilon"
            
            ruleList.append(rule)
        logging.debug("RuleList: " + str(ruleList))
        return ruleList
    
    def test_rulefile(self):
        self.assertTrue(True)

    