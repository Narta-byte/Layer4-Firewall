import unittest
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable

import random
import logging
import cProfile
import pstats


class TestEquivalenceOfListAndTrietree(unittest.TestCase):
    def setUp(self):
        self.tree0 = policyTrieTree.PolicyTrieTree()
        self.tree1 = policyTrieTree.PolicyTrieTree()
        self.tree2 = policyTrieTree.PolicyTrieTree()
        self.tree3 = policyTrieTree.PolicyTrieTree()
        self.tree4 = policyTrieTree.PolicyTrieTree()
        # treeList = [self.tree0, self.tree1, self.tree2, self.tree3, self.tree4]
        treeList = [self.tree0, self.tree1, self.tree2]
        # treeList = [self.tree0, self.tree1]
        # treeList = [self.tree0]

        self.policyBuilder = PolicyBuilder.PolicyBuilder(treeList)
        self.policyBuilder.setSeed(311415)

        self.hashTable = CuckooHashTable.CuckooHashTable()

        self.listFirewall = listFirewall.ListFirewall()

        # deleting all the logs
        file = open("logs.txt", "w")
        file.flush()
        file.close()

        logging.basicConfig(
            format="%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%d-%m-%Y:%H:%M:%S",
            level=logging.DEBUG,
            filename="logs.txt",
        )

    def test_samePacketsInBoth(self):
        rule0 = ("5", "5", "12", "alpha")
        rule1 = ("*", "*", "*", "beta")
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))

        self.listFirewall.insertRule(rule0)
        self.listFirewall.insertRule(rule1)

        # 1ST TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("1", "1", "1"))

        logging.debug("codeword!: " + str(codeword))

        self.policyBuilder.writeCodewords()
        self.assertEqual(
            self.listFirewall.lookup(("1", "1", "1")),
            self.hashTable.lookup(codeword)[0][3],
        )

        # 2ND TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("1", "7", "11"))
        self.assertEqual(
            self.listFirewall.lookup(("1", "7", "11")),
            self.hashTable.lookup(codeword)[0][3],
        )
        logging.debug("codeword!: " + str(codeword))

        # 3RD TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("255", "255", "255"))
        logging.debug("codeword!: " + str(codeword))

        self.assertEqual(
            self.listFirewall.lookup(("255", "255", "255")),
            self.hashTable.lookup(codeword)[0][3],
        )

    def test_randomPackets_with_ranges(
        self,
    ):  # Test 500 random packages vs firewall list
        import cProfile

        pr = cProfile.Profile()
        pr.enable()

        ruleList = []
        random.seed(311415)
        for k in range(0, 20):
            rule = ["", "", "", ""]
            for i in range(0, 3):
                chance = random.randint(0, 100)
                if chance <= 2:
                    rule[i] = str(random.randint(0, 25))
                elif chance > 2 and chance <= 4:
                    rule[i] = "*"
                elif chance > 4:
                    rule[i] = format(random.randint(0, 25), "b") + "*"
            chance = random.randint(0, 100)
            if chance < 25:
                rule[3] = "alpha"
            elif chance >= 25 and chance <= 50:
                rule[3] = "beta"
            elif chance > 50 and chance < 75:
                rule[3] = "gamma"
            elif chance >= 75:
                rule[3] = "hotel"
            ruleList.append(rule)
        # file = open("rule_list_for_random_test.txt", "w")

        # cProfile.run(self.policyBuilder.insertRule([rule for rule in ruleList]), "profile.txt")
        # stats = pstats.Stats('profile.txt')
        # stats.sort_stats('cumulative').print_stats(10)
        # self.policyBuilder.insertRule([rule for rule in ruleList])

        for rule in ruleList:
            if rule[:3] == ["*", "*", "*"]:
                logging.debug("Throwing out ***" + str(rule))
                continue
            logging.debug("New inserted packet: " + str(rule))
            # file.write(str(rule)+"\n")
            self.policyBuilder.insertRule(rule)
            self.listFirewall.insertRule(rule)
        # file.close()
        self.policyBuilder.insertRule(("*", "*", "*", "delta"))
        self.listFirewall.insertRule(("*", "*", "*", "delta"))

        # file = open("list_firewall.txt", "w")
        # file.write(self.listFirewall.getRules())
        # file.close()

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))

        # self.tree0.drawGraph(html = True)
        self.policyBuilder.writeCodewords()

        packetList = []
        for i in range(0, 100):
            packet = (
                str(random.randint(0, 25)),
                str(random.randint(0, 25)),
                str(random.randint(0, 25)),
            )
            # for j in range(0,3):
            #     packet[j] = str(random.randint(0,5))

            logging.debug("")
            logging.debug("NEW PACKET:       packetnum: " + str(i))

            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][3]
            logging.debug("(codeword) " + str(codeword))

            logging.debug(
                "looking up packet op: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )
            logging.debug("looking up hash op: " + str(self.hashTable.lookup(codeword)))

            packetList.append(packet)
            logging.debug(
                "packetnumber: "
                + str(i)
                + " firewalll: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )

            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3]
            )

        pr.disable()
        pr.print_stats(sort="time")

    def test_randomPackets(self):  # Test 500 random packages vs firewall list
        pr = cProfile.Profile()
        pr.enable()
        ruleList = []
        numrange = 15
        random.seed(311415)
        for _ in range(0, 40):  # NUM RULES
            rule = ["", "", "", ""]
            for i in range(0, 3):
                chance = random.randint(0, 100)
                if chance <= 25:
                    rule[i] = str(random.randint(0, numrange))
                elif chance > 25 and chance <= 65:
                    rule[i] = "*"
                elif chance > 65:
                    rule[i] = str(random.randint(0, numrange))
            chance = random.randint(0, 100)
            if chance < 10:
                rule[3] = "alpha"
            elif 10 <= chance < 20:
                rule[3] = "beta"
            elif 20 <= chance < 30:
                rule[3] = "gamma"
            elif 30 <= chance < 40:
                rule[3] = "delta"
            elif 40 <= chance < 50:
                rule[3] = "epsilon"
            elif 50 <= chance < 60:
                rule[3] = "zeta"
            elif 60 <= chance < 70:
                rule[3] = "eta"
            elif 70 <= chance < 80:
                rule[3] = "theta"
            elif 80 <= chance < 90:
                rule[3] = "iota"
            else:  # 90 <= chance <= 100
                rule[3] = "kappa"
            ruleList.append(rule)

        file = open("rule_list_for_random_test.txt", "w")
        for rule in ruleList:
            if rule[:3] == ["*", "*", "*"]:
                logging.debug("Throwing out ***" + str(rule))
                continue
            logging.debug("New inserted packet: " + str(rule))
            file.write(str(rule) + "\n")
            self.policyBuilder.insertRule(rule)
            self.listFirewall.insertRule(rule)
        file.close()
        # self.policyBuilder.insertRule(("*", "*", "*", "delta"))
        self.policyBuilder.insertRule(["*", "*", "*", "default"])
        self.listFirewall.insertRule(("*", "*", "*", "default"))

        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        file.close()

        self.policyBuilder.writeCodewords()

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))

        packetList = []
        for i in range(0, 10000):  # _____________ INSERT MORE PACKETS HERE ____________
            packet = (
                str(random.randint(0, numrange)),
                str(random.randint(0, numrange)),
                str(random.randint(0, numrange)),
            )
            # for j in range(0,3):
            #     packet[j] = str(random.randint(0,5))

            logging.debug("")
            logging.debug("NEW PACKET:       packetnum: " + str(i))

            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][3]
            logging.debug("(codeword) " + str(codeword))

            logging.debug(
                "looking up packet op: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )
            logging.debug("looking up hash op: " + str(self.hashTable.lookup(codeword)))

            # self.policyBuilder.writeCodewords()

            packetList.append(packet)
            logging.debug(
                "packetnumber: "
                + str(i)
                + " firewalll: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )

            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3]
            )

        # self.policyBuilder.writeCodewords()
        pr.disable()
        pr.print_stats(sort="time")


    def test_twoTrees(self):
        rule0 = ("5", "12", "alpha")
        rule1 = ("*", "*", "beta")
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))

        self.listFirewall.insertRule(rule0)
        self.listFirewall.insertRule(rule1)

        # 1ST TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("1", "1"))

        logging.debug("codeword!: " + str(codeword))

        self.policyBuilder.writeCodewords()
        self.assertEqual(
            self.listFirewall.lookup(("1", "1")), self.hashTable.lookup(codeword)[0][2]
        )

        # #2ND TEST
        # codeword = ""
        # codeword = self.policyBuilder.retriveCodeword(("1","7","11"))
        # self.assertEqual(self.listFirewall.lookup(("1","7","11")), self.hashTable.lookup(codeword)[0][3])
        # logging.debug("codeword!: " + str(codeword))

        # #3RD TEST
        # codeword = ""
        # codeword = self.policyBuilder.retriveCodeword(("255","255","255"))
        # logging.debug("codeword!: " + str(codeword))

        # self.assertEqual(self.listFirewall.lookup(("255","255","255")), self.hashTable.lookup(codeword)[0][3])

    def test_oneTree(self):
        rule0 = ("5", "alpha")
        rule1 = ("*", "beta")
        self.policyBuilder.insertRule(rule0)
        self.policyBuilder.insertRule(rule1)

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))

        self.listFirewall.insertRule(rule0)
        self.listFirewall.insertRule(rule1)

        # 1ST TEST
        codeword = ""
        codeword = self.policyBuilder.retriveCodeword(("1"))

        logging.debug("codeword!: " + str(codeword))

        self.policyBuilder.writeCodewords()
        self.assertEqual(
            self.listFirewall.lookup(("1")), self.hashTable.lookup(codeword)[0][1]
        )

    def test_randomPackets_with_ranges(self, tree_count=3):
        # Test 500 random packages vs firewall list
        pr = cProfile.Profile()
        pr.enable()

        ruleList = self.generate_rule_list(13, tree_count)  # Num of rules!

        for rule in ruleList:
            if rule[:tree_count] == ["*"] * tree_count:
                logging.debug("Throwing out ***" + str(rule))
                continue
            logging.debug("____________________New inserted packet: " + str(rule))
            self.policyBuilder.insertRule(rule)
            self.listFirewall.insertRule(rule)

        self.policyBuilder.insertRule(("*",) * tree_count + ("Zooted",))
        self.listFirewall.insertRule(("*",) * tree_count + ("Zooted",))

        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        file.close()

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))

        # self.tree0.drawGraph(html=True)
        self.policyBuilder.writeCodewords()
        packetList = [self.generate_packet(tree_count) for _ in range(1000)]  # Number of packets
        for i, packet in enumerate(packetList):
            logging.debug("_____NEW PACKET:       packetnum: " + str(i))

            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][tree_count]
            logging.debug("(codeword) " + str(codeword))

            logging.debug(
                "looking up packet op: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )
            logging.debug("looking up hash op: " + str(self.hashTable.lookup(codeword)))

            logging.debug(
                "packetnumber: "
                + str(i)
                + " firewalll: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )

            self.assertEqual(
                self.listFirewall.lookup(packet),
                self.hashTable.lookup(codeword)[0][tree_count],
            )

        pr.disable()
        pr.print_stats(sort="time")

    def generate_rule_list(self, count, tree_count):
        random.seed(311415)
        ruleList = []

        for _ in range(count):
            rule = [self.generate_rule_element(i) for i in range(tree_count)]
            rule.append(self.generate_action())
            ruleList.append(rule)

        return ruleList

    def generate_rule_element(self, i):
        range_num = 15 #2**16
        chance = random.randint(0, 50)
        if chance <= 4:
            return str(random.randint(0, range_num))
        elif chance <= 16:
            return "*"
        else:
            return format(random.randint(0, range_num), "b") + "*"

    def generate_action(self):
        chance = random.randint(0, 100)
        if chance < 10:
            return "alpha"
        elif chance < 20:
            return "beta"
        elif chance < 30:
            return "gamma"
        elif chance < 40:
            return "delta"
        elif chance < 50:
            return "epsilon"
        elif chance < 60:
            return "zeta"
        elif chance < 70:
            return "eta"
        elif chance < 80:
            return "theta"
        elif chance < 90:
            return "iota"
        else:
            return "kappa"

    # The rest of the helper functions remain unchanged

    def generate_packet(self, tree_count):
        range_num = 15 #2**16
        return tuple(str(random.randint(0, range_num)) for _ in range(tree_count))

    def test_packets(self, packetList, tree_count):
        for i, packet in enumerate(packetList):
            logging.debug("\nNEW PACKET:       packetnum: " + str(i))

            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][3]
            logging.debug("(codeword) " + str(codeword))

            logging.debug(
                "looking up packet op: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )
            logging.debug("looking up hash op: " + str(self.hashTable.lookup(codeword)))

            self.policyBuilder.writeCodewords()
            logging.debug(
                "packetnumber: "
                + str(i)
                + " firewalll: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )
            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3]
            )

    def test_custom_test(self):  # Test 500 random packages vs firewall list
        pr = cProfile.Profile()
        pr.enable()
        ruleList = []

        ruleList = [
            ["79", "90", "40", "hotel"],
            ["49", "68", "56", "alpha"],
            ["97", "*", "66", "beta"],
            ["57", "95", "90", "hotel"],
            ["76", "11", "*", "beta"],
            ["65", "94", "70", "alpha"],
            ["7", "*", "*", "alpha"],
            ["62", "47", "45", "beta"],
            ["29", "81", "40", "hotel"],
        ]

        for rule in ruleList:
            if rule[:3] == ["*", "*", "*"]:
                logging.debug("Throwing out ***" + str(rule))
                continue
            logging.debug("New inserted packet: " + str(rule))
            self.policyBuilder.insertRule(rule)
            self.listFirewall.insertRule(rule)
        # self.policyBuilder.insertRule(("*", "*", "*", "delta"))
        self.policyBuilder.insertRule(["*", "*", "*", "delta"])
        self.listFirewall.insertRule(("*", "*", "*", "delta"))

        file = open("list_firewall.txt", "w")
        file.write(self.listFirewall.getRules())
        file.close()

        self.policyBuilder.writeCodewords()

        for rank, rule in enumerate(self.policyBuilder.previousRuleTuple):
            self.hashTable.insert(rule[1], (rule[0], rank))

        packetList = []
        for i in range(0, 10):  # _____________ INSERT MORE PACKETS HERE ____________
            packet = (
                str(random.randint(0, 100)),
                str(random.randint(0, 100)),
                str(random.randint(0, 100)),
            )
            # for j in range(0,3):
            #     packet[j] = str(random.randint(0,5))

            logging.debug("")
            logging.debug("NEW PACKET:       packetnum: " + str(i))

            codeword = self.policyBuilder.retriveCodeword(packet)
            if codeword is None:
                codeword = self.hashTable.defualtRule[0][3]
            logging.debug("(codeword) " + str(codeword))

            logging.debug(
                "looking up packet op: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )
            logging.debug("looking up hash op: " + str(self.hashTable.lookup(codeword)))

            # self.policyBuilder.writeCodewords()

            packetList.append(packet)
            logging.debug(
                "packetnumber: "
                + str(i)
                + " firewalll: "
                + str(packet)
                + str(self.listFirewall.lookup(packet))
            )

            self.assertEqual(
                self.listFirewall.lookup(packet), self.hashTable.lookup(codeword)[0][3]
            )

        # self.policyBuilder.writeCodewords()
        pr.disable()
        pr.print_stats(sort="time")
