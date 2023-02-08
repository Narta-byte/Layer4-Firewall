import trie_tree_parser.python.TrieTree.TrieTree as trieTree
import trie_tree_parser.python.TrieTree.srcIpv4TrieTree as srcIpv4TrieTree
import trie_tree_parser.python.TrieTree.ruleNode as ruleNode
#%%
# import trie_tree_parser.python.TrieTree.srcIpv4TrieTree as srcIpv4TrieTree
# import srcIpv4TrieTree as srcIpv4TrieTree
class SrcPortTrieNode(trieTree.TrieNode):
    def __init__(self, ch):
        super().__init__(ch)
        self.color = "#11BB11"
class SrcPortTrieTree(trieTree.TrieTree):
    def __init__(self, ch = ''):
        self.root = SrcPortTrieNode(ch)
        self.root.color = "#118811"
    def insert(self, rule, binaryInput = False):
        length = 16
        if not binaryInput:
            srcPort = self.portToBinary(rule.srcPort)
        else:
            srcPort = rule.srcPort, len(rule.srcPort)
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = srcPort[level]
            if ch in child:
                crawl = child[ch]
            else:
                if level != length-1: #-1
                    temp =SrcPortTrieNode(ch)
                    child[ch] = temp
                    crawl = temp
                    
                else:
                    temp =srcIpv4TrieTree.DstIpv4TrieNode(ch)
                    child[ch] = temp
                    dstIpv4Tree =  srcIpv4TrieTree.DstIpv4TrieTree()
                    dstIpv4Tree.insert(rule.dstIp,"PERMIT",rule)
                    child[ch].children[rule.dstIp] = dstIpv4Tree.root
                    crawl = temp
                    pass
        crawl.isEnd = True
        crawl.rule = rule
    def portToBinary(self, port):
        decimal = int(port)
        binary = format(decimal, '016b')
        return binary
        # return "1111111111111111", 15

class dstPortTrieNode(SrcPortTrieNode):
    def __init__(self, ch):
        super().__init__(ch)
        self.color = "#1111BB"
class dstPortTrieTree(SrcPortTrieTree):
    def __init__(self, ch = ''):
        self.root = dstPortTrieNode(ch)
        self.root.color = "#111188"
    def insert(self, rule, binaryInput = False):
        length = 16
        if not binaryInput:
            dstPort = self.portToBinary(rule.dstPort)
        else:
            dstPort = rule.dstPort, len(rule.dstPort)
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = dstPort[level]
            if ch in child:
                crawl = child[ch]
            else:
                if level != length-1: #-1
                    temp =dstPortTrieNode(ch)
                    child[ch] = temp
                    crawl = temp
                    
                else:
                    temp = ruleNode.RuleNode(ch)
                    child[ch] = temp
                    # # dstIpv4Tree =  srcIpv4TrieTree.DstIpv4TrieTree()
                    # # dstIpv4Tree.insert(rule.dstIp,"PERMIT",rule)
                    # child[ch].children[rule.Answer] = dstIpv4Tree.root
                    # crawl = temp
                    pass
        crawl.isEnd = True
        crawl.rule = rule
    def portToBinary(self, port):
        decimal = int(port)
        binary = format(decimal, '016b')
        return binary
        # return "1111111111111111", 15