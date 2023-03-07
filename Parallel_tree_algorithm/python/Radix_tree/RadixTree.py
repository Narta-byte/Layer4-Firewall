# %%
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt


class RadixNode():
    def __init__(self, codeword = "", is_word=False, keys=None, value = None):
        self.is_word = is_word
        self.children = keys if keys else {}
        self.value = value
        self.color = "#AAAAAA"
        self.codeword = codeword
        
class RadixTree():
    def __init__(self):
        self.root=RadixNode()

    def insert(self, word, codeword):
        node = self.root
        while True:
            for key, child in node.children.items():
                prefix, split, rest = self.match(key, word)
                if not split:
                    if not rest:
                        child.is_word = True
                        return True
                    else:
                        node = child
                        word = rest
                        break
                if prefix:
                    new_node = RadixNode(codeword, is_word=not rest, keys={split: child}, value = word)
                    node.children[prefix] = new_node
                    del node.children[key]
                    node = new_node
                    word = rest
                    break
            else:
                node.children[word] = RadixNode(codeword, is_word=True, value = word)
                return

    def search(self, word):
        node = self.root
        while True:
            for key, child in node.children.items():
                prefix, split, rest = self.match(key, word)
                if not split and not rest:
                    return child.is_word, child.codeword
                if not split:
                    node = child
                    word = rest
                    break
            else:
                return False, 0

    def match(self, key, word):
        i = 0
        while i < len(key) and i < len(word) and key[i] == word[i]:
            i += 1
        return key[:i], key[i:], word[i:]
        
    def drawGraph(self,html):
        if html == True:
            self.n = Network("1000px","1000px", directed=True)
            self.bfs()
            self.n.show("radix_tree.html",False)
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
                    self.n.add_node(idx, label = child.value, color = child.color) 
                        
                    self.n.add_edge(parrent, idx)
    
    
if __name__ == "__main__":
    tree = RadixTree()
    tree.insert("app","b")
    tree.insert("apple","a")
    tree.insert("apple pie", "C")
    tree.insert("banana", "adsf")
    tree.insert("orange", "A")
    # print(tree.search("apple")) # True
    # print(tree.search("pear")) # False
    # print(tree.starts_with("ba")) # True
    # print(tree.starts_with("gr")) # False

    # print(tree.search("apple"))
    # print(tree.search("apple pie"))
    # print(tree.search("banana"))
    # print(tree.search("Kage"))
    tree.drawGraph(html=True)
    
    print(tree.search("apple"))
    print(tree.search("app"))
    print(tree.search("hoæsdaig"))
    # assert tree.search("apple") == "apple"
    # assert tree.search("apartment") == "apartment"
    # assert tree.search("appendix") == "appendix"
    # assert tree.search("book") == "book"
    # assert tree.search("bike") == "bike"
    # assert tree.search("bat") == "bat"
    # assert tree.search("baby") == "baby"
    # assert tree.search("bake") == "bake"

    # assert tree.search("ap") == "apple"
# %%
