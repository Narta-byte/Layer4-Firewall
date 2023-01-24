#%%
from TrieTree import Trie
dict = Trie()
dict.insert("192.168.1.1","PERMIT")
arg = "192.168.1.1"
print(dict.match(arg))
arg = "192.168.3.1/24"
dict.insert(arg,"DENY")
arg = "192.168.3.1"
dict.insert(arg,"PERMIT")
# print(dict.match("192.168.3.1"))
print(dict.match("192.168.3.2"))

dict.drawGraph(html = True)
# %%
