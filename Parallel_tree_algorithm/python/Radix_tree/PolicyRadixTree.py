import Parallel_tree_algorithm.python.Radix_tree.RadixTree as radixTree
import logging


class PolicyRadixNode(radixTree.RadixNode):
    pass
class PolicyRadixTree(radixTree.RadixTree):
    def insert(self, key, codeword):
        if key != "*":
            key = format(int(key), '016b')
        
        return super().insert(key, codeword)

    def getCodeword(self, key):
        if key != "*":
            key = format(int(key), '016b')
        return super().search(key)
