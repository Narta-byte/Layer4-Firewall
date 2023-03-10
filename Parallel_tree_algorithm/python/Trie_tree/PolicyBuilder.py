import random
import logging


class PolicyBuilder:
    def __init__(self,treeList):
        self.treeList = treeList
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        self.codewordLength = 16
    def insertRuleIntoTree(self, rule, tree):
        ruleCodeword = ""
        for i, tree in enumerate(self.treeList):
            exists, codeword = tree.getCodeword(rule[i])
            
            if not exists:
                codeword = self.generateCodeword(self.codewordLength)
            
            ruleCodeword += codeword
            tree.insert(rule[i], codeword)
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
        
        intersectionCodeword = self.generateCodeword(self.codewordLength*len(self.treeList))
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
        
        combinations = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    tempCombination = ["temp", "temp", "temp", "tempRule"]
                    tempCombination[3] = rule0Tuple[0][3]
                    if bool(x):
                        tempCombination[0] = rule0Tuple[0][0]
                    else:
                        tempCombination[0] = rule1[0]
                    if bool(y):
                        tempCombination[1] = rule0Tuple[0][1]
                    else:
                        tempCombination[1] = rule1[1]
                    if bool(z):
                        tempCombination[2] = rule0Tuple[0][2]
                    else:
                        tempCombination[2] = rule1[2]
                    combinations.append(tempCombination)
                    
        newComb = list(set(tuple(x) for x in combinations)) # Get only unique values in combinations
        for combination in newComb:
            logging.debug(combination)

               
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
    
    def writeCodewords(self):   #Writing to "codewords.txt"
        #file = open("codewords.txt", "w") 
        file = open("Parallel_tree_algorithm/python/Trie_tree/codewords.txt", "w")
        for rule in self.previousRuleTuple:
            file.write(str(rule[0]) + " : " + rule[1] +  "\n")
        file.close() 
    
    def getRuleTuple(self):
        output = ""
        for rule in self.previousRuleTuple:
            output += (str(rule[0]) + " " + rule[1] + "\n")
        return output
    
    def setSeed(self, seed):
        random.seed(seed)
        

    def retriveCodeword(self, packet): # More readable?
        codeword = []
        logging.debug("Packet: " + str(packet))

        for i, packet_value in enumerate(packet):
            exists, codewordSegment = self.treeList[i].getCodeword(packet_value)
            logging.debug(f"packet[{i}] = {packet_value} Exists{i}: {exists} subcode{i}: {codewordSegment} ")
            
            if exists:
                codeword.append(codewordSegment)
            else: 
                exists, codewordSegment = self.treeList[i].getCodeword("*")
                if not exists:
                    raise Exception("Error there is no wildcard route for tree " + str(i))
                codeword.append(codewordSegment)
        
        possibleCodewords = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    tempCodeword = []
                    tempPacket = []
                    self.AppendTemp(packet, codeword, x, tempCodeword, tempPacket, 0)
                    self.AppendTemp(packet, codeword, y, tempCodeword, tempPacket, 1)
                    self.AppendTemp(packet, codeword, z, tempCodeword, tempPacket, 2)
                    
                    if self.ruleAlreadyExistsPacket(tempPacket):
                        possibleCodewords.append(tempCodeword)
        logging.debug("Possible codewords: " + str(possibleCodewords))
        
        answerList = []
        for possibleCodeword in possibleCodewords:
            answer = ""
            for i in range(3):
                answer += possibleCodeword[i]
            answerList.append(answer)
        logging.debug("Answer list: " + str(answerList))
        return answerList

    def ruleAlreadyExistsPacket(self, rule): #Does the inc. packet exist in previoustuple
    # if the rules fields are equal skip the iteration and let the old rule have precedence
        for oldRuleTuple in self.previousRuleTuple:
            if oldRuleTuple[0][0:len(rule)] == rule[0:len(rule)]:
                logging.debug("Matching in codewords with packet:" + str(oldRuleTuple[0][0:len(rule)]))
                return True
        return False
        
    def AppendTemp(self, packet, codeword, x, tempCodeword, tempPacket, cnt):
        if bool(x):
            tempCodeword.append((codeword[cnt]))
            tempPacket.append(packet[cnt])
        else:
            junk, codeword = self.treeList[cnt].getCodeword("*")
            tempCodeword.append((codeword))
            tempPacket.append("*")
