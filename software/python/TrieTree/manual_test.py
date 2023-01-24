#%%
from TrieTree import Trie
dict = Trie()
# dict.insert("hat")
#dict.insert("cat")
# #dict.insert("car")
# #dict.insert("cathat")
# #dict.insert("catmat")
dict.insert("192.168.1.1")
dict.insert("222.168.1.1")
# dict.insert("192.168.2.1")
dict.drawGraph(html = True)
# print(dict.getMatchingPrefix("hat"))
# dict = Trie()
# print(dict.ipv4Tobinary("192.168.1.1"))

# %%
