# %%
from pyvis.network import Network
class Node:
    def __init__(self, value, depth = 0):
        self.value = value
        self.children = []
        self.depth = depth
class RangeTree:
    def __init__(self):
        self.root = Node(None)
        self.TotalruleList = []
    def insert(self, rule, root, ruleList, depth = 0,):
         if depth == len(rule):
             self.TotalruleList.append(ruleList)
             return
         self.child = root
         if rule[depth] == "*":
            self.child.children.append(Node(rule[depth]))
            ruleList.append(rule[depth])
            self.insert(rule, self.child.children[0],ruleList, depth+1)
            
         elif "-" not in rule[depth]:
            self.child.children.append(Node(rule[depth]))
            ruleList.append(rule[depth])
            self.insert(rule, self.child.children[0],ruleList, depth+1)
            
         elif "-" in rule[depth]:
                indiciesRange = rule[depth].split("-")
                for i in range(int(indiciesRange[0]),int(indiciesRange[1])+1):
                    self.child.children.append(Node(str(i)))
                for child in self.child.children:
                    tempRuleList = ruleList.copy()
                    tempRuleList.append(child.value)
                    self.insert(rule, child, tempRuleList, depth+1)
                    
    def printTree(self):
        self.n = Network("1000px","1000px", directed=True)
        visited = []
        queue = [self.root]
        parrentQueue = [1]
        idx = 1
        while queue:
            node = queue.pop(0)
            parrent = parrentQueue.pop(0)
            visited.append(node)
            self.n.add_node(idx, label = node.value, color = "#FF00FF")
            for child in node.children:
                if child not in visited:
                    queue.append(child)
                    idx +=1
                    parrentQueue.append(idx)
                    self.n.add_node(idx, label = child.value) 
                        
                    self.n.add_edge(parrent, idx)
        self.n.show("range_tree.html",False)
rt = RangeTree()
rt.insert(["1-25","1-25","1-25","1-25"], rt.root, [])
print(rt.TotalruleList)
# rt.printTree()
# %%



