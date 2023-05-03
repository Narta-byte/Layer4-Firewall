import Parallel_tree_algorithm.python.Trie_tree.TrieTree as trieTree
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import logging


class PolicyTrieNode(trieTree.TrieNode):
    def __init__(self, key):
        super().__init__(key)
        self.color = "#11BB11"
        self.aggrateRule = ""
        self.codeword = ""
        self.idx = None
class PolicyTrieTree(trieTree.TrieTree):
    def __init__(self,key = ''):
        self.root = PolicyTrieNode(key)
        self.root.color = "#123456"
        self.treeDepth = 16

    def insert(self, key, codeword):
        if not "*" in key:
            key = format(int(key), "0"+str(self.treeDepth)+'b')
            length = len(key)
        elif key == "*":
            self.root.codeword = codeword
            self.root.color = "#BB1199"
            return
        else:
            key = key.split("*")[0]
            length = len(key)
            logging.debug(f'key: {key} length: {length}')
        crawl = self.root
        for level in range(length):
            child = crawl.children
            tempKey = key[level]
            if tempKey in child:
                crawl = child[tempKey]
                if level == length-1:
                    logging.debug(f'Adding codeword to existing node key: {key} length: {length} codeword: {codeword} tempKey: {tempKey} level: {level}')
                    child[tempKey].color = "#2277BB"
                    child[tempKey].codeword = codeword
                
            else:
                if level != length-1:
                    temp =PolicyTrieNode(tempKey)
                    child[tempKey] = temp
                    crawl = temp
                    
                else:
                    temp =PolicyTrieNode(tempKey)
                    child[tempKey] = temp
                    logging.debug(f'Making new node key: {key} length: {length} codeword: {codeword} tempKey: {tempKey} level: {level}' )
                    temp.color = "#2222BB"
                    temp.codeword = codeword
        crawl.isEnd = True
    
    def getCodeword(self, key):
        if not "*" in key:
            key = format(int(key), "0"+str(self.treeDepth)+'b')
            length = len(key)
        else:
            key = key.split("*")[0]
            length = len(key)
            
        crawl = self.root
        child = crawl.children
        tempKey = ""
        bestMatch = ""
        if crawl.codeword != "":
            bestMatch = crawl.codeword
        for level in range(length):
            if crawl.codeword != "":
                bestMatch = crawl.codeword
            child = crawl.children
            tempKey = key[level]
            if tempKey in child:
                crawl = child[tempKey]
                
            else:
                if bestMatch == "":
                    # logging.debug("False 1 Key: " + str(int(key,2)))
                    return False, ""
                else:
                    # logging.debug("False 2. Key: " + str(int(key,2)))
                    return False, bestMatch
        if crawl.codeword == "":
            # if key != '':
            #     logging.debug("Return 3 Key: " + str(int(key,2)))
            return False, ""
        else:
            # if key != '':
            #     logging.debug("TRUE Key: " + str(int(key,2)))
            return True, crawl.codeword