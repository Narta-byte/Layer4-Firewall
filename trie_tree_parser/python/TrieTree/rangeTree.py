# %%
from pyvis.network import Network
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
class RangeTree:
    def __init__(self):
        self.root = Node(None)
    def insert(self, rule): # [1,1,1]
        self.child = self.root
        for field in rule:
            if field == "*":
                self.child.children.append(Node(field))
                self.child = self.child.children[0]
            elif "-" not in field:
                self.child.children.append(Node(field))
                self.child = self.child.children[0]
            elif "-" in field:
                indiciesRange = field.split("-")
                for i in range(int(indiciesRange[0]),int(indiciesRange[1])+1): # 'list' object is not callable
                    self.child.children.append(Node(str(i))) # make it fork porpperly
                    # self.insert(self.child.children)
                    self.child = self.child.children[0]               
    def printTree(self):
        self.n = Network("1000px","1000px", directed=True)
        
        
        
        queue = [self.root]
        idx = 0
        while queue:
            node = queue.pop(0)
            print(node.value)
            self.n.add_node(idx)
            for child in node.children:
                self.n.add_edge(idx, child.value)
                queue.append(child)
        
        self.n.show("trie_tree.html",False)
    
rt = RangeTree()
rt.insert(["1","2","2-3"])
rt.printTree()
# %%
