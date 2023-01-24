# %%
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt

class TrieNode:
    def __init__(self, ch):
        self.value = ch
        self.children = {}
        self.isEnd = False
class Trie:
    def __init__(self):
        self.root = TrieNode('')
        # self.n = Network("1000px","1000px")
        #self.n = nx.Graph()
    def insert(self, ipv4):
        ipv4 = self.ipv4Tobinary(ipv4)
        length = len(ipv4)
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
        
    def getMatchingPrefix(self, input):
        result = ""
        input = self.ipv4Tobinary(input)
        length = len(input)
        crawl = self.root
        level, prevMatch = 0, 0
        for level in range(length):
            ch = input[level]
            child = crawl.children
            if ch in child:
                result += ch
                crawl = child[ch]
                if crawl.isEnd:
                    prevMatch = level + 1
            else:
                break
        if not crawl.isEnd:
            return result[:prevMatch]
        else:
            return result

    def ipv4Tobinary(self,ipv4Addr):
        ipv4Addr_seg = ipv4Addr.split(".")
        binaryIpv4Addr = ""
        for octet in ipv4Addr_seg:
            tmp = bin(int(octet))[2:].zfill(8)
            binaryIpv4Addr += tmp
        return str(binaryIpv4Addr)

    def drawGraph(self,html):
        
        if html == True:
            self.n = Network("1000px","1000px")
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
            self.n.add_node(idx, label=node.value,color="#FF0000")
            for child in node.children.values():
                if child not in visited:
                    queue.append(child)
                    idx +=1
                    parrentQueue.append(idx)
                    self.n.add_node(idx, label = child.value)
                    self.n.add_edge(parrent, idx)
            
            

# %%