import random
import logging
import time

class PolicyBuilder:
    def __init__(self,treeList):
        self.treeList = treeList
        self.ruleLength = len(treeList)+1
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        self.codewordLength= 16
        self.nextCodeword = 0
        self.treeDepth = 16
        self.previousRulePrefixes = set()  # Add this line to store previous rule prefixes

        
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
        # prefix = rule[:self.ruleLength-1]
        # for oldRuleTuple in self.previousRuleTuple:
        #     if oldRuleTuple[0][:self.ruleLength-1] == prefix:
        #         return True
        # return False
        prefix = tuple(rule[:self.ruleLength - 1])
        return prefix in self.previousRulePrefixes



    def createIntersectionCodeword(self, output_rule):
        intersection_codeword = ""
        for i, tree in enumerate(self.treeList):
            exists, temp_codeword = tree.getCodeword(output_rule[i])
            if not exists:
                intersection_codeword += self.generateCodeword(self.codewordLength)
            intersection_codeword += temp_codeword
        return intersection_codeword

        
    def insertRule(self, rule):
        if self.ruleIsSubset(rule): #or self.ruleAlreadyExists(rule): Already exists is checked for in filterperm
            return

        rule_codeword = self.insertRuleIntoTree(rule, self.treeList)

        if not self.previousRuleTuple:
            self.previousRuleTuple.append((rule, rule_codeword))
            self.previousRulePrefixes.add(tuple(rule[:self.ruleLength - 1]))

            return

        for old_rule_tuple in self.previousRuleTuple:
            rule_permutations = self.permutations(old_rule_tuple, rule)
            if rule_permutations is None:
                continue

            rule_permutations = self.filterPermutations(rule_permutations, rule)

            for output_rule in rule_permutations:
                intersection_codeword = self.createIntersectionCodeword(output_rule)
                self.previousRuleTuple.append((output_rule, intersection_codeword))
                self.previousRulePrefixes.add(tuple(output_rule[:self.ruleLength - 1]))

        self.previousRuleTuple.append((rule, rule_codeword))
        self.previousRulePrefixes.add(tuple(rule[:self.ruleLength - 1]))
       
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
            if insertedRule[0:self.ruleLength-1] == permutation[0:self.ruleLength-1]:
                logging.debug("if2: " +str(permutation))
                continue

            elif self.ruleAlreadyExists(permutation) or output.__contains__(permutation):
                logging.debug("if1: " +str(permutation))
                continue

            else:
                logging.debug("els: " +str(permutation))

                if self.ruleIsSubset(permutation): #Subset of previous rules
                    logging.debug("Even tho  rule0, also a  rule0 of the current inserted rule, so that takes over")
                    logging.debug("sub of" + str(permutation) + " ins:" + str(insertedRule))

                    output.append(permutation)
                    continue
                
                if self.subset(permutation, insertedRule): #subset of curr inserted rule
                    logging.debug("is super of" + str(permutation) + " " + str(insertedRule) )
                    permutation[self.ruleLength-1] = insertedRule[len(self.treeList)]
                    output.append(permutation)
                    continue

                if all(x == '*' for x in permutation[:-1]):
                    continue

        output = [list(x) for x in set(tuple(x) for x in output)] #Delete duplicates
        logging.debug("Output geben: " + str(output))
        return output

    def ruleIsSubset(self,rule):
        for previousRule in self.previousRuleTuple:
            if self.subset(rule, previousRule[0]):
                rule[self.ruleLength-1] = previousRule[0][self.ruleLength-1]
                return True
        return False
        
    def subset(self, currRule, previousRule):
        if all(prev == '*' or prev == curr for prev, curr in zip(previousRule, currRule)):
            return True
        return self.matches(previousRule, currRule)

    def matches(self, thisRule, currRule):
        if thisRule[:len(thisRule)-1] == currRule:
            return True

        for prevRuleField, currRuleField in zip(thisRule[:-1], currRule):
            if prevRuleField == currRuleField:
                continue
            elif prevRuleField == "*":
                continue
            elif self.lpm(prevRuleField, currRuleField):
                continue
            else:
                return False
        return True


    def lpm(self, this_rule, curr_rule):
        if '*' in (this_rule, curr_rule):
            return False
    
        def get_lpm(rule):
            return rule.split('*')[0] if '*' in rule else bin(int(rule))[2:].zfill(self.treeDepth)
    
        lpm_this_rule = get_lpm(this_rule)
        lpm_curr_rule = get_lpm(curr_rule)
    
        if len(lpm_curr_rule) < len(lpm_this_rule):
            return False
    
        return all(this == curr for this, curr in zip(lpm_this_rule, lpm_curr_rule))



        

    def retriveCodeword(self, packet):
        codeword = ""
        logging.debug("Packet: " + str(packet))

        for i, packet_value in enumerate(packet):
            exists, codewordSegment = self.treeList[i].getCodeword(packet_value)
            logging.debug(f"packet[{i}] = {packet_value} Exists{i}: {exists} subcode{i}: {codewordSegment} ")
            if exists or codewordSegment != "":
                codeword += str(codewordSegment)
            else: 
                return None
        return codeword

    def generateCodeword(self, length):
        self.nextCodeword += 1
        return format(self.nextCodeword, f"0{length}b")

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
        
