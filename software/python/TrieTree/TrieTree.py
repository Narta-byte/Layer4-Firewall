# %%
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
class TrieNode:
    def __init__(self, ch):
        self.value = ch
        self.children = {}
        self.isEnd = False
        self.rule = "NO_RULE"
class Trie:
    def __init__(self):
        self.root = TrieNode('')

    def insert(self, ipv4, rule, binaryInput = False):
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
                temp = TrieNode(ch)
                child[ch] = temp
                crawl = temp
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
            
    def bfs(self):
        visited = []
        queue = [self.root]
        parrentQueue = [1]
        idx = 1
        while queue:
            node = queue.pop(0)
            parrent = parrentQueue.pop(0)
            visited.append(node)
            self.n.add_node(idx, label = node.value, color = "#FF00FF")
            for child in node.children.values():
                if child not in visited:
                    queue.append(child)
                    idx +=1
                    parrentQueue.append(idx)
                    self.n.add_node(idx, label = child.value, color = self.getColor(child)) 
                    self.n.add_edge(parrent, idx)
    def getColor(self, node):
        match node.rule:
            case "NO_RULE":
                return "#AAAAFF"
            case "PERMIT":
                return "#00FF00"
            case "DENY":
                return "#FF0000"
            case _:
                raise Exception("Error rule "+ node.rule +" not supported")
            

# %%