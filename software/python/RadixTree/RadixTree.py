# # class RadixTreeNode:
# #     def __init__(self, value=None):
# #         self.value = value
# #         self.children = {}

# #     def add_child(self, key, value=None):
# #         self.children[key] = RadixTreeNode(value)

# #     def has_child(self, key):
# #         return key in self.children

# #     def get_child(self, key):
# #         return self.children[key]

# # class RadixTree:
# #     def __init__(self):
# #         self.root = RadixTreeNode()

# #     def insert(self, string):
# #         node = self.root
# #         for char in string:
# #             if not node.has_child(char):
# #                 node.add_child(char)
# #             node = node.get_child(char)
# #         node.value = string

# #     def search(self, string):
# #         node = self.root
# #         for char in string:
# #             if not node.has_child(char):
# #                 return None
# #             node = node.get_child(char)
# #         return node.value
    

# # rad = RadixTree()
# # rad.insert("1010111")


# # input = "10101111"
# # print(input + ":   ", end="")
# # print(rad.search(input))


# # # Test code
# # rt = RadixTree()

# # # Insert some words
# # rt.insert("hello")
# # rt.insert("world")
# # rt.insert("hell")
# # rt.insert("wor")

# # # Search for a word
# # print(rt.search("hello")) # prints "hello"
# # print(rt.search("worl")) # prints None
# # print(rt.search("wor")) # prints "wor"


# # from collections import defaultdict

# # class RadixTreeNode():
# #     def __init__(self,is_word=False,keys=None):
# #         self.is_word=is_word
# #         self.children=keys if keys else defaultdict(RadixTreeNode)

# # class Trie():
# #     def __init__(self):
# #         self.root=RadixTreeNode()

# #     def insert(self, word):
# #         return self.insert_helper(self.root, word)

# #     def insert_helper(self, node, word):
# #         for key,child in node.children.items():
# #             prefix, split, rest = self.match(key, word)
# #             if not split:
# #                 #key complete match
# #                 if not rest:
# #                     #word matched
# #                     child.is_word=True
# #                     return True
# #                 else:
# #                     #match rest of word
# #                     return self.insert_helper(child, rest)
# #             if prefix:
# #                 #key partial match, need to split
# #                 new_node=RadixTreeNode(is_word=not rest,keys={split:child})
# #                 node.children[prefix]=new_node
# #                 del node.children[key]
# #                 return self.insert_helper(new_node, rest)
# #         node.children[word]=RadixTreeNode(is_word=True)

# #     def search(self, word):
# #         return self.search_helper(self.root,word)

# #     def search_helper(self,node, word):
# #         for key,child in node.children.items():
# #             prefix, split, rest = self.match(key, word)
# #             if not split and not rest:
# #                 return child.is_word
# #             if not split:
# #                 return self.search_helper(child,rest)
# #         return False

# #     def startsWith(self,word):
# #         return self.startsWith_helper(self.root,word)

# #     def startsWith_helper(self,node,word):
# #         for key,child in node.children.items():
# #             prefix, split, rest = self.match(key, word)
# #             if not rest:
# #                 return True
# #             if not split:
# #                 return self.startsWith_helper(child,rest)
# #         return False

# #     def match(self, key, word):
# #         i=0
# #         for k,w in zip(key,word):
# #             if k!=w:
# #                 break
# #             i+=1
# #         return key[:i],key[i:],word[i:]
    
    

# # rad = Trie()
# # rad.insert("1010111")


# # input = "1010111"
# # print(input + ":   ", end="")
# # print(rad.search(input))
# class RadixTreeNode:
#     def __init__(self, value=None):
#         self.value = value
#         self.children = {}

#     def add_child(self, key, value=None):
#         self.children[key] = RadixTreeNode(value)

#     def has_child(self, key):
#         return key in self.children

#     def get_child(self, key):
#         return self.children[key]

# class RadixTree:
#     def __init__(self):
#         self.root = RadixTreeNode()
        
#     def insert(self, ip_address, action):
#         node = self.root
#         octets = ip_address.split(".")
#         for i, octet in enumerate(octets):
#             if not node.has_child(octet):
#                 if i == 2:
#                     node.add_child("*", action)
#                 else:
#                     node.add_child(octet)
#             node = node.get_child(octet)
#         node.value = (ip_address, action)

#     def search(self, ip_address):
#         node = self.root
#         octets = ip_address.split(".")
#         for i, octet in enumerate(octets):
#             if i == 2:
#                 if node.has_child("*"):
#                     return node.get_child("*").value
#                 else:
#                     return None
#             if not node.has_child(octet):
#                 return None
#             node = node.get_child(octet)
#         return node.value
#     def check_ip_in_subnet(ip_address, subnet_address, subnet_mask):
#         ip_address_binary = ''.join(format(int(x), '08b') for x in ip_address.split("."))
#         subnet_address_binary = ''.join(format(int(x), '08b') for x in subnet_address.split("."))
#         subnet_mask_binary = ''.join(format(int(x), '08b') for x in subnet_mask.split("."))
#         for i in range(32):
#             if subnet_mask_binary[i] == "1":
#                 if ip_address_binary[i] != subnet_address_binary[i]:
#                     return False
#         return True
    
#     # Test code
# # rt = RadixTree()

# # # Insert IP addresses to block
# # rt.insert("192.168.1.1", "block")
# # rt.insert("192.168.1.2", "block")

# # # Insert IP addresses to allow
# # rt.insert("192.168.2.1", "allow")
# # rt.insert("192.168.3.1", "allow")

# # # Search for an IP address
# # print(rt.search("192.168.1.1")) # prints ("192.168.1.1", "block")
# # print(rt.search("192.168.2.1")) # prints ("192.168.2.1", "allow")

# rt = RadixTree()

# # Insert IP addresses to block
# rt.insert("192.168.1.0", "255.255.255.0", "block")

# # Search for an IP address
# ip_address = "192.168.1.12"
# subnet_address = "192.168.1.0"
# subnet_mask = "255.255.255.0"
# if rt.check_ip_in_subnet(ip_address, subnet_address, subnet_mask):
#     print(ip_address, "is in the blocked subnet")
# else:
#     print(ip_address, "is not in the blocked subnet")
class Node:
    def __init__(self):
        self.children = {}
        self.leaf = False
        self.block = False

class RadixTree:
    def __init__(self):
        self.root = Node()

    def insert(self, ip):
        current_node = self.root
        for bit in self._ip_to_bits(ip):
            if bit not in current_node.children:
                current_node.children[bit] = Node()
            current_node = current_node.children[bit]
        current_node.leaf = True

    def search(self, ip):
        current_node = self.root
        for bit in self._ip_to_bits(ip):
            if bit not in current_node.children:
                return False
            current_node = current_node.children[bit]
        return current_node.block

    def block(self, ip):
        current_node = self.root
        for bit in self._ip_to_bits(ip):
            if bit not in current_node.children:
                return False
            current_node = current_node.children[bit]
        current_node.block = True
        return True
        
    def _ip_to_bits(self, ip):
        ip_parts = ip.split('.')
        bits = [bin(int(part))[2:].zfill(8) for part in ip_parts]
        
        
# Create a new Radix Tree
tree = RadixTree()

# Insert some IP addresses
tree.insert("192.168.1.1")
tree.insert("192.168.1.2")
tree.insert("192.168.1.3")
tree.insert("192.168.2.1")

# Block a range of IP addresses
tree.block("192.168.1.0/24")

# Search for an IP address
print(tree.search("192.168.1.1")) # Output: True
print(tree.search("192.168.2.1")) # Output: False