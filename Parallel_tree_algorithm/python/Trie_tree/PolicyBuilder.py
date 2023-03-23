import random
import logging


class PolicyBuilder:
    def __init__(self,treeList):
        self.treeList = treeList
        self.ruleLength = len(treeList)+1
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        self.codewordLength = 16
    
    def insertRuleIntoTree(self, rule, tree):
        ruleCodeword = ""
        for i, tree in enumerate(self.treeList):
            exists, codeword = tree.getCodeword(rule[i])
            if not exists:
                codeword = self.generateCodeword(self.codewordLength)
            logging.debug(f'codeword: {codeword} rule: {rule[i]} exists: {exists} ')
            ruleCodeword += codeword
            tree.insert(rule[i], codeword)
        return ruleCodeword
    
    def ruleAlreadyExists(self,rule):
        # if the rules fields are equal skip the iteration and let the old rule have precedence
        # logging.debug(f'AlreadyExists oldRuleTuple: {self.previousRuleTuple} rule: {rule}')
        for oldRuleTuple in self.previousRuleTuple:
            if oldRuleTuple[0][0:self.ruleLength-1] == rule[0:self.ruleLength-1]:
                return True
        return False

    
    def insertRule(self,rule): 
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
            self.insertRuleHelper(sublist)

    def insertRuleHelper(self,rule):
        
        if self.ruleAlreadyExists(rule) or self.ruleIsSubset(rule):
            logging.debug("Threw out the rule just cause: " +str(rule))
            return
       
        ruleCodeword = self.insertRuleIntoTree(rule, self.treeList)

        # if there are no previous rules, add the new rule to the list
        if self.previousRuleTuple == []:
            self.previousRuleTuple.append([rule, ruleCodeword])
            return
        
        for oldRuleTuble in self.previousRuleTuple:
            rulePermutations = []
        
            rulePermutations = self.permutations(oldRuleTuble, rule)
            if rulePermutations is None:
                continue
            logging.debug('ruleIntersection before filter of rule: ' +str(rule) )
            #for segment in rulePermutations:
             #   logging.debug(str(segment))

            rulePermutations = self.filterPermutations(rulePermutations, rule)

            logging.debug('ruleIntersection after filter:')
            for segment in rulePermutations:
                logging.debug(str(segment) )

            for outputRule in rulePermutations:
                intersectionCodeword = ""
                for i, tree in enumerate(self.treeList):
                    exsits, tempCodeword = tree.getCodeword(outputRule[i])
                    if not exsits:
                        intersectionCodeword += self.generateCodeword(self.codewordLength)
                    intersectionCodeword += tempCodeword
                logging.debug("adding rule: " + str(outputRule) + " " + str(intersectionCodeword) + " " + str(ruleCodeword))
                self.previousRuleTuple.append([outputRule, intersectionCodeword])
                # self.insertRuleHelper(outputRule)
                # logging.debug("previousRuleTuple: " + str(self.previousRuleTuple))
        self.previousRuleTuple.append([rule, ruleCodeword])
       
    def permutations(self,rule0Tuple,rule1):
        output = []
        def permutationsHelper(oldRule, newRule, workingList):
            if len(workingList) == self.ruleLength-1:
                
                workingList.append(rule0Tuple[0][self.ruleLength-1])
                #workingList.append(rule0Tuple[0][rule1[3]])
                #workingList[-1] = rule1[-1]
                #logging.debug("This is rule1: " + str(rule1))
                #logging.debug("What is rule? With old rule with new bone: " + str(workingList[-1]))
                output.append(workingList)
                return
                
            idx = len(workingList)
            newWorkingList = workingList.copy()
            workingList.append(newRule[idx])
            newWorkingList.append(oldRule[idx])
            permutationsHelper(oldRule, newRule, workingList)
            permutationsHelper(oldRule, newRule, newWorkingList)
         
        permutationsHelper(rule0Tuple[0], rule1, [])
        logging.debug(f'output from perms: {output} rule0: {rule0Tuple[0]} rule1: {rule1} ')
        return output

    def filterPermutations(self,rulePermutations, insertedRule):
        output = []
        for permutation in rulePermutations:
            if self.ruleAlreadyExists(permutation) or output.__contains__(permutation):
                logging.debug("if1: " +str(permutation))
                continue
            elif insertedRule[0:self.ruleLength-1] == permutation[0:self.ruleLength-1]:
                logging.debug("if2: " +str(permutation))
                continue
            elif permutation[0:self.ruleLength-1] == ["*", "*", "*"]: 
                logging.debug("if4: " +str(permutation))
                continue
            
        #    elif not self.ruleIsSubset(permutation):
        #        logging.debug("if3: " +str(permutation))
        #        continue
            else:
                logging.debug("els: " +str(permutation))
                if self.ruleIsSubset(permutation) and \
                    (insertedRule[0] == '*' or insertedRule[0] == permutation[0]) and \
                    (insertedRule[1] == '*' or insertedRule[1] == permutation[1]) and \
                    (insertedRule[2] == '*' or insertedRule[2] == permutation[2]):
                    logging.debug("we in both" + str(permutation) + " ins:" + str(insertedRule))
                    #permutation[self.ruleLength-1] = insertedRule[3] ## Skal være lig den øverste beslutning!
                    output.append(permutation)
                    continue
                    #return output


                if self.ruleIsSubset(permutation):
                    # if (insertedRule[0] == '*' or insertedRule[0] == permutation[0]) and \
                    #     (insertedRule[1] == '*' or insertedRule[1] == permutation[1]) and \
                    #     (insertedRule[2] == '*' or insertedRule[2] == permutation[2]):
                    logging.debug("Even tho subset, also a subset of the current inserted rule, so that takes over")
                    #permutation[self.ruleLength-1] = insertedRule[3]
                    logging.debug("sub of" + str(permutation) + " ins:" + str(insertedRule))
                    output.append(permutation)
                    continue
                    #return output
                
                #Inserted subset
                if (insertedRule[0] == '*' or insertedRule[0] == permutation[0]) and \
                        (insertedRule[1] == '*' or insertedRule[1] == permutation[1]) and \
                        (insertedRule[2] == '*' or insertedRule[2] == permutation[2]):
                        logging.debug("is super of" + str(permutation) + " " + str(insertedRule) )
                        permutation[self.ruleLength-1] = insertedRule[3]
                        output.append(permutation)
                        continue
                        #return output


        output = [list(x) for x in set(tuple(x) for x in output)] #Delete duplicates
        logging.debug("Output geben: " + str(output))

        return output
            
    def generateCodeword(self, length):
        codeword = ""
        for _ in range(length):
            codeword += str(random.randint(0,1))
        return codeword
    
    def ruleIsSubset(self,rule):
        for previousRule in self.previousRuleTuple:
            if (previousRule[0][0] == '*' or previousRule[0][0] == rule[0]) and \
               (previousRule[0][1] == '*' or previousRule[0][1] == rule[1]) and \
               (previousRule[0][2] == '*' or previousRule[0][2] == rule[2]):
                rule[3] = previousRule[0][3]
                return True
        return False
    def isSubsetOf(self,rule):
        for previousRule in self.previousRuleTuple:
            if (previousRule[0][0] == '*' or previousRule[0][0] == rule[0]) and \
               (previousRule[0][1] == '*' or previousRule[0][1] == rule[1]) and \
               (previousRule[0][2] == '*' or previousRule[0][2] == rule[2]):
                return previousRule[0]
        return []
    def ruleIsSuperset(self,rule):
        for previousRule in self.previousRuleTuple:
            if (previousRule[0][0] == rule[0] or rule[0] == '*') and \
               (previousRule[0][1] == rule[1] or rule[1] == '*') and \
               (previousRule[0][2] == rule[2] or rule[2] == '*'):
                logging.debug("ruleIsSuperset: " + str(previousRule[0]) + " " + str(rule))
                return True
        return False
    def IsSuperset(self, oldRule, newRule):
       
        if (oldRule[0] == newRule[0] or newRule[0] == '*') and \
          (oldRule[1] == newRule[1] or newRule[1] == '*') and \
          (oldRule[2] == newRule[2] or newRule[2] == '*'):
           return True
        return False
    def isSubset(self, oldRule, newRule):
        if (oldRule[0] == '*' or oldRule[0] == newRule[0]) and \
           (oldRule[1] == '*' or oldRule[1] == newRule[1]) and \
           (oldRule[2] == '*' or oldRule[2] == newRule[2]):
            return True
        return False
    def isDifferent(self, oldRule, newRule):
        if (oldRule[0] != newRule[0] and (newRule[0] != '*' or oldRule[0] != '*')) and \
           (oldRule[1] != newRule[1] and (newRule[1] != '*' or oldRule[1] != '*')) and \
           (oldRule[2] != newRule[2] and (newRule[2] != '*' or oldRule[2] != '*')):
            return True
        return False
    def writeCodewords(self):   #Writing to "codewords.txt"
        file = open("codewords.txt", "w")
        for rule in self.previousRuleTuple:
            file.write(str(rule[0]) + " " + rule[1] +  "\n")
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
            
            if exists or codewordSegment != "":
                codeword.append(codewordSegment)
            
            else: 
                # exists, codewordSegment = self.treeList[i].getCodeword("*")
                logging.debug("WHY IS THIS HAPPENING")
                return None
                # if not exists:
                    # raise Exception("Error there is no wildcard route for tree " + str(i))
                codeword.append(codewordSegment)
        
        possibleCodewords = []
        debugPosCodewords = []
        cursedTruthTable = []
        
        tempCodeword = []
        tempPacket = []
        self.AppendTemp(packet, codeword, 1, tempCodeword, tempPacket, 0)
        self.AppendTemp(packet, codeword, 1, tempCodeword, tempPacket, 1)
        self.AppendTemp(packet, codeword, 1, tempCodeword, tempPacket, 2)

        possibleCodewords.append(tempCodeword)
        
        
        answerList = []
        for possibleCodeword in possibleCodewords:
            answer = ""
            logging.debug("Possible codeword: " + str(possibleCodeword))
            for i in range(self.ruleLength - 1):
                answer += possibleCodeword[i]
            answerList.append(answer)
        logging.debug("Answer list: " + str(answerList))
        logging.debug("Answer: the length " + str(len(answerList)))
        
        return answerList[-1]

    def ruleAlreadyExistsPacket(self, rule): #Does the inc. packet exist in previoustuple
    # if the rules fields are equal skip the iteration and let the old rule have precedence
        for oldRuleTuple in self.previousRuleTuple:
            if oldRuleTuple[0][0:len(rule)] == rule[0:len(rule)]:
                logging.debug("Matching in codewords with packet:" + str(oldRuleTuple[0][0:len(rule)]))
                return True
        return False
        
    def AppendTemp(self, packet, codeword, x, tempCodeword, tempPacket, cnt):
        if x:
            tempCodeword.append((codeword[cnt]))
            tempPacket.append(packet[cnt])
        else:
            _, codeword = self.treeList[cnt].getCodeword("*")
            tempCodeword.append((codeword))
            tempPacket.append("*")

pb = PolicyBuilder([])
pb.previousRuleTuple= [ (['*', '5', '2', 'beta'],123), (['*', '*', '2', 'alpha'],12345)]
print(pb.ruleIsSubset(['*', '3', '2', 'beta']))
print(pb.IsSuperset(['*', '5', '0', 'beta'],['*', '5', '*', 'beta']))


print(pb.isDifferent(['*', '*', '0', 'alpha'],['*', '*', '2', 'beta']))