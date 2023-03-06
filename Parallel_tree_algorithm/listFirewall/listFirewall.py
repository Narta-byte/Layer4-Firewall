

class ListFirewall:
    def __init__(self):
        self.rules = []

    def insert(self, rule):
        self.rules.append(rule)
        
    def lookup(self, inputRule):
        for thisRule in self.rules:
            if self.matches(thisRule, inputRule):
                return thisRule
        return None
    
    def matches(self, thisRule, inputRule):
        if thisRule == inputRule:
            return True
        for i in range(len(thisRule)):
            if thisRule[i] == inputRule[i]: 
                continue
            elif thisRule[i] == "*" or inputRule[i] == "*":   
                continue 
            else:
                return False
            logging.debug("thisRule: "+str(thisRule))
            logging.debug("inputPacket: "+str(inputPacket))
        return True