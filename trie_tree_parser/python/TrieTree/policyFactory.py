import random
import logging
import warnings
# import trie_tree_parser.python.TrieTree.rangeTree as rangetree


class PolicyFactory:
    def __init__(self,treeList):
        self.treeList = treeList
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        
    def insertRuleIntoTree(self,rule,tree):
        i = 0
        ruleCodeword = ""
        for tree in self.treeList:
            exists, codeword = tree.getCodeword(rule[i])
            if not exists: 
                codeword = self.generateCodeword(8)
            
            ruleCodeword += codeword
            tree.insert(rule[i],rule[len(rule)-1], codeword)
            i += 1
        return ruleCodeword
    
    def ruleAlreadyExists(self,rule):
        # if the rules fields are equal skip the iteration and let the old rule have precedence
        for oldRuleTuple in self.previousRuleTuple:
            if oldRuleTuple[0][0:len(rule)-1] == rule[0:len(rule)-1]:
                return True
        return False


    def insertRange(self,rule):
        result = [[]]

        for field in rule:
            if "-" in field:
                start, end = field.split("-")
                new_lists = []
                for tal in range(int(start), int(end)+1):
                    for res in result:
                        new_list = res + [str(tal)]
                        new_lists.append(new_list)
                result = new_lists
            else:
                for i in range(len(result)):
                    result[i].append(field)

        for sublist in result:
            self.insertRule(sublist)
            #time.sleep(1)

    def insertRule(self,rule):
        # if the rule already exists, skip the iteration
        if self.ruleAlreadyExists(rule):
            return
        ruleCodeword = self.insertRuleIntoTree(rule, self.treeList)
        
        # if there are no previous rules, add the new rule to the list
        if self.previousRuleTuple == []:
            self.previousRuleTuple.append([rule, ruleCodeword])
            return
        
        intersectionCodeword = self.generateCodeword(24)
        ruleIntersection = []
        
        for oldRuleTuble in self.previousRuleTuple:
            ruleIntersection = self.intersection(oldRuleTuble, rule)
            if ruleIntersection is None:
                continue
            intersectionCodeword = self.insertRuleIntoTree(ruleIntersection,self.treeList)
            
        if ruleIntersection is not None:
            self.previousRuleTuple.append([ruleIntersection,intersectionCodeword])
       
        self.previousRuleTuple.append([rule, ruleCodeword])
        
        
       
    def intersection(self,rule0Tuple,rule1):
        ruleIntersection = ["placeholder0", "placeholder1", "placeholder2", "placeholder3"]


        for i in range(len(rule1)-1):
            
            if i == 0 : # add the protocol for the old rule to the intersection rule
                ruleIntersection[3] = rule0Tuple[0][3] 
                
            if rule0Tuple[0][i] == rule1[i]: # if they are equal
                ruleIntersection[i] = rule1[i]
                
            elif rule0Tuple[0][i] == "*" and not rule1 == "*": # rule1 is a subset of rule0
                ruleIntersection[i] = rule1[i]
            
            elif rule1[i] == "*" and not rule0Tuple[0] == "*": # or the other way around
                ruleIntersection[i] = rule0Tuple[0][i]

            else:
                return None
                
        if self.ruleAlreadyExists(ruleIntersection) or rule1[0:len(rule1)-1] == ruleIntersection[0:len(rule1)-1]:
            return None
        return ruleIntersection
    
    def generateCodeword(self, length):
        codeword = ""
        for _ in range(length):
            codeword += str(random.randint(0,1))
        return codeword
    
    def writeCodewords(self):
        
        file = open("codewords.txt","w") 
        for rule in self.previousRuleTuple:
            file.write(str(rule[0]) + " " + rule[1] + "\n")

        file.close() 
    
    def getRuleTuple(self):
        
        output = ""
        for rule in self.previousRuleTuple:
            output += (str(rule[0]) + " " + rule[1] + "\n")
            
        # logging.debug(output)
        return output
    
    def setSeed(self, seed):
        random.seed(seed)
        
    def getCodeword(self, packet):
        i = 0
        packetCodeword = ""
        for tree in self.treeList:
            exists, subCodeword = tree.getCodeword(packet[i])
            if not exists:
                warnings.warn("Error there is no codeword for the packet, will then use wildcard route")
                defualtRoute = ""
                for tree in self.treeList:
                    exists, subCodeword= tree.getCodeword("*")
                    if not exists:
                        raise Exception("Error there is no wildcard route")
                    defualtRoute += subCodeword
                logging.debug("Using default route")
                logging.debug("the codeword for defaultroute"+ str(defualtRoute))
                return defualtRoute
            
            packetCodeword += subCodeword
            i += 1
            
        return packetCodeword
    