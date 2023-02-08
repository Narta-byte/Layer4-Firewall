import unittest
import trie_tree_parser.python.TrieTree.srcPortTrieTree as srcPortTrieTree
import trie_tree_parser.python.TrieTree.ruleParser.rule as ruleObject
class testSrcPortTrieTree(unittest.TestCase):
    def setUp(self):
        self.tree = srcPortTrieTree.SrcPortTrieTree()
        self.ruleObject0 = ruleObject.Rule("UDP","1.1.1.1/8","80","2.2.2.2","90","DENY")
        self.ruleObject1 = ruleObject.Rule("UDP","1.1.1.1/8","90","2.2.2.2","90","DENY")
    def test_insert(self):
        self.tree.insert(self.ruleObject0)
        self.tree.insert(self.ruleObject1)
        self.tree.insert(self.ruleObject0)
        print(self.tree.root.children)
        self.tree.drawGraph(html=True)
        # self.assertEqual(2, len(self.tree.root.children))
        # self.assertEqual(self.tree.root.children,2)
    def test_portToBinary(self):
        self.assertEqual("0000000001010000",self.tree.portToBinary("80"))
        self.assertEqual("0000000001011010",self.tree.portToBinary("90"))
if __name__ == '__main__':
    unittest.main()