#%%
import unittest
# import trie_tree_parser.python.ruleParsers.ruleParser as ruleParser
import Parallel_tree_algorithm.python.TrieTree.ruleParser.ruleParser as ruleParser
import Parallel_tree_algorithm.python.TrieTree.ruleParser.rule as ruleObject

class TestParser(unittest.TestCase):
    def setUp(self):
       self.parser = ruleParser.RuleParser()
    def test_parser(self):
        folderPath = "trie_tree_parser\\rules"
        file = "\\singleRule.rule"
        self.parser.parse(folderPath+file)
        testRule = ruleObject.Rule("TCP","192.168.1.1/32","80","192.168.2.1/24","90","PERMIT")
        testRuleExists = False
        for rule in self.parser.ruleList:
            if rule == testRule:
                testRuleExists = True
        self.assertTrue(testRuleExists)

if __name__ == '__main__':
    unittest.main()


# %%
