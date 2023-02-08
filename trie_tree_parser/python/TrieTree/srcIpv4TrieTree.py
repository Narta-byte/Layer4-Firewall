from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import trie_tree_parser.python.TrieTree.TrieTree as trieTree
import trie_tree_parser.python.TrieTree.srcPortTrieTree as srcPortTrieTree

class SrcIpv4TrieNode(trieTree.TrieNode):
    def __init__(self, ch):
        super().__init__(ch)
        self.color = "#FFA500"
class SrcIpv4TrieTree(trieTree.TrieTree):
    def __init__(self,ch = ''):
        self.root = SrcIpv4TrieNode(ch)
        self.root.color = "#AAA500"
    def insert(self, ipv4, rule, ruleObject, binaryInput = False):
        ipv4, length = self.extractCIDR(ipv4)
        if not binaryInput:
            ipv4 = self.ipv4Tobinary(ipv4)
        
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = ipv4[level]
            if ch == ".":
                continue
            if ch in child:
                crawl = child[ch]
            else:
                if level != length-1:
                    temp =SrcIpv4TrieNode(ch)
                    child[ch] = temp
                    crawl = temp
                    
                else:
                    # temp =srcPortTrieTree.SrcPortTrieNode(ch)
                    temp =SrcIpv4TrieNode(ch)
                    child[ch] = temp
                    srcPortTree =  srcPortTrieTree.SrcPortTrieTree()
                    srcPortTree.insert(ruleObject)
                    child[ch].children[ruleObject.srcPort] = srcPortTree.root
                    crawl = temp
                    pass
        
        crawl.isEnd = True
        crawl.rule = rule
        
    def match(self, ipv4, binaryInput = False):
        ipv4, junk = self.extractCIDR(ipv4)
        if not binaryInput:
            ipv4 = self.ipv4Tobinary(ipv4)
        result = ""
        length = len(ipv4)
        crawl = self.root
        level, prevMatch = 0, 0
        latestRule = "NO_RULES"
        for level in range(length):
            ch = ipv4[level]
            child = crawl.children
            if crawl.rule != "NO_RULE":
                latestRule = crawl.rule
            if ch in child:
                result += ch
                crawl = child[ch]
                if crawl.isEnd:
                    prevMatch = level + 1
            else:
                break
        if crawl.rule != "NO_RULE":
                latestRule = crawl.rule
        if not crawl.isEnd:
            return latestRule + " : " + result[:prevMatch]
        else:
            return latestRule + " : " + result    
        
    def ipv4Tobinary(self,ipv4):
        ipv4, junk = self.extractCIDR(ipv4)
        ipv4Seg = ipv4.split(".")
        binaryIpv4 = ""
        for octet in ipv4Seg:
            tmp = bin(int(octet))[2:].zfill(8)
            binaryIpv4 += tmp
        return str(binaryIpv4)

    def extractCIDR(self,ipv4):
        if "/" not in ipv4:
            return ipv4, 32
        else:
            ipv4, cidr = ipv4.split("/")
            return ipv4, int(cidr)
    def drawGraph(self,html):
        
        if html == True:
            self.n = Network("1000px","1000px", directed=True)
            self.bfs()
            self.n.show("trie_tree.html",False)
        else: 
            self.n = nx.DiGraph()
            nx.draw(self.n, with_labels=True, font_weight='bold')
            self.bfs()
            plt.show()



class DstIpv4TrieNode(SrcIpv4TrieNode):
    def __init__(self, ch):
        super().__init__(ch)
        self.color = "#00FFFF"


class DstIpv4TrieTree(SrcIpv4TrieTree):
    def __init__(self,ch = ''):
        self.root = DstIpv4TrieNode(ch)
        self.root.color = "#00AAAA"
    def insert(self, ipv4, rule, ruleObject, binaryInput = False):
        ipv4, length = self.extractCIDR(ipv4)
        if not binaryInput:
            ipv4 = self.ipv4Tobinary(ipv4)
        
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = ipv4[level]
            if ch == ".":
                continue
            if ch in child:
                crawl = child[ch]
            else:
                if level != length-1:
                    temp =DstIpv4TrieNode(ch)
                    child[ch] = temp
                    crawl = temp
                    pass
                    
                else:
                    temp =DstIpv4TrieNode(ch)
                    child[ch] = temp
                    dstPortTree =  srcPortTrieTree.dstPortTrieTree()
                    dstPortTree.insert(ruleObject)
                    child[ch].children[ruleObject.srcPort] = dstPortTree.root
                    crawl = temp
                    pass
        
        crawl.isEnd = True
        crawl.rule = rule
