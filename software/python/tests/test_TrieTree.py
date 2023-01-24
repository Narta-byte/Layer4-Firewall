import unittest

from software.python.TrieTree.TrieTree import Trie
class TestTrie(unittest.TestCase):
    def setUp(self):
        self.dict = Trie()
        self.dict.insert("192.168.1.1")
     
    def test_getMatchingPrefix(self):
        arg = "192.168.1.1"
        self.assertEqual(self.dict.ipv4Tobinary(arg), self.dict.getMatchingPrefix(arg))
        arg = "123.123.123.123"
        self.assertNotEqual(self.dict.ipv4Tobinary(arg), self.dict.getMatchingPrefix(arg))
    

if __name__ == '__main__':
    unittest.main()
