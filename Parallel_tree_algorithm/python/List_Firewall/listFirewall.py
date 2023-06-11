import logging


class ListFirewall:
    def __init__(self):
        self.rules = []
        self.treeDepth = 4
        self.codewordLength = 4
    def insertRule(self, rule):
        rule = [str(int(element[:-1],2)) if (len(element) == self.codewordLength + 1 and element[-1] == "*" and element[:-1].isdigit())
        else element for element in rule]
        self.rules.append(rule)
        
    def lookup(self, inputPacket):
        for thisRule in self.rules:
            logging.debug("Lookup thisrule: " + str(thisRule))
            if self.matches(thisRule, inputPacket):
                logging.debug("Packet matched w rule: "+str(thisRule)+"  Packet: " + str(inputPacket))
                return thisRule[-1]
        return "No Match"
    
    def matches(self, thisRule, inputPacket):
        logging.debug("whole thisrule: " + str(thisRule))
        logging.debug("whole inputPack: " + str(inputPacket))
        if thisRule[:-1] == inputPacket:
            return True
        for i, _ in enumerate(thisRule[:-1]):
            if thisRule[i] == inputPacket[i]:
                continue
            elif thisRule[i] == "*":
                continue 
            elif thisRule[i][0] != '*' and thisRule[i][-1] == '*' and inputPacket[i].startswith(thisRule[i][:-1]):
               continue
            else:
                # logging.debug("return false")
                return False
        # logging.debug("matches true")
        return True

    def lpm(self, thisRule, inputPacket):
        if len(thisRule.split('*')) < 2:
            return False
        #inputPacketToBin = format(int(inputPacket), "0" + str(self.codewordLength) + 'b') ###
        #inputPacketToBin = format(int(inputPacket), "0" + str(self.codewordLength)) ###
        inputPacketToBin = bin(int(inputPacket))[2:].zfill(self.codewordLength) ###
        # logging.debug("inpitpacket: "+str(inputPacket))
        # logging.debug("thisrule: " +str(thisRule[0]))
        # logging.debug("thisrule: " +str(thisRule))
        # logging.debug("inpit converted to bin in firewall!: " + str(inputPacketToBin))
        # logging.debug(len(str(int(thisRule.split('*')[0]))))

        for i, j in enumerate(thisRule.split('*')[0]):
            j = int(j)
            # logging.debug("J in in loop: " + str(j))
            # logging.debug("I in in loop: " + str(i))
            # logging.debug(str(thisRule[j]))
            # logging.debug(inputPacketToBin[j])
            # if thisRule[i] == "*":
            #     return True
            if str(thisRule[i]) != str(inputPacketToBin[i]):
                logging.debug("finally famous")
                return False
            # if str(thisRule[i]) == '*':
            #     logging.debug("finally")
            #     return True
            # if thisRule[j] != inputPacketToBin[j]:
            #     return False
        # logging.debug("retting true")
        return True

    def getRules(self):
        output = ""
        for rule in self.rules:
            output += str(rule) + "\n"
        return output
