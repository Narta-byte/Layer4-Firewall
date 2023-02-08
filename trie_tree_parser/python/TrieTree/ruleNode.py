import trie_tree_parser.python.TrieTree.TrieTree as trieTree

class RuleNode(trieTree.TrieNode):
    def __init__(self, ch):
        super().__init__(ch)
        self.color = "#000000"