# %%
import unittest

# from trie_tree_parser.python.TrieTree.ipv4TrieTree import Ipv4TrieTree
import trie_tree_parser.python.TrieTree.ipv4TrieTree as ipv4TrieTree
# import trie_tree_parser.python.TrieTree.trieTree as ipv4TrieTree

# from trie_tree_parser.python.TrieTree.IpTree import IpTree


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.tree = ipv4TrieTree.Ipv4TrieTree()
        self.tree.insert("192.168.1.1", "PERMIT")

    def test_match(self):
        arg = "192.168.1.1"
        self.assertEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))
        arg = "123.123.123.123"
        self.assertNotEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))

    def test_matchRule(self):
        arg = "192.168.2.1"
        self.tree.insert(arg, "DENY")
        self.assertEqual("DENY : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))
        self.assertNotEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match(arg))

    def test_matchDepth(self):
        arg = "192.168.3.1/24"
        self.tree.insert(arg, "DENY")
        arg = "192.168.3.1"
        self.tree.insert(arg, "PERMIT")
        self.assertEqual("PERMIT : " + self.tree.ipv4Tobinary(arg), self.tree.match("192.168.3.1"))
        self.assertEqual("DENY : " + self.tree.ipv4Tobinary("192.168.3"), self.tree.match("192.168.3.2"))

    def test_extractCIDR(self):
        self.assertEqual(('192.168.1.1', 24), self.tree.extractCIDR("192.168.1.1/24"))
        self.assertEqual(('192.168.1.1', 32), self.tree.extractCIDR("192.168.1.1"))


if __name__ == '__main__':
    unittest.main()

# %%
