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
        for tree in self.treeList:
            self.arrayTree.append(self.convertTreeToArray(tree))
        file = open("tree/tree_data_tb.txt", "w")

        for i, tree in enumerate(self.treeList):
            # file.write(self.treeToVHDL(self.treeList[i])[0])
            file.write(self.treeToVHDL(self.treeList[i])[0])
        file.close()


    def convertTreeToArray(self, tree):
       
        return (self.bfs(tree)[-1][0], self.bfs(tree))
    
    def treeToVHDL(self, tree, addressLength = '04X', dataLength = '04X'):
        vhdlString = ""
        list = self.bfs(tree)
        # file = open("tree/tree_data_tb.txt", "w")
        vhdlString += (str(format(0, dataLength)) + str(format(0, addressLength)) + str(format(0, addressLength))+"\n")
        length = 1


        output = self.bfs(tree)
        logging.debug("output: " + str(output))
        for i in range(len(output)):
            element = [0,0,0,0]
            if len(output) > i: 
                element = output[i]
            
            logging.debug("element: " + str(element))
            length += 1
            if bool(element[1]):
                codeword = format(int(str(element[1]), 2), dataLength)
            else:
                codeword = format(0, dataLength)
            if element[2]:
                zeroPointer = format(element[2], addressLength)
            else:
                zeroPointer = format(0, addressLength)
            if element[3]:
                onePointer = format(element[3], addressLength)
            else:
                onePointer = format(0, addressLength)

            logging.debug("codeword: " + str(codeword) + " zeroPointer: " + str(zeroPointer) + " onePointer: " + str(onePointer))
            vhdlString += (codeword + zeroPointer + onePointer+"\n")
        return vhdlString, length
        # file.close()




    def bfs(self, tree):
        # from pyvis.network import Network
        # self.n = Network("1000px","1000px", directed=True)
        visited = []
        queue = [tree.root]
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


      
       
       
