import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import logging
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall
import cProfile


class TestErrorCase(unittest.TestCase):
    def setUp(self):
        file = open("logs.txt", "w")
        file.flush()
        file.close()

        logging.basicConfig(
            format="%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%d-%m-%Y:%H:%M:%S",
            level=logging.DEBUG,
            filename="logs.txt",
        )

        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()

    def test_subRanges(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["10*", "1", "1", "alpha"],
            ["1*", "1", "1", "beta"],
            ["*", "*", "*", "gamma"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["12", "1", "1"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "In firewall : "
                + str(self.listFirewall.lookup(packet))
                + ", in hash: "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )

    def test_packet10(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
['10*', '1100*', '1111*', 'epsilon'],
['*', '0*', '*', 'theta'],
['110*', '*', '*', 'theta'],
['*', '14', '1000*', 'alpha'],
['1110*', '110*', '111*', 'epsilon'],
['10*', '11*', '*', 'kappa'],
['111*', '1011*', '1110*', 'beta'],
['10*', '1011*', '1110*', 'kappa'],
['*', '5', '10*', 'gamma'],
('*', '*', '*', 'Zooted')

        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["13", "5", "3"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "In firewall : "
                + str(self.listFirewall.lookup(packet))
                + ", in hash: "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )


    def test_packet62(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
['*', '0*', '*', 'hotel'],
['*', '14', '1000*', 'alpha'],
('*', '*', '*', 'delta')
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [['4', '5', '15']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "In firewall : "
                + str(self.listFirewall.lookup(packet))
                + ", in hash: "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )


















    def initListAndTreeFirewalls(self, ruleList):
        for rule in ruleList:
            logging.debug("___________________New inserted rule: " + str(rule))
            self.policyFactory.insertRule(rule)
            self.listFirewall.insertRule(rule)

        self.hashTable = CuckooHashTable.CuckooHashTable()
        for rule in self.policyFactory.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])

        self.policyFactory.writeCodewords()

    def init3Trees(self, tree_count=3, treeDepth=16):
        self.treeList = [self.create_tree(treeDepth) for _ in range(tree_count)]
        self.policyFactory = PolicyBuilder.PolicyBuilder(self.treeList)
        self.policyFactory.setSeed(311415)

    def create_tree(self, tree_depth):
        tree = policyTrieTree.PolicyTrieTree()
        tree.treeDepth = tree_depth
        return tree
