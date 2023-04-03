import logging


class ACLBuilder():
    def __init__(self, treeList, policyBuilder, hashTable):
        self.treeList = treeList
        self.policyBuilder = policyBuilder
        self.hashTable = hashTable
    
    def buildACL(self):
        self.VHDLtreeTuple = []
        for tree in self.treeList:
            self.VHDLtreeTuple.append(self.convertTreeToVHDL(tree))

    def convertTreeToVHDL(self, tree):
        treeLength = 0

        return (treeLength, tree)