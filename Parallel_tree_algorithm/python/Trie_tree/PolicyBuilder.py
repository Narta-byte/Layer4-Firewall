import random
import logging


class PolicyBuilder:
    def __init__(self,treeList):
        self.treeList = treeList
        self.ruleLength = len(treeList)+1
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        self.codewordLength = 16
        self.nextCodeword = 0
        
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
        if self.ruleAlreadyExists(rule) or self.ruleIsSubset(rule):
            logging.debug("Discarded rule bc it exits or is subset: " +str(rule))
            return
       
        ruleCodeword = self.insertRuleIntoTree(rule, self.treeList)

        # if there are no previous rules, add the new rule to the list
        if self.previousRuleTuple == []:
            self.previousRuleTuple.append((rule, ruleCodeword))
            return
        
        for oldRuleTuble in self.previousRuleTuple:
            rulePermutations = self.permutations(oldRuleTuble, rule)
            if rulePermutations is None:
                continue
            logging.debug('ruleIntersection before filter of rule: ' +str(rule) )

            rulePermutations = self.filterPermutations(rulePermutations, rule)

            logging.debug('ruleIntersection after filter:')
            for segment in rulePermutations:
                logging.debug(str(segment))

            for outputRule in rulePermutations:
                intersectionCodeword = ""
                for i, tree in enumerate(self.treeList):
                    exsits, tempCodeword = tree.getCodeword(outputRule[i])
                    if not exsits:
                        intersectionCodeword += self.generateCodeword(self.codewordLength)
                    intersectionCodeword += tempCodeword
                logging.debug("adding rule: " + str(outputRule) + " " + str(intersectionCodeword) + " " + str(ruleCodeword))
                self.previousRuleTuple.append((outputRule, intersectionCodeword))

        self.previousRuleTuple.append((rule, ruleCodeword))

       
    def permutations(self,rule0Tuple,rule1):
        output = []
        def permutationsHelper(oldRule, newRule, workingList):
            if len(workingList) == self.ruleLength-1:
                
                workingList.append(rule0Tuple[0][self.ruleLength-1])
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

            else:
                logging.debug("els: " +str(permutation))
                if self.ruleIsSubset(permutation) and \
                    (insertedRule[0] == '*' or insertedRule[0] == permutation[0]) and \
                    (insertedRule[1] == '*' or insertedRule[1] == permutation[1]) and \
                    (insertedRule[2] == '*' or insertedRule[2] == permutation[2]):
                    logging.debug("we in both" + str(permutation) + " ins:" + str(insertedRule))

                    output.append(permutation)
                    continue

                if self.ruleIsSubset(permutation):
                    logging.debug("Even tho subset, also a subset of the current inserted rule, so that takes over")
                    logging.debug("sub of" + str(permutation) + " ins:" + str(insertedRule))

                    output.append(permutation)
                    continue
                
                if (insertedRule[0] == '*' or insertedRule[0] == permutation[0]) and \
                        (insertedRule[1] == '*' or insertedRule[1] == permutation[1]) and \
                        (insertedRule[2] == '*' or insertedRule[2] == permutation[2]):
                        logging.debug("is super of" + str(permutation) + " " + str(insertedRule) )
                        permutation[self.ruleLength-1] = insertedRule[3]
                        output.append(permutation)
                        continue

        output = [list(x) for x in set(tuple(x) for x in output)] #Delete duplicates
        logging.debug("Output geben: " + str(output))

        return output
            
    def generateCodeword(self, length):
        self.nextCodeword+=1
        codeword = ""
        codeword += format(self.nextCodeword, str(length) + 'b')
        return codeword
    
    def ruleIsSubset(self,rule):
        for previousRule in self.previousRuleTuple:
            if (previousRule[0][0] == '*' or previousRule[0][0] == rule[0]) and \
               (previousRule[0][1] == '*' or previousRule[0][1] == rule[1]) and \
               (previousRule[0][2] == '*' or previousRule[0][2] == rule[2]):
                
                rule[3] = previousRule[0][3]
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
        codeword = ""
        logging.debug("Packet: " + str(packet))

        for i, packet_value in enumerate(packet):
            exists, codewordSegment = self.treeList[i].getCodeword(packet_value)
            logging.debug(f"packet[{i}] = {packet_value} Exists{i}: {exists} subcode{i}: {codewordSegment} ")
            if exists or codewordSegment != "":
                codeword += codewordSegment
            else: 
                return None
        return codeword
