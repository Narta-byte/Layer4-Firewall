import logging


class ListFirewall:
    def __init__(self):
        self.rules = []
        self.treeDepth = 16
        self.codewordLength = 4
    def insertRule(self, rule):
        rule = [element[:-1] if (len(element) == self.codewordLength + 1 and element[-1] == "*" and element[:-1].isdigit())
        else element for element in rule]
        self.rules.append(rule)
        
    def lookup(self, inputPacket):
        for thisRule in self.rules:
            if self.matches(thisRule, inputPacket):
                logging.debug("Packet matched w rule: "+str(thisRule)+"  Packet: " + str(inputPacket))
                return thisRule[len(thisRule)-1]
        return "No Match"
    
    def matches(self, thisRule, inputPacket):
        if thisRule[:len(thisRule)-1] == inputPacket:
            return True
        for i in range(len(thisRule)-1):
            if thisRule[i] == inputPacket[i]:
                continue
            elif thisRule[i] == "*":
                continue 
            elif self.lpm(thisRule[i], inputPacket[i]):
               continue
            else:
                return False
        logging.debug("thisRule: "+str(thisRule))
        logging.debug("inputPacket: "+str(inputPacket))
        return True

    def lpm(self, thisRule, inputPacket):
        if len(thisRule.split('*')) < 2:
            return False
        inputPacketToBin = format(int(inputPacket), "0" + str(self.treeDepth) + 'b') ###

        for j in range(int(thisRule.split('*')[0])):
            if thisRule[j] == "*":
                return True
            if thisRule[j] != inputPacketToBin[j]:
                return False
        return True
                      
    def getRules(self):
        output = ""
        for rule in self.rules:
            output += str(rule) + "\n"
        return output