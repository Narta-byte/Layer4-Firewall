# %%
import trieTree

class ProtocolTrieTree(trieTree.TrieTree):
    def insert(self, key):
        length = 1
        crawl = self.root
        for level in range(length):
            child = crawl.children
            ch = key
            if ch in child:
                crawl = child[ch]
            else:
                temp = trieTree.TrieNode(ch)
                child[ch] = temp
                crawl = temp
        crawl.isEnd = True
        
if __name__ == '__main__':
    dict = ProtocolTrieTree()
    dict.insert("TCP")
    dict.insert("UDP")
    dict.insert("TCP")
    
    dict.drawGraph(html=True)
# %%
