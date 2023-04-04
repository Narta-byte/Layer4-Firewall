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
        random.seed(31415)
        self.treeList = []
        self.numberOfTrees = 3
        for _ in range(self.numberOfTrees):
            self.treeList.append(policyTrieTree.PolicyTrieTree())

        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.hashTable = CuckooHashTable.CuckooHashTable()

        ruleList = self.createRuleList(10)
        for rule in ruleList:
           logging.debug("Rule in for loop: " + str(rule))
           self.policyBuilder.insertRule(rule)
        
        for rule in self.policyBuilder.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        self.policyBuilder.writeCodewords()
        
        self.hashTable.defualtRule = ['*', '*', '*', 'default']
        
        self.aclBuilder = ACLbuilder.ACLBuilder(self.treeList, self.policyBuilder,  self.hashTable)
        
    def createRuleList(self, numberOfRules = 10):
        ruleList = []
        for _ in range(0,numberOfRules):
            rule = ["","","",""]
            for i in range(0,3):
                chance = random.randint(0,100)
                if chance <= 2:
                    rule[i] = str(random.randint(0,25))
                elif chance > 2 and chance <= 4:
                    rule[i] = "*"
                elif chance > 4:
                    rule[i] = format(random.randint(0,25),'b') + "*"
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
        return ruleList
    
    def test_treeToVHDL(self):
        logging.debug("treeList: " + str(self.aclBuilder.treeList))
        # self.aclBuilder.treeList[0].drawGraph(html = True)
        parsedTrees = self.aclBuilder.convertTreeToVHDL(self.aclBuilder.treeList[0])
        logging.debug("Parsed trees: " + str(parsedTrees))

        self.assertTrue(True)


    def test_rulefile(self):
        self.assertTrue(True)

    