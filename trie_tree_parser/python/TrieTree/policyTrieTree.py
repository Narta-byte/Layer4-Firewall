# %%
import sys

# sys.path.append('C:\\Users\\Mig\\Desktop\\Bachelor\\Layer4-Firewall\trie_tree_parser\\python\\ruleParsers')
# print(sys.path)
import protocolTrieTree
from trie_tree_parser.python.TrieTree.ruleParser.ruleParser import RuleParser
# from ruleParser.ruleParser import ruleParser



if __name__ == "__main__":
    ruleParser = RuleParser.RuleParser()
    
    dict0 = protocolTrieTree.ProtocolTrieTree()
    dict0.insert("TCP")
    
# %%
