import logging


    
class ACLBuilder():
    def __init__(self, treeList, policyBuilder, hashTable):
        self.treeList = treeList
        self.policyBuilder = policyBuilder
        self.hashTable = hashTable
    
    def buildACL(self):
        self.VHDLtreeTuple = []
        logging.debug("treeList: " + str(self.treeList))
        for tree in self.treeList:
            self.VHDLtreeTuple.append(self.convertTreeToVHDL(tree))

    def convertTreeToVHDL(self, tree):
        treeLength = 0
        self.i = 0
        # self.output = []
        # self.output = DLL(tree.root.codeword)
        self.bfs(tree)
        self.n.show("tree.html",False)

        self.output = []

        return (treeLength, tree)
    
    def bfs(self, tree):
        from pyvis.network import Network
        self.n = Network("1000px","1000px", directed=True)
        visited = []
        queue = [tree.root]
        idxQueue = [1]
        repList = []
        # repList.append([tree.root.codeword,None,None])
        parrentQueue = [1]
        idx = 0
        
        while queue:
            node = queue.pop(0)
            idx = idxQueue.pop(0)

            parrent = parrentQueue.pop(0)
            visited.append(node)
            
            self.n.add_node(idx, label = (node.value+", "+str(idx)), color = "#FF00FF")
            repList.append([idx, node.codeword,None,None])
            for child in node.children.values():
                if child not in visited:
                    idx +=1
                    queue.append(child)
                    idxQueue.append(idx)
                    parrentQueue.append(idx)
                    self.n.add_node(idx, label = (child.value+", "+str(idx)), color = child.color) 

                    # try: 
                    if child.value == "0":
                        repList[-1][1+1] = idx
                        self.n.add_edge(parrent, idx)

                    elif child.value == "1":
                        repList[-1][2+1] = idx
                        self.n.add_edge(parrent, idx)

                    # except KeyError:
                    #     pass

                        
                    # self.n.add_edge(parrent, idx)
        logging.debug("repList: ")
        for rep in repList:
            logging.debug(rep)


      
       
       
