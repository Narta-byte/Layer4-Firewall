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

        ruleList = [
            ["*", "*", "3", "alpha"],
            ["0", "2", "*", "beta"],
            ["*", "2", "3", "delta"],
            ["*", "*", "*", "gamma"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packet = ["8", "2", "3"]

        codeword = self.policyFactory.retriveCodeword(packet)

        logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
        if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
            self.logDifference(packet, codeword)

        logging.debug(
            "In firewall: "
            + str(self.listFirewall.lookup(packet))
            + " | in hash: "
            + str(self.hashTable.lookup(codeword)[3])
        )

        self.assertEqual(
            self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
        )

    def test_permutations(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()

        ruleList = [
            ["*", "5", "2", "beta"],
            ["3", "*", "*", "alpha"],
            ["0", "3", "4", "alpha"],
            ["*", "*", "0", "beta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packet = ["5", "3", "0"]

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

    def test_superset(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["*", "5", "2", "beta"],
            ["*", "*", "2", "alpha"],
            ["*", "3", "0", "gamma"],
            # ['*', '*', '*', 'hotel'],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["1", "3", "2"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("last codeword test: " + str(codeword))
            logging.debug(
                "different decisions : "
                + str(self.listFirewall.lookup(packet))
                + ", "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )

    def test_new_rule_is_subset(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["3", "*", "*", "alpha"],
            ["0", "3", "4", "alpha"],
            ["3", "5", "5", "beta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["3", "5", "5"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("last codeword test: " + str(codeword))
            logging.debug(
                "In firewall : "
                + str(self.listFirewall.lookup(packet))
                + ", in hash: "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )

    def test_errorcase(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["1", "*", "0", "gamme"],
            ["*", "*", "2", "alpha"],
            ["*", "*", "*", "hotel"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["1", "3", "2"]]

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

    def test_errorcase_next(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["*", "5", "2", "beta"],
            ["3", "*", "*", "alpha"],
            ["0", "3", "4", "alpha"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["0", "3", "4"]]  # ,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            # if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
            #   self.logDifference(packet, codeword)
            # logging.debug("different decisions : "+str(self.listFirewall.lookup(packet))+", " +str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )

    def test_errorcase_next2(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["0", "5", "3", "beta"],
            ["1", "*", "0", "alpha"],
            ["*", "*", "1", "alpha"],
            # ['*', '*', '*', 'delta']
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["2", "5", "1"]]  # ,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "hash lookup codeword: " + str(self.hashTable.lookup(codeword))
            )
            logging.debug("hash lookup: " + str(self.hashTable.lookup(codeword)[3]))
            logging.debug(
                "different decisions : "
                + str(self.listFirewall.lookup(packet))
                + ", "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )

    def test_very_basic(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["*", "0", "*", "beta"],
            ["*", "*", "0100", "alpha"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["0010", "0", "0100"]]  # ,  ['1', '3', '2']]

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

    def test_perm_exists_of_newrule(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["1", "*", "0", "alpha"],
            ["*", "0", "3", "beta"],
            ["*", "*", "0", "beta"],
            # ['*', '*', '*', 'delta']
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["5", "1", "0"]]  # ,  ['1', '3', '2']]

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

    def test_tryRemoveLast_rule(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["*", "5", "2", "beta"],
            ["*", "*", "2", "alpha"],
            ["2", "*", "*", "alpha"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["2", "1", "2"]]  # ,  ['1', '3', '2']]

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

        # def test_errorcaseTEMP(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["0*", "*", "5", "gamma"],
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

    def test_newbug(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["0", "*", "5", "gamma"],
            ["1", "1", "*", "alpha"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["1", "2", "5"]]  # ,["1","2","3"]] #['12','1','1']]

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

    def test_should_never_have_happened(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["1", "4", "1", "gamma"],
            ["3", "2", "2", "gamma"],
            ["*", "*", "*", "delta"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        #        self.initListAndTreeFirewalls(['*', '*', '*', 'delta'])

        packetList = [["1", "2", "4"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_same_case(self):
        self.init3Trees(3, 16)
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["5", "3", "4", "alpha"],
            ["2", "0", "0", "gamma"],
            ["*", "*", "*", "delta"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        #        self.initListAndTreeFirewalls(['*', '*', '*', 'delta'])

        packetList = [["1", "3", "0"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_new_def_case(self):
        self.init3Trees(3, 16)
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["3", "0", "2", "alpha"],
            ["*", "2", "*", "alpha"],
            ["*", "*", "*", "delta"]
            # ['4', '4', '1', 'alpha'],
            # ['*', '2', '*', 'alpha'],
            # ['*', '*', '*', 'delta']
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["4", "2", "5"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_new_caseee(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["3", "9", "*", "gamma"],
            ["*", "2", "6", "hotel"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["3", "2", "6"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_never_ending(
        self,
    ):  # Change the * guard in perms. Maybe change it with just check for equal rules
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["29", "13", "10", "gamma"],
            ["22", "18", "37", "gamma"],
            ["38", "0", "4", "beta"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["22", "18", "37"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "This is what we lookup: " + str(self.hashTable.lookup(codeword))
            )
            logging.debug(
                "In firewall : "
                + str(self.listFirewall.lookup(packet))
                + ", in hash: "
                + str(self.hashTable.lookup(codeword)[3])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3]
            )

    def test_possibly_last(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["30", "64", "19", "gamma"],
            ["7", "*", "*", "alpha"],
            ["*", "*", "*", "delta"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["7", "91", "19"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_has_tobe_last(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["30", "64", "19", "gamma"],
            ["7", "*", "*", "alpha"],
            ["62", "47", "45", "beta"],
        ]

        self.initListAndTreeFirewalls(ruleList)
        packetList = [["7", "31", "69"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_packet_367(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["57", "34", "43", "gamma"],
            ["28", "72", "15", "hotel"],
            ["7", "*", "*", "alpha"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["7", "72", "43"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_next(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["97", "*", "66", "beta"],
            ["76", "11", "*", "beta"],
            ["59", "26", "20", "gamma"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["59", "39", "82"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_newParadigm(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["24", "19", "12", "alpha"],
            ["97", "*", "66", "beta"],
            ["76", "11", "*", "beta"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["24", "56", "8"]]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_done_soon_pls(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["24", "19", "12", "alpha"],
            ["97", "*", "66", "beta"],
            ["57", "95", "90", "hotel"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["24", "25", "90"]]
        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_packet545(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["97", "*", "66", "beta"],
            ["57", "95", "90", "hotel"],
            ["59", "26", "20", "gamma"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["59", "30", "90"]]
        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_packet657(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["30", "64", "19", "gamma"],
            ["79", "90", "40", "hotel"],
            ["97", "*", "66", "beta"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["79", "64", "66"]]
        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_packet3660(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["30", "64", "19", "gamma"],
            ["76", "11", "*", "beta"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["76", "64", "19"]]  # ['30', '11', '24']
        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_4010(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["76", "11", "*", "beta"],
            ["1", "25", "53", "gamma"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["76", "11", "53"]]
        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_2089(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["7", "*", "*", "alpha"],
            ["29", "81", "40", "hotel"],
            ["97", "7", "29", "gamma"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["7", "81", "29"]]
        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_158799(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["76", "11", "*", "beta"],
            ["60", "*", "46", "alpha"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["76", "11", "46"]]
        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            logging.debug(
                "is this list index?: " + str(self.hashTable.lookup(codeword))
            )
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

    def test_oneTree(self):
        numtrees = 1
        self.init3Trees(numtrees, 16)
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [["5", "alpha"], ["2", "gamma"], ["*", "delta"]]

        self.initListAndTreeFirewalls(ruleList)

        packetList = [["5"]]  # ,["1","2","3"]] #['12','1','1']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            # logging.debug("is this list index?: " + str(self.hashTable.lookup(codeword)))
            if (
                self.listFirewall.lookup(packet)
                != self.hashTable.lookup(codeword)[numtrees]
            ):
                self.logDifference(packet, codeword)
            logging.debug(
                "different decisions : "
                + str(self.listFirewall.lookup(packet))
                + ", "
                + str(self.hashTable.lookup(codeword)[numtrees])
            )
            self.assertEqual(
                self.listFirewall.lookup(packet),
                self.hashTable.lookup(codeword)[numtrees],
            )

    def logDifference(self, packet, codeword):
        logging.debug("hashtable lookup" + str(self.hashTable.lookup(["8", "2", "3"])))
        logging.debug(self.policyFactory.getRuleTuple())
        logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
        logging.debug("packet: " + str(packet))
        logging.debug("hashTableValue: " + str(self.hashTable.lookup(codeword)))
        self.policyFactory.writeCodewords()
        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        # logging.debug("Tree0's codeword "+str(self.tree0.getCodeword(packet[0])))
        # logging.debug("Tree1's codeword "+str(self.tree1.getCodeword(packet[1])))
        # logging.debug("Tree2's codeword "+str(self.tree2.getCodeword(packet[2])))

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
