from pyvis.network import Network
import networkx as nx

class TrieNode:
    def __init__(self, ch):
        self.value = ch
        self.children = {}
        self.bIsEnd = False
        
    def getChildren(self):
        return self.children
    
    def getValue(self):
        return self.value
    
    def setIsEnd(self, val):
        self.bIsEnd = val
    
    def isEnd(self):
        return self.bIsEnd

class Trie:
    def __init__(self):
        self.root = TrieNode('')
        self.n = Network("500px","500px")
        self.n.add_node(0,label = "root")
    
    def insert(self, word):
        length = len(word)
        crawl = self.root
        for level in range(length):
            child = crawl.getChildren()
            ch = word[level]
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
            child = crawl.getChildren()
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
        children = node.getChildren()
        myLevel = level
        for child in children:
            level+=1
            self.inOrder(children[child],level)
            self.n.add_edge(myLevel,level)
        
    def drawGraph(self):
        self.inOrder(self.root,1)
        children = self.root.getChildren()
        for child in children:
            self.n.add_edge(0,child)
        self.n.show("trie_tree.html")
                
            

dict = Trie()
dict.insert("hat")
dict.insert("cat")

# input = "192.168.1.1"
# print(input + ":   ", end="")
# print(dict.getMatchingPrefix(input))

# input = "192.168.1.2"
# print(input + ":   ", end="")
# print(dict.getMatchingPrefix(input))

# input = "192.168.2.2"
# print(input + ":   ", end="")
# print(dict.getMatchingPrefix(input))


dict.drawGraph()