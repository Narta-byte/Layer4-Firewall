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
            ["*", "0*", "*", "alpha"],
            ["12", "*", "6", "beta"],
            ("*", "*", "*", "delta"),
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["12", "13", "6"]]

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

    def test_surprisebug(self):
        self.init3Trees(treeDepth=16)
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["17", "1101*", "1111*", "alpha"],
            ["*", "10*", "11010*", "alpha"],
            ["0*", "11100*", "10011*", "hotel"],
            ["*", "*", "*", "delta"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        #        self.initListAndTreeFirewalls(['*', '*', '*', 'delta'])

        packetList = [["17", "10", "38"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug(
                "different decisions : "
                + str(self.listFirewall.lookup(packet))
                + ", "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )

    def test_errorcaseTEMP(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["0*", "*", "5", "beta"],
            ["3", "0", "101*", "gamma"],
            ["*", "*", "*", "charlie"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["3", "4", "5"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
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
            ["*", "0*", "*", "hotel"],
            ["*", "14", "1000*", "alpha"],
            ("*", "*", "*", "delta"),
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["4", "5", "15"]]

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

    def test_packet_new62(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        # self.
        ruleList = [
            ["9", "1100*", "1111*", "epsilon"],
            ["*", "0*", "*", "theta"],
            ["*", "5", "10*", "gamma"],
            ("*", "*", "*", "Zooted"),
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [
            ["4", "5", "15"]
            # ["12", "13", "6"]
        ]

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

    def test_packet62again(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["*", "0*", "*", "theta"],
            ["*", "5", "10*", "gamma"],
            ["*", "11*", "15", "kappa"],
            ["*", "*", "*", "Zooted"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["4", "5", "15"]]

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

    def test_62_noch_mal(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["10*", "12", "15", "epsilon"],
            ["*", "0*", "*", "theta"],
            ["110*", "*", "*", "theta"],
            ["*", "14", "8", "alpha"],
            ["14", "110*", "111*", "epsilon"],
            ["10*", "11*", "*", "kappa"],
            ["111*", "11", "14", "beta"],
            ["10*", "11", "14", "kappa"],
            ["*", "5", "10*", "gamma"],
            ["14", "12", "9", "delta"],
            ["8", "0*", "111*", "zeta"],
            ["11", "2", "10", "iota"],
            ["*", "11*", "15", "kappa"],
            ["*", "*", "*", "Zooted"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["4", "5", "15"]]

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

    def test_packet1(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["10*", "12", "15", "epsilon"],
            ["*", "0*", "*", "theta"],
            ["110*", "*", "*", "theta"],
            ["*", "14", "8", "alpha"],
            ["14", "110*", "111*", "epsilon"],
            ["10*", "11*", "*", "kappa"],
            ["111*", "11", "14", "beta"],
            ["10*", "11", "14", "kappa"],
            ["*", "5", "10*", "gamma"],
            ["14", "12", "9", "delta"],
            ["8", "0*", "111*", "zeta"],
            ["11", "2", "10", "iota"],
            ["*", "11*", "15", "kappa"],
            ["*", "*", "*", "Zooted"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [['10', '15', '15']]

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
