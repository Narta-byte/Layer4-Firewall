import unittest
import trie_tree_parser.python.TrieTree.protocolTrieTree as protocolTrieTree
import trie_tree_parser.python.TrieTree.ruleParser.rule as ruleObject


class testProtocolTree(unittest.TestCase):
    def setUp(self):
        self.tree = protocolTrieTree.ProtocolTrieTree()
        # self.tree.insert("TCP")
        # self.tree.insert("UDP")
        # self.tree.insert("TCP")
    def test_insert(self):
        self.ruleObject = ruleObject.Rule("UDP","1.1.1.1/16","80","2.2.2.2/16","90","DENY")
        self.tree.insert(self.ruleObject)
        self.ruleObject = ruleObject.Rule("UDP","1.1.1.1/16","90","1.2.2.2/16","80","PERMIT")
        self.tree.insert(self.ruleObject)
        # self.ruleObject = ruleObject.Rule("TCP","1*","80","2*","90","DENY")
        # self.tree.insert(self.ruleObject)
        # self.assertEqual(2, len(self.tree.root.children))
        self.tree.drawGraph(html=True)
        # self.assertEqual(self.tree.root.children,2)
    
    
if __name__ == '__main__':
    unittest.main()
