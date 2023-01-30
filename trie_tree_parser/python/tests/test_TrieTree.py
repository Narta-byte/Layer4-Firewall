import unittest

from trie_tree_parser.python.TrieTree.TrieTree import Trie
class TestTrie(unittest.TestCase):
    def setUp(self):
        self.dict = Trie()
        self.dict.insert("192.168.1.1","PERMIT")
     
    def test_match(self):
        arg = "192.168.1.1"
        self.assertEqual("PERMIT : " + self.dict.ipv4Tobinary(arg), self.dict.match(arg))
        arg = "123.123.123.123"
        self.assertNotEqual("PERMIT : " + self.dict.ipv4Tobinary(arg), self.dict.match(arg))
    
    def test_matchRule(self):
        arg = "192.168.2.1"
        self.dict.insert(arg,"DENY")
        self.assertEqual("DENY : " + self.dict.ipv4Tobinary(arg), self.dict.match(arg))
        self.assertNotEqual("PERMIT : " + self.dict.ipv4Tobinary(arg), self.dict.match(arg))

    def test_matchDepth(self):
        arg = "192.168.3.1/24"
        self.dict.insert(arg,"DENY")
        arg = "192.168.3.1"
        self.dict.insert(arg,"PERMIT")
        self.assertEqual("PERMIT : " + self.dict.ipv4Tobinary(arg), self.dict.match("192.168.3.1"))
        self.assertEqual("DENY : " + self.dict.ipv4Tobinary("192.168.3"), self.dict.match("192.168.3.2"))
        
    def test_extractCIDR(self):
        self.assertEqual(('192.168.1.1', 24),self.dict.extractCIDR("192.168.1.1/24"))
        self.assertEqual(('192.168.1.1',32),self.dict.extractCIDR("192.168.1.1"))

if __name__ == '__main__':
    unittest.main()
