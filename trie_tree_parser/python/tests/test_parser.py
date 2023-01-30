import unittest

from trie_tree_parser.python.ruleParsers.ruleParser import RuleParser


# from trie_tree_parser.python.TrieTree.TrieTree import Trie
class TestParser(unittest.TestCase):
    def setUp(self):
       self.ruleParser = RuleParser()
    def test_parser(self):
        self.ruleParser.toString()
        self.assertEqual(1,1)
    
if __name__ == '__main__':
    unittest.main()

