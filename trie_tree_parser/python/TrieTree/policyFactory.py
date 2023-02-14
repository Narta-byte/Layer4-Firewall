import random


class PolicyFactory:
    def __init__(self,treeList):
        self.treeList = treeList
        self.previousRuleTuble = []
        self.ruleCodeWord = ""
    
    def insertRuleIntoTree(self,rule,tree):
        i = 0
        ruleCodeword = ""
        for tree in self.treeList:
            
            exists, codeword = tree.getCodeword()
            if not exists:
                codeword = self.generateCodeword(8)
            
            
            
            ruleCodeword += codeword
            tree.insert(rule[i],rule[len(rule)-1], codeword)
            i += 1
        return ruleCodeword
        
    def insertRule(self,rule):
        ruleCodeword = self.insertRuleIntoTree(rule,self.treeList)
        
        # if self.previousRuleTuble != []:
        #     intersectionCodeword = self.generateCodeword(24)
        #     ruleIntersection = []
            
        #     for oldRuleTuble in self.previousRuleTuble:
        #         ruleIntersection = self.intersection(oldRuleTuble, rule)
        #         intersectionCodeword = self.insertRuleIntoTree(ruleIntersection,self.treeList)
                
        #     self.previousRuleTuble.append([ruleIntersection,intersectionCodeword])
        self.previousRuleTuble.append([rule, ruleCodeword])
       
    def intersection(self,rule0,rule1):
        ruleIntersection = ["placeholder0","placeholder1","placeholder2","placeholder3"]
        for i in range(3):
            
            if i == 0 : # add the protocol for the old rule to the intersection rule
                ruleIntersection[3] = rule0[0][3] 
                
            if rule0[0][i] == rule1[i]: # if they are equal
                ruleIntersection[i] = "1"
                
            elif rule0[0][i] == "*" and not rule1 == "*": # rule1 is a subset of rule0
                ruleIntersection[i] = rule1[i]
            
            elif rule1[i] == "*" and not rule0[0] == "*": # or the other way around
                ruleIntersection[i] = rule0[0][i]
        return ruleIntersection
    
    def generateCodeword(self, length):
        codeword = ""
        for _ in range(length):
            codeword += str(random.randint(0,1))
        return codeword
    
    def writeCodewords(self):
        
        file = open("codewords.txt","w") 
        for rule in self.previousRuleTuble:
            file.write(str(rule[0]) + " " + rule[1] + "\n")

        file.close() 