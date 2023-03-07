# %%
if __name__ != '__main__':
    import Parallel_tree_algorithm.python.Trie_tree.ruleParser.rule as rule

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
            newRule = rule.Rule(fields[0],fields[1],fields[2],fields[3],fields[4],fields[5])
            self.ruleList.append(newRule)
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
    
    
if __name__ == '__main__':
    import rule
    folderPath = "..\\..\\..\\rules"
    # folderPath = "trie_tree_parser\\rules"
    file = "\\singleRule.rule"
    import os
    print(os.getcwd())
    parser = RuleParser()
    parser.parse(folderPath+file)
    print(parser.toString())
        

# %%
