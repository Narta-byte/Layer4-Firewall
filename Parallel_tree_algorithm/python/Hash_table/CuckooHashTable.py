import logging

class CuckooHashTable:
    def __init__(self):
        self.dictionary = {}
        self.defualtRule = []
    def insert(self, codeword, rule):
       
        for i in range(0, len(rule)-2):
            if rule[i] != '*':
                break
        self.dictionary[codeword] = rule
   
    def lookup(self, codeword):
    
        try:
            return self.dictionary[codeword]
        except:
            logging.debug("No match for codeword: "+str(codeword))
            return self.defualtRule