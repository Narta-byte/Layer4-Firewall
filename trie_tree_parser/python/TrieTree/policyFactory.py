
import random
import logging
import warnings
# import trie_tree_parser.python.TrieTree.rangeTree as rangetree


class PolicyFactory:
    def __init__(self,treeList):
        self.treeList = treeList
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        self.codewordLength = 8
    def insertRuleIntoTree(self,rule,tree):
        i = 0
        ruleCodeword = ""
        for tree in self.treeList:
            exists, codeword = tree.getCodeword(rule[i])
            if not exists: 
                codeword = self.generateCodeword(self.codewordLength)
            
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
            file.write(str(rule[0]) + " : " + rule[1] + "\n")

        file.close() 
    
    def getRuleTuple(self):
        
        output = ""
        for rule in self.previousRuleTuple:
            output += (str(rule[0]) + " " + rule[1] + "\n")
            
        # logging.debug(output)
        return output
    
    def setSeed(self, seed):
        random.seed(seed)
        
    def getCodewordPolicyFactory(self, packet):
        i = 0
        packetCodeword = ""
        for tree in self.treeList:
            exists, subCodeword = tree.getCodeword(packet[i])
            if not exists:
                exists, subCodeword = tree.getCodeword("*")
                if not exists:
                    raise Exception("Error there is no wildcard route")
                
            
            packetCodeword += subCodeword
            i += 1

        return packetCodeword
    
    def ruleAlreadyExistsPacket(self, rule):
    # if the rules fields are equal skip the iteration and let the old rule have precedence
        for oldRuleTuple in self.previousRuleTuple:
            if oldRuleTuple[0][0:len(rule)] == rule[0:len(rule)]:
                logging.debug("Original: " + str(oldRuleTuple[0][0:len(rule)]) + " == " + str(rule[0:len(rule)]))
                return True
        return False


    def ruleAlreadyExists00Star(self, rule): #Equal rules at  0 0 *
        return self.ruleAlreadyExistsPacket([rule[0], rule[1], '*'])


    def ruleAlreadyExists0Star0(self, rule): # Rules with 0 * 0
        return self.ruleAlreadyExistsPacket([rule[0], '*', rule[2]])


    def ruleAlreadyExists0StarStar(self, rule): #Equal rules at 0 * *
        return self.ruleAlreadyExistsPacket([rule[0], '*', '*'])


    def ruleAlreadyExistsStar00(self, rule): #Equal rules at * 0 0
        return self.ruleAlreadyExistsPacket(['*', rule[1], rule[2]])


    def ruleAlreadyExistsStar0Star(self, rule): #Equal rules at * 0 *
        return self.ruleAlreadyExistsPacket(['*', rule[1], '*'])


    def ruleAlreadyExistsStarStar0(self, rule): #Equal rules at * * 0
        return self.ruleAlreadyExistsPacket(['*', '*', rule[2]])


    def ELSEDEFAULT(self, rule):
        return self.ruleAlreadyExistsPacket(['*', '*', '*'])


    def getCodewordtest(self, packet):
        codeWordList = []
        subCodeword = []
        packetCodeword = ""
        logging.debug("Packet: " + str(packet))

        for i, packet_value in enumerate(packet):
            exists, sub_codeword = self.treeList[i].getCodeword(packet_value)
            subCodeword.append(sub_codeword)
            logging.debug(f"packet[{i}] = {packet_value} Exists{i}: {exists} subcodew{i}: {sub_codeword}")

        if self.ruleAlreadyExistsPacket(packet):
            packetCodeword += subCodeword[0]
            packetCodeword += subCodeword[1]
            packetCodeword += subCodeword[2]

            codeWordList.append(packetCodeword)
            packetCodeword = ""
                #return packetCodeword

        if self.ruleAlreadyExistsStar0Star(packet): #5 Over 6
            packetCodeword += self.treeList[0].getCodeword("*")[1]
            packetCodeword += subCodeword[1]
            packetCodeword += self.treeList[2].getCodeword("*")[1]

            logging.debug("PacketCodeword *0*: " + str(packetCodeword))
            codeWordList.append(packetCodeword)
            packetCodeword = ""
            #return packetCodeword

        if self.ruleAlreadyExists0Star0(packet): # 2 0*0   conflict with 6
            packetCodeword += subCodeword[0]
            packetCodeword += self.treeList[1].getCodeword("*")[1]
            packetCodeword += subCodeword[2]

            logging.debug("PacketCodeword 0 * 0: " + str(packetCodeword))
            codeWordList.append(packetCodeword)
            logging.debug("Listen: " + str(codeWordList))
            packetCodeword = ""
            #return packetCodeword

        if self.ruleAlreadyExistsStarStar0(packet): # 6 confilct with 2
            packetCodeword += self.treeList[0].getCodeword("*")[1]
            packetCodeword += self.treeList[1].getCodeword("*")[1]
            packetCodeword += subCodeword[2]

            logging.debug("PacketCodeword so far: " + str(packetCodeword))
            codeWordList.append(packetCodeword)
            packetCodeword = ""
            #return packetCodeword
            

        if self.ruleAlreadyExists00Star(packet):
            packetCodeword += subCodeword[0]
            packetCodeword += subCodeword[1]
            packetCodeword += self.treeList[2].getCodeword("*")[1]

            logging.debug("PacketCodeword 00*: " + str(packetCodeword))
            codeWordList.append(packetCodeword)
            packetCodeword = ""
                #return packetCodeword

        
        if self.ruleAlreadyExists0StarStar(packet):
            packetCodeword += subCodeword[0]
            packetCodeword += self.treeList[1].getCodeword("*")[1]
            packetCodeword += self.treeList[2].getCodeword("*")[1]

            logging.debug("PacketCodeword for 0**: " + str(packetCodeword))
            codeWordList.append(packetCodeword)
            packetCodeword = ""
            #return packetCodeword 

        if self.ruleAlreadyExistsStar00(packet):  #6
            packetCodeword += self.treeList[0].getCodeword("*")[1]
            packetCodeword += subCodeword[1]
            packetCodeword += subCodeword[2]
            logging.debug("PacketCodeword for *00: " + str(packetCodeword))
            codeWordList.append(packetCodeword)
            packetCodeword = ""
            #return packetCodeword

        if self.ELSEDEFAULT(packet):
            ishere, subCodeword00= self.treeList[0].getCodeword("*")
            if not ishere:
                raise Exception("Error there is no wildcard route for tree0")
            packetCodeword += subCodeword00
            ishere, subCodeword11= self.treeList[1].getCodeword("*")
            if not ishere:
                raise Exception("Error there is no wildcard route for tree1")
            packetCodeword += subCodeword11
            ishere, subCodeword22= self.treeList[2].getCodeword("*")
            if not ishere:
                raise Exception("Error there is no wildcard route for tree2")
            packetCodeword += subCodeword22
            codeWordList.append(packetCodeword)
            logging.debug("Default: " + str(packetCodeword))
            packetCodeword = ""


        logging.debug(packetCodeword)
        #codeWordList.append(packetCodeword)
        logging.debug("Listen: " + str(codeWordList))

        return codeWordList



    def getCodewordtest2(self, packet): # More readable?
        codeWordList = []
        subCodeword = []
        packetCodeword = ""
        logging.debug("Packet: " + str(packet))

        for i, packet_value in enumerate(packet):
            exists, sub_codeword = self.treeList[i].getCodeword(packet_value)
            subCodeword.append(sub_codeword)
            logging.debug(f"packet[{i}] = {packet_value} Exists{i}: {exists} subcodew{i}: {sub_codeword}")

        codeword_configs = [
            (self.ruleAlreadyExistsPacket(packet), [subCodeword[0], subCodeword[1], subCodeword[2]]),
            (self.ruleAlreadyExistsStarStar0(packet), [self.treeList[0].getCodeword("*")[1], self.treeList[1].getCodeword("*")[1], subCodeword[2]]),
            (self.ruleAlreadyExists0Star0(packet), [subCodeword[0], self.treeList[1].getCodeword("*")[1], subCodeword[2]]),
            (self.ruleAlreadyExists00Star(packet), [subCodeword[0], subCodeword[1], self.treeList[2].getCodeword("*")[1]]),
            (self.ruleAlreadyExists0StarStar(packet), [subCodeword[0], self.treeList[1].getCodeword("*")[1], self.treeList[2].getCodeword("*")[1]]),
            (self.ruleAlreadyExistsStar00(packet), [self.treeList[0].getCodeword("*")[1], subCodeword[1], subCodeword[2]]),
            (self.ruleAlreadyExistsStar0Star(packet), [self.treeList[0].getCodeword("*")[1], subCodeword[1], self.treeList[2].getCodeword("*")[1]]),
        ]

        for condition, codeword_parts in codeword_configs:
            if condition:
                packetCodeword += ''.join(codeword_parts)
                codeWordList.append(packetCodeword)
                packetCodeword = ""
                #break

        if not codeWordList:
            ishere, subCodeword00= self.treeList[0].getCodeword("*")
            if not ishere:
                raise Exception("Error there is no wildcard route for tree0")
            packetCodeword += subCodeword00
            ishere, subCodeword11= self.treeList[1].getCodeword("*")
            if not ishere:
                raise Exception("Error there is no wildcard route for tree1")
            packetCodeword += subCodeword11
            ishere, subCodeword22= self.treeList[2].getCodeword("*")
            if not ishere:
                raise Exception("Error there is no wildcard route for tree2")
            packetCodeword += subCodeword22
            codeWordList.append(packetCodeword)
            logging.debug("Default: " + str(packetCodeword))

        logging.debug("Listen: " + str(codeWordList))
        return codeWordList

"""        ###     BEST VERSION BUT DOES NOT WORK :(   ###
    def getCodewordtest3(self, packet): 
        codeWordList = []
        subCodeword = []
        packetCodeword = ""
        logging.debug("Packet: " + str(packet))
        rules = {
            'ruleAlreadyExistsPacket': [0, 1, 2],
            'ruleAlreadyExistsStar0Star': ['*', 1, '*'],
            'ruleAlreadyExists0Star0': [0, '*', 2],
            'ruleAlreadyExistsStarStar0': ['*', '*', 2],
            'ruleAlreadyExists00Star': [0, 1, '*'],
            'ruleAlreadyExists0StarStar': [0, '*', '*'],
            'ruleAlreadyExistsStar00': ['*', 1, 2],
            'ELSEDEFAULT': ['*', '*', '*']
        }

        for i, packet_value in enumerate(packet):
            exists, sub_codeword = self.treeList[i].getCodeword(packet_value)
            subCodeword.append(sub_codeword)
            logging.debug(f"packet[{i}] = {packet_value} Exists{i}: {exists} subcodew{i}: {sub_codeword}")

        for rule, values in rules.items():
            if getattr(self, rule)(packet):
                for value in values:
                    if value == '*':
                        packetCodeword += self.treeList[values.index(value)].getCodeword("*")[1]
                    else:
                        packetCodeword += subCodeword[value]
                codeWordList.append(packetCodeword)
                logging.debug(f"PacketCodeword {rule}: {str(packetCodeword)}")
                packetCodeword = ""
                break

        logging.debug(packetCodeword)
        logging.debug("Listen: " + str(codeWordList))
        return codeWordList
 """