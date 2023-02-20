import trie_tree_parser.python.TrieTree.TrieTree as trieTree
import trie_tree_parser.python.TrieTree.ruleNode as ruleNode
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import logging


class PortNumberTrieNode(trieTree.TrieNode):
    def __init__(self, ch):
        super().__init__(ch)
        self.color = "#11BB11"
        self.totalRules = 0
        self.aggrateRule = ""
        self.aggragateChildren = {}
        self.codeword = ""
class PortNumberTrieTree(trieTree.TrieTree):
    def __init__(self,ch = ''):
        self.root = PortNumberTrieNode(ch)
        self.root.color = "#123456"
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')
    

    def insert(self, key, strRule,codeword):
        if key != "*":
            key = format(int(key), '016b')
        
        length = len(key)
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = key[level]
            if ch in child:
                crawl = child[ch]
            else:
                if level != length-1:
                    temp =PortNumberTrieNode(ch)
                    child[ch] = temp
                    crawl = temp
                    
                else:
                    temp =PortNumberTrieNode(ch)
                    if strRule == "PERMIT":
                        temp.color = "#1111BB"
                        temp.aggrateRule = "PERMIT"
                        # temp.value = str(ch) + " VALUE = " + str(int(key,2))
                        
                    else: 
                        temp.color = "#BB1111"
                        temp.aggrateRule = "DENY"
                        # temp.value = str(ch) + " VALUE = " + str(int(key,2))
                    
                    self.root.aggragateChildren[key] = temp
                    
                    self.root.aggragateChildren[key] = temp
                    self.root.totalRules += 1
                    child[ch] = temp
                    # temp.children["codeword"] = ruleNode.RuleNode(codeword)
                    
                    temp.color = "#694200"
                    temp.codeword = codeword
                    
                    
        crawl.isEnd = True
    def portToBinary(self, port):
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
        ch = ""
        for level in range(length):
            child = crawl.children
            ch = key[level]
            if ch in child:
                crawl = child[ch]
                # logging.debug("first : "+ child[ch].codeword)
                # logging.debug("first : "+child[ch].codeword)
                
            else:
           
                return False, 0
        # logging.debug("last : "+str(crawl.codeword))
        return True, crawl.codeword
                    
               
                    
                    
        
        
        
    
    
        

        
    # def drawAggregatedGraph(self):
    #     self.n = Network("1000px","1000px", directed=True)
    #     self.aggregrateBfs()
    #     self.n.show("trie_tree.html",False)
    # def aggregrateBfs(self):
    #     visited = []
    #     queue = [self.root]
    #     parrentQueue = [1]
    #     idx = 1
    #     while queue:
    #         node = queue.pop(0)
    #         parrent = parrentQueue.pop(0)
    #         visited.append(node)
    #         self.n.add_node(idx, label = node.value, color = "#FF00FF")
    #         for child in node.aggragateChildren.values():
    #             if child not in visited:
    #                 queue.append(child)
    #                 idx +=1
    #                 parrentQueue.append(idx)
    #                 self.n.add_node(idx, label = child.value, color = child.color) 
                        
    #                 self.n.add_edge(parrent, idx)