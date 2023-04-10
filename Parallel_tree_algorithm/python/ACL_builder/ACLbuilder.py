import logging

'''
This class is used to build data structure for ACL that the hardware can read.
format is
number of trees
length of the trees
tree0
tree1
tree...
treeN
hashtable length
hashtable data
'''
    
class ACLBuilder():
    def __init__(self, treeList, policyBuilder, hashTable):
        self.treeList = treeList
        self.policyBuilder = policyBuilder
        self.hashTable = hashTable
    
    def buildACL(self):
        self.arrayTree = []
        logging.debug("treeList: " + str(self.treeList))
        for tree in self.treeList:
            self.arrayTree.append(self.convertTreeToArray(tree))
        logging.debug("arrayTree: " + str(self.arrayTree))


    def convertTreeToArray(self, tree):
        # self.output = []
        # self.output = DLL(tree.root.codeword)
        
        # self.n.show("tree.html",False)
        return (self.bfs(tree)[-1][0], self.bfs(tree))
    
    def treeToVHDL(self, tree):
        vhdlString = ""
        list = self.bfs(tree)
        file = open("tree/tree_data_tb.txt", "w")
        file.write("00000000\n")
        output = self.bfs(tree)
        for element in output:
            if bool(element[1]):
                codeword = format(int(element[1], 2), '04X')
            else:
                codeword = format(0, '04X')
            if element[2]:
                zeroPointer = format(element[2], '02X')
            else:
                zeroPointer = format(0, '02X')
            if element[3]:
                onePointer = format(element[3], '02X')
            else:
                onePointer = format(0, '02X')

            logging.debug("codeword: " + str(codeword) + " zeroPointer: " + str(zeroPointer) + " onePointer: " + str(onePointer))
            file.write(codeword + zeroPointer + onePointer+"\n")
        file.close()




    def bfs(self, tree):
        # from pyvis.network import Network
        # self.n = Network("1000px","1000px", directed=True)
        visited = []
        queue = [tree.root]
        idxQueue = [1]
        repList = []
        parrentQueue = [1]
        idx = 0
        # repList.append([idx, tree.root.codeword,None,None])
        
        while queue:
            node = queue.pop(0)
            # idx = idxQueue.pop(0)

            parrent = parrentQueue.pop(0)
            visited.append(node)
            
            # self.n.add_node(idx, label = (node.value+", "+str(idx)), color = "#FF00FF")
            # repList.append([idx, node.codeword,None,None])
            if node.idx is None:
                # repList[-1][1+1] = idx
                # node.children["0"].idx = idx
                repList.append([idx, node.codeword,None,None])

            else:
                # repList[-1][1+1] = node.children["0"].idx
                repList.append([node.idx, node.codeword,None,None])



            for child in node.children.values():
                if child not in visited:
                    idx +=1
                    queue.append(child)
                    # idxQueue.append(idx)
                    parrentQueue.append(idx)
                    # self.n.add_node(idx, label = (child.value+", "+str(idx)), color = child.color) 

                    if child.value == "0":
                        if node.children["0"].idx is None:
                            repList[-1][1+1] = idx
                            node.children["0"].idx = idx
                        else:
                            repList[-1][1+1] = node.children["0"].idx

                        # self.n.add_edge(parrent, idx)

                    elif child.value == "1":
                        if node.children["1"].idx is None:
                            repList[-1][2+1] = idx
                            node.children["1"].idx = idx
                        else:
                            repList[-1][2+1] = node.children["1"].idx
                        # self.n.add_edge(parrent, idx)


                        
                    # self.n.add_edge(parrent, idx)
        return repList
        # logging.debug("repList: ")
        # for rep in repList:
        #     logging.debug(rep)


      
       
       
