#%%
from TrieTree import Trie
dict = Trie()
dict.insert("192.168.1.1","PERMIT")
dict.insert("192.168.1","DENY")
dict.insert("222.168.1.1","DENY")
# dict.insert("1","DENY", binaryInput = True)
# dict.insert("11","DENY", binaryInput = True)
# dict.insert("10","PERMIT", binaryInput = True)
# dict.insert("2","PERMIT")
# dict.insert("64","PERMIT")
dict.drawGraph(html = True)
# %%
