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
class PolicyTrieTree(trieTree.TrieTree):
    def __init__(self,key = ''):
        self.root = PolicyTrieNode(key)
        self.root.color = "#123456"
        self.treeDepth = 16

    def insert(self, key, codeword):
        if not "*" in key:
            key = format(int(key), '016b')
            length = len(key)
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
            else:
                if level != length-1:
                    temp =PolicyTrieNode(tempKey)
                    child[tempKey] = temp
                    crawl = temp
                    
                else:
                    temp =PolicyTrieNode(tempKey)
                    child[tempKey] = temp
                    
                    temp.color = "#2222BB"
                    temp.codeword = codeword
        crawl.isEnd = True

    def to16Bit(self, port):
        keyList = []
        indiciesRange = port.split("-")
        for i in range(int(indiciesRange[0]),int(indiciesRange[1])+1):
            keyList.append(format(int(i), '016b'))
        
        return keyList
    
    def getCodeword(self, key):
        if not "*" in key:
            key = format(int(key), '016b')
            length = len(key)
        else:
            key = key.split("*")[0]
            length = len(key)
            logging.debug(f'key: {key} length: {length}')
            

        crawl = self.root
        child = crawl.children
        tempKey = ""
        for level in range(length):
            # logging.debug("crawl codeWord: " + str(crawl.codeword))
            child = crawl.children
            tempKey = key[level]
            if tempKey in child:
                crawl = child[tempKey]
                
            else:
                # logging.debug("key not found"+ str(crawl.codeword))
                return False, 0
        # logging.debug("key found" + str(crawl.codeword))
        
        return True, crawl.codeword
    
            