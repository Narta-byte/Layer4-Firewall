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

        logging.debug("Rulelist from test: ")
        logging.debug(ruleList)
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["0010", "0", "0100"]]  # ,  ['1', '3', '2']]

        for packet in packetList:
            codeword = self.policyFactory.retriveCodeword(packet)

            logging.debug("codeword: " + str(codeword) + " for packet " + str(packet))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+ str(self.listFirewall.lookup(packet))+ ", "+ str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])

    def test_perm_exists_of_newrule(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["1", "*", "0", "alpha"],
            ["*", "0", "3", "gaf"],
            ["*", "*", "0", "beta"],
            ["*", "*", "*", "delta"],
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
            logging.debug("is this list index?: " + str(self.hashTable.lookup(codeword)))
            if self.listFirewall.lookup(packet) != self.hashTable.lookup(codeword)[3]:
                self.logDifference(packet, codeword)
            logging.debug("different decisions : "+ str(self.listFirewall.lookup(packet))+ ", "+ str(self.hashTable.lookup(codeword)[3]))
            self.assertEqual(self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[3])

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
            ["29", "13", "10", "gamma"],
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

    def test_packet_newnew62(self):
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["10", "12", "15", "epsilon"],
            ["4", "*", "*", "theta"],
            ["*", "5", "7", "gamma"],
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

    def test_back_to_sq_1(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["7", "*", "2", "gamma"],
            ["*", "9", "*", "alpha"],
            ["10", "6", "*", "alpha"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["10", "9", "2"]]
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

    def test_packet6(self):
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["*", "*", "6", "beta"],
            ["2", "13", "11", "gamma"],
            ["14", "6", "5", "gamma"],
            ["*", "9", "*", "alpha"],
            ["*", "11", "2", "gamma"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [
            ["14", "11", "6"]
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

    def test_packet34(self):
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["2", "*", "12", "a"],
            ["*", "2", "*", "v"],
            ["*", "11", "2", "c"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [
            ["2", "2", "12"]
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

    def test_last_test_here(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["*", "*", "3", "b"],
            ["13", "*", "*", "c"],
            ["*", "5", "10*", "k"],
            ("*", "*", "*", "Zooted"),
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

    def test_last_one(self):
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["12", "0", "6", "alpha"],
            ["*", "*", "6", "beta"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [
            ["12", "0", "6"]
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

    def test_come_on(self):
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["*", "9", "12", "alpha"],
            ["*", "*", "12", "beta"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [
            ["3", "9", "12"]
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

    def test_grindin(self):
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["14", "*", "5", "gamma"],
            ["*", "18", "*", "alpha"],
            ["14", "18", "*", "hotel"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [
            ["14", "18", "15"]
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

    def test_back_atit(self):
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["*", "*", "25", "epsilon"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [
            ["9", "27", "45"]
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

    def test_lastonepls(self):
        self.init3Trees(treeDepth=4)
        self.listFirewall = listFirewall.ListFirewall()
        self.listFirewall.treeDepth = 4
        self.policyFactory.codewordLength = 4
        ruleList = [
            ["9", "*", "49", "zeta"],
            ["*", "19", "24", "gamma"],
            ["12", "57", "34", "alpha"],
            ["*", "*", "*", "default"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["9", "27", "45"]]

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

    def test_range200(self):
        self.init3Trees()
        self.listFirewall = listFirewall.ListFirewall()
        ruleList = [
            ["18", "188", "109", "gamma"],
            ["60", "129", "39", "gamma"],
            ["48", "*", "144", "alpha"],
            ["156", "190", "1", "beta"],
            ["163", "134", "51", "beta"],
            ["59", "185", "21", "gamma"],
            ["20", "104", "132", "beta"],
            ["115", "190", "180", "hotel"],
            ["152", "22", "93", "hotel"],
            ["185", "*", "40", "gamma"],
            ["45", "154", "124", "gamma"],
            ["74", "11", "155", "beta"],
            ["2", "56", "79", "hotel"],
            ["17", "16", "147", "hotel"],
            ["172", "*", "26", "alpha"],
            ["189", "134", "167", "alpha"],
            ["150", "121", "127", "alpha"],
            ["44", "51", "155", "alpha"],
            ["2", "50", "107", "gamma"],
            ["*", "160", "26", "gamma"],
            ["147", "*", "80", "beta"],
            ["88", "125", "2", "hotel"],
            ["135", "*", "42", "alpha"],
            ["16", "69", "46", "gamma"],
            ["70", "52", "61", "alpha"],
            ["192", "21", "146", "hotel"],
            ["122", "74", "45", "alpha"],
            ["42", "142", "152", "beta"],
            ["29", "130", "71", "alpha"],
            ["28", "140", "168", "gamma"],
            ["179", "67", "170", "gamma"],
            ["30", "145", "104", "hotel"],
            ["25", "159", "139", "hotel"],
            ["175", "130", "189", "hotel"],
            ["20", "15", "110", "alpha"],
            ["124", "95", "91", "beta"],
            ["58", "162", "81", "hotel"],
            ["19", "134", "183", "gamma"],
            ["195", "14", "58", "gamma"],
            ["21", "22", "97", "hotel"],
            ["119", "*", "181", "beta"],
            ["*", "175", "25", "beta"],
            ["149", "75", "90", "gamma"],
            ["22", "155", "3", "alpha"],
            ["17", "6", "11", "hotel"],
            ["107", "161", "111", "gamma"],
            ["196", "44", "94", "gamma"],
            ["69", "16", "*", "beta"],
            ["112", "44", "84", "alpha"],
            ["194", "181", "105", "hotel"],
            ["170", "19", "186", "gamma"],
            ["176", "102", "105", "gamma"],
            ["82", "85", "192", "gamma"],
            ["31", "87", "14", "hotel"],
            ["7", "73", "192", "hotel"],
            ["59", "187", "41", "hotel"],
            ["129", "21", "1", "beta"],
            ["30", "140", "13", "hotel"],
            ["160", "192", "125", "beta"],
            ["41", "*", "142", "gamma"],
            ["40", "43", "69", "hotel"],
            ["48", "0", "18", "alpha"],
            ["66", "18", "176", "beta"],
            ["30", "10", "10", "gamma"],
            ["60", "40", "199", "hotel"],
            ["87", "173", "28", "beta"],
            ["*", "157", "64", "hotel"],
            ["30", "55", "196", "gamma"],
            ["29", "184", "61", "gamma"],
            ["103", "72", "73", "beta"],
            ["*", "30", "146", "alpha"],
            ["82", "146", "154", "gamma"],
            ["200", "10", "33", "beta"],
            ["*", "182", "164", "hotel"],
            ["184", "23", "174", "beta"],
            ["83", "174", "146", "hotel"],
            ["52", "13", "110", "hotel"],
            ["196", "117", "*", "alpha"],
            ["81", "16", "96", "hotel"],
            ["7", "104", "22", "alpha"],
            ["*", "*", "*", "delta"],
        ]
        self.initListAndTreeFirewalls(ruleList)
        packetList = [["0", "134", "3"]]
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

    def test_oneTree(self):  # wait with this
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
            # self.policyBuilder.insertRule(rule)
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
