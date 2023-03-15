import Parallel_tree_algorithm.python.Trie_tree.TrieTree as trieTree
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import logging


class PolicyTrieNode(trieTree.TrieNode):
    def __init__(self, key):
        super().__init__(key)
        self.color = "#11BB11"
        self.totalRules = 0
        self.aggrateRule = ""
        self.aggragateChildren = {}
        self.codeword = ""
class PolicyTrieTree(trieTree.TrieTree):
    def __init__(self,key = ''):
        self.root = PolicyTrieNode(key)
        self.root.color = "#123456"
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')

    def insert(self, key, codeword):
        if key != "*":
            key = format(int(key), '016b')
        
        length = len(key)
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
                    
                    self.root.aggragateChildren[key] = temp
                    
                    self.root.aggragateChildren[key] = temp
                    self.root.totalRules += 1
                    child[tempKey] = temp
                    
                    temp.color = "#694200"
                    temp.codeword = codeword
                    
                    
        crawl.isEnd = True
    def to16Bit(self, port):
        keyList = []
        indiciesRange = port.split("-")
        for i in range(int(indiciesRange[0]),int(indiciesRange[1])+1):
            keyList.append(format(int(i), '016b'))
        
        return keyList
    
    def getCodeword(self, key):
        if key != "*":
            key = format(int(key), '016b')
            
        length = len(key)
        crawl = self.root
        child = crawl.children
        tempKey = ""
        for level in range(length):
            child = crawl.children
            tempKey = key[level]
            if tempKey in child:
                crawl = child[tempKey]
                
            else:
           
                return False, 0
        
        return True, crawl.codeword
    
            