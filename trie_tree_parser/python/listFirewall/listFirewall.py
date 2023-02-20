

class ListFirewall:
    def __init__(self):
        self.rules = []

    def insert(self, rule):
        self.rules.append(rule)
        
    def lookup(self, inputPacket):
        for thisRule in self.rules:
            if self.matches(thisRule, inputPacket):
                return thisRule[len(thisRule)-1]
        return "No Match"
    
    def matches(self, thisRule, inputPacket):
        if thisRule == inputPacket:
            return True
        for i in range(len(thisRule)-1):
            if thisRule[i] == inputPacket[i]: 
                continue
            elif thisRule[i] == "*" or inputPacket[i] == "*":   
                continue 
            else:
                return False
        return True
    
    def insertRange(self, rule):
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
            #str_sublist = str(sublist).replace("'", "\"")
            #logging.debug(sublist)
            self.insert(sublist)
    
    def getRules(self):
        output = ""
        for rule in self.rules:
            output += str(rule) + "\n"
        return output