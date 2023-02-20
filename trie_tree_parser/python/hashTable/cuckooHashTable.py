
class CuckooHashTable:
    def __init__(self):
        self.dictionary = {}
   
    def insert(self, codeword, rule):
        self.dictionary[codeword] = rule
   
    def lookup(self, codeword):
        return self.dictionary[codeword]

    
