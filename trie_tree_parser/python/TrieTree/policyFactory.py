import trie_tree_parser.python.TrieTree.protocolTrieTree as protocolTrieTree
import trie_tree_parser.python.TrieTree.TrieTree as trieTree
class PolicyFactory:
    def __init__(self):
        pass
    def constructPolicy(self,rulelist):
        # protocolTree = protocolTrieTree.ProtocolTrieTree()
        # protocolTree.insert(rulelist[0].protocol)
        # protocolTree.drawGraph(html=True)
        # protocolTree.match("TCP")
        tree = trieTree.TrieTree()
        tree.insert(rulelist[0].protocol)
        
        tree.root