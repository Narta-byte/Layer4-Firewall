import unittest
import trie_tree_parser.python.TrieTree.portNumberTrieTree as portnumbertrie
import trie_tree_parser.python.TrieTree.policyFactory as policyFactory

class TestPortNumberRange(unittest.TestCase):
    def setUp(self):
        self.tree = portnumbertrie.PortNumberTrieTree()
    def test_insert(self):
        self.tree.insertRange("0-2","DENY")
        self.tree.insertRange("1-3","PERMIT")
        # self.tree.drawGraph(html=True)
        # self.tree.drawAggregatedGraph()
        self.assertEqual(self.tree.root.totalRules,4)
    def test_3Trees_overlap(self):
        self.tree0 = portnumbertrie.PortNumberTrieTree()
        self.tree1 = portnumbertrie.PortNumberTrieTree()
        self.tree2 = portnumbertrie.PortNumberTrieTree()
        treeList = [self.tree0,self.tree1,self.tree2]
        
        self.policyFactory = policyFactory.PolicyFactory(treeList)
        rule0 = ["1","1","*","alpha"]
        rule1 = ["*","1","1","beta"]
        defualtRule = ["*","*","*","delta"]
        self.policyFactory.insertRule(rule0)
        self.policyFactory.insertRule(rule1)
        # self.policyFactory.insertRule(defualtRule)
        # self.policyFactory.establishCodewords()
        self.policyFactory.writeCodewords()
        self.tree0.drawGraph(html = True)
        self.tree1.drawGraph(html = True)
        self.tree2.drawGraph(html = True)
