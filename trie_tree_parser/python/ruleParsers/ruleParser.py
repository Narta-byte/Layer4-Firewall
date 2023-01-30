# %%

# from trie_tree_parser.python.parsers.rule import Rule
class Rule:
    def __init__(self,protocol, srcIp, srcPort, dstIp, dstPort, rule):
        self.protocol = protocol
        self.srcIp = srcIp
        self.srcPort = srcPort
        self.dstIp = dstIp
        self.dstPort = dstPort
        self.rule = rule


class RuleParser:
    def __init__(self):
        self.ruleList = []
    def parse(self,path):
        self.fileHandler = open(path)
        lines = self.fileHandler.readlines()
        for line in lines:
            if line[0] == "#": 
                continue
            fields = line.split()
            rule = Rule(fields[0],fields[1],fields[2],fields[3],fields[4],fields[5])
            self.ruleList.append(rule)
    def toString(self):
        output="------------------------\n"
        i = 0
        for rule in self.ruleList:
            output += "Rule #"+str(i)+"\n"
            output += "  -Protocol : "+rule.protocol + "\n"
            output += "  -srcIp : "+rule.srcIp + " | "
            output += "srcPort : "+rule.srcPort + "\n"
            output += "  -dstIp : "+rule.dstIp + " | "
            output += "dstPort : "+rule.dstPort + "\n"
            output += "  -rule : "+rule.rule + "\n"
            i+=1
        return output
    
            
folderPath = "..\\..\\rules"
file = "\\singleRule.rule"
parser = RuleParser()
parser.parse(folderPath+file)
print(parser.toString())
        

# %%
