# %%
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt

class TrieNode:
    def __init__(self, ch):
        # self.Noderoot = None
        self.value = ch
        self.children = {}
        self.isEnd = False
        self.rule = "NO_RULE"
        self.color = "#AAAAAA"
class TrieTree:
    def __init__(self,ch = ''):
        self.root = TrieNode(ch)
        # self.root.Noderoot = self.root
    def insert(self, key):
        length = len(key)
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = key[level]
            if ch in child:
                crawl = child[ch]
            else:
                temp = TrieNode(ch)
                child[ch] = temp
                crawl = temp
        crawl.isEnd = True
        
    def match(self, key):
        result = ""
        length = len(key)
        crawl = self.root
        level, prevMatch = 0, 0
        for level in range(length):
            ch = key[level]
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

    def drawGraph(self,html):
        
        if html == True:
            self.n = Network("1000px","1000px", directed=True)
            self.aggregrateBfs()
            self.n.show("trie_tree.html",False)
        else: 
            self.n = nx.DiGraph()
            nx.draw(self.n, with_labels=True, font_weight='bold')
            self.aggregrateBfs()
            plt.show()
            
    def aggregrateBfs(self):
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
                    self.n.add_node(idx, label = child.value, color = child.color) 
                        
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
                # return "#123456"
                return "#123456"
                # raise Exception("Error rule "+ node.rule +" not supported")
    
            
if __name__ == '__main__':
    dict = TrieTree()
    dict.insert("TCP")
    dict.insert("TTP")
    dict.drawGraph(html = True)
# %%
