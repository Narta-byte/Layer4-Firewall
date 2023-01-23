from pyvis.network import Network
import networkx as nx

class TrieNode:
    def __init__(self, ch):
        self.value = ch
        self.children = {}
        self.bIsEnd = False
    
    def getValue(self):
        return self.value
    
    def setIsEnd(self, val):
        self.bIsEnd = val
    
    def isEnd(self):
        return self.bIsEnd

class Trie:
    def __init__(self):
        self.root = TrieNode('')
        self.n = Network("1000px","1000px")
    
    def insert(self, word):
        length = len(word)
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = word[level]
            if ch == ".":
                continue
            if ch in child:
                crawl = child[ch]
            else:
                temp = TrieNode(ch)
                child[ch] = temp
                crawl = temp
        crawl.setIsEnd(True)
        
    def getMatchingPrefix(self, input):
        result = ""
        length = len(input)
        crawl = self.root
        level, prevMatch = 0, 0
        for level in range(length):
            ch = input[level]
            child = crawl.children()
            if ch in child:
                result += ch
                crawl = child[ch]
                if crawl.isEnd():
                    prevMatch = level + 1
            else:
                break
        if not crawl.isEnd():
            return result[:prevMatch]
        else:
            return result

    def inOrder(self,node,level):
        if node is None:
            return
        print(node.getValue())
        self.n.add_node(level,label=node.getValue())
        children = node.children
        myLevel = level
        for child in children:
            level+=1
            self.inOrder(children[child],level)
            self.n.add_edge(myLevel,level)
        
    def drawGraph(self):
        self.bfs()
        self.n.show("trie_tree.html")
    def bfs(self):
        visited = []
        queue = [self.root]
        parrentQueue = [1]
        idx = 1
        while queue:
            node = queue.pop(0)
            parrent = parrentQueue.pop(0)
            visited.append(node)
            print(node.value)
            self.n.add_node(idx, label=node.value,color="#FF0000")
            for child in node.children.values():
                if child not in visited:
                    queue.append(child)
                    idx +=1
                    parrentQueue.append(idx)
                    self.n.add_node(idx, label=child.value)
                    self.n.add_edge(parrent, idx)
            
            

dict = Trie()
#dict.insert("hat")
#dict.insert("cat")
#dict.insert("car")
#dict.insert("cathat")
#dict.insert("catmat")
dict.insert("192.168.1.1")
dict.insert("192.168.2.1")
dict.drawGraph()