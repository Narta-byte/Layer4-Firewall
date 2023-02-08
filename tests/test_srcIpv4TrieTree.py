# %%
import unittest

import trie_tree_parser.python.TrieTree.srcIpv4TrieTree as srcIpv4TrieTree
import trie_tree_parser.python.TrieTree.ruleParser.rule as ruleObject

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.tree = srcIpv4TrieTree.SrcIpv4TrieTree()
        self.ruleObject = ruleObject.Rule("UDP","1.1.1.1/8","80","2.2.2.2","90","DENY")
        self.tree.insert("192.168.1.1", "PERMIT",self.ruleObject)

    def test_match(self):
        arg = "192.168.1.1"
        self.assertEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))
        arg = "123.123.123.123"
        self.assertNotEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))

    def test_matchRule(self):
        arg = "192.168.2.1"
        self.tree.insert(arg, "DENY", self.ruleObject)
        self.assertEqual("DENY : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))
        self.assertNotEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))

    def test_matchDepth(self):
        arg = "192.168.3.1/24"
        self.tree.insert(arg, "DENY", self.ruleObject)
        arg = "192.168.3.1"
        self.tree.insert(arg, "PERMIT", self.ruleObject)
        self.assertEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match("192.168.3.1"))
        self.assertEqual("DENY : " + self.tree.ipv4Tobinary("192.168.3"), self.tree.match("192.168.3.2"))

    def test_extractCIDR(self):
        self.assertEqual(('192.168.1.1', 24), self.tree.extractCIDR("192.168.1.1/24"))
        self.assertEqual(('192.168.1.1', 32), self.tree.extractCIDR("192.168.1.1"))


if __name__ == '__main__':
    unittest.main()

# %%
