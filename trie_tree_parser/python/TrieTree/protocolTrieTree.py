# %%
import trie_tree_parser.python.TrieTree.TrieTree as trieTree
import trie_tree_parser.python.TrieTree.srcIpv4TrieTree as srcIpv4TrieTree


import trie_tree_parser.python.TrieTree.ruleParser.rule as ruleObject
class ProtocolNode(trieTree.TrieNode):
    def __init__(self, ch):
        super().__init__(ch)
        self.color = "#AA1111"
class ProtocolTrieTree(trieTree.TrieTree):
    def __init__(self):
        self.root = ProtocolNode('')
    def insert(self, rule):
        # length = 1
        crawl = self.root
        # for level in range(length):
        child = crawl.children
        ch = rule.protocol
        if ch in child:
            crawl = child[ch]
        else:
            temp = ProtocolNode(ch)
            child[ch] = temp
            ipv4Tree =  srcIpv4TrieTree.SrcIpv4TrieTree()
            ipv4Tree.insert(rule.srcIp,"PERMIT",rule)
            child[ch].children[rule.srcIp] = ipv4Tree.root
            crawl = temp
        crawl.isEnd = True
        
if __name__ == '__main__':
    # import trie_tree_parser.python.TrieTree.TrieTree as trieTree
    import TrieTree as trieTree
    ruleObject = ruleObject.Rule("UDP","1*","80","2*","90","DENY")
    tree = ProtocolTrieTree()
    tree.insert(ruleObject)
    # dict.insert("UDP")
    # dict.insert("TCP")
    
    tree.drawGraph(html=True)
# %%
