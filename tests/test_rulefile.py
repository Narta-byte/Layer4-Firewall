import Parallel_tree_algorithm.python.ACL_builder.ACLbuilder as ACLbuilder
import Parallel_tree_algorithm.python.Trie_tree.PolicyTrieTree as policyTrieTree
import Parallel_tree_algorithm.python.Trie_tree.PolicyBuilder as PolicyBuilder
import Parallel_tree_algorithm.python.List_Firewall.listFirewall as listFirewall
import Parallel_tree_algorithm.python.Hash_table.CuckooHashTable as CuckooHashTable
import unittest
import logging
import random


class TestRuleFile(unittest.TestCase):
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
        random.seed(31415)
        # self.treeList = []
        self.numberOfTrees = 5
        # for _ in range(self.numberOfTrees):
        #     self.treeList.append(policyTrieTree.PolicyTrieTree())

        # self.treeList[0].treeDepth = 8
        # self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        # self.hashTable = CuckooHashTable.CuckooHashTable()

        # ruleList = self.createRuleList(10)
        # logging.debug("Rule list: " + str(ruleList))
        # for rule in ruleList:
        #    logging.debug("Rule in for loop: " + str(rule))
        #    self.policyBuilder.insertRule(rule)

        # for rule in self.policyBuilder.previousRuleTuple:
        #     self.hashTable.insert(rule[1], rule[0])
        # self.policyBuilder.writeCodewords()

        # self.hashTable.defualtRule = (["*"] * self.numberOfTrees) + ["default"]

        # self.aclBuilder = ACLbuilder.ACLBuilder(
        #     self.treeList, self.policyBuilder, self.hashTable
        # )

    def createRuleList(self, numberOfRules=10):
        ruleList = []
        for _ in range(0, numberOfRules):
            rule = [""] * self.numberOfTrees
            for i in range(0, self.numberOfTrees):
                chance = random.randint(0, 100)
                if chance <= 2:
                    rule[i] = str(random.randint(0, 25))
                elif chance > 2 and chance <= 4:
                    rule[i] = "*"
                elif chance > 4:
                    rule[i] = format(random.randint(0, 25), "b") + "*"
            chance = random.randint(0, 100)
            if chance < 25:
                rule.append("alpha")
            elif chance >= 25 and chance <= 50:
                rule.append("beta")
            elif chance > 50 and chance < 75:
                rule.append("gamma")
            elif chance >= 75:
                # rule[-1] = "hotel"
                rule.append("hotel")

            ruleList.append(rule)
        return ruleList

    def test_treeToVHDL(self):
        logging.debug("treeList: " + str(self.aclBuilder.treeList))
        # self.aclBuilder.treeList[0].drawGraph(html = True)
        # parsedTrees = self.aclBuilder.convertTreeToArray(self.aclBuilder.treeList[0])
        # logging.debug("Parsed trees: " + str(parsedTrees))
        logging.debug(
            "codeword for 11001*"
            + str(self.aclBuilder.treeList[0].getCodeword("11001*"))
        )

        self.aclBuilder.buildACL()

        self.aclBuilder.treeToVHDL(self.aclBuilder.treeList[0])
        self.aclBuilder.programCuckooHashTable(self.hashTable)
        self.assertTrue(True)

    def test_specificRuleList(self):
        self.treeList = []
        # self.numberOfTrees = 5
        self.init3Trees(5, [8, 16, 16, 32, 32])
        # for _ in range(self.numberOfTrees):
        #     self.treeList.append(policyTrieTree.PolicyTrieTree())
        # self.treeList[0].treeDepth = 8
        # self.treeList[1].treeDepth = 16
        # self.treeList[2].treeDepth = 16
        # self.treeList[3].treeDepth = 32
        # self.treeList[4].treeDepth = 32

        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.hashTable = CuckooHashTable.CuckooHashTable()

        ruleList = [
            ["*", "1111001111011101*", "*", "*", "*", "PERMIT"],
            ["*", "*", "*", "*", "*", "DENY"],
        ]

        # ruleList =[
        #     ["00000010","*","*","*","*","PERMIT"],
        #     ["*","*","*","*","*","DENY"],
        # ]
        logging.debug("Rule list: " + str(ruleList))

        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)

        for rule in self.policyBuilder.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        self.policyBuilder.writeCodewords()

        self.hashTable.defualtRule = (["*"] * self.numberOfTrees) + ["default"]

        self.aclBuilder = ACLbuilder.ACLBuilder(
            self.treeList, self.policyBuilder, self.hashTable
        )
        self.aclBuilder.buildACL()
        self.aclBuilder.treeToVHDL(self.aclBuilder.treeList[0])
        self.aclBuilder.programCuckooHashTable(self.hashTable)

    def test_complexRuleSet(self):
        self.treeList = []
        self.init3Trees(5, [8, 16, 16, 32, 32])

        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.hashTable = CuckooHashTable.CuckooHashTable()

        # Protocol       #Src port           #Dst Port           #SrcIP                              #dstIP
        ruleList = [
            [
                "*",
                "00000001101110*",
                "0*",
                "*",
                "00100011101110101110000000011001",
                "flip_bits",
            ],
            ["*", "00000001101110*", "0*", "*", "*", "not_flip_bits"],
            [
                "00000110*",
                "*",
                "*",
                "00001010110100011110110010101010*",
                "*",
                "TCP_with_from_somewhere",
            ],
            ["*", "*", "*", "*", "*", "DENY"],
        ]

        logging.debug("Rule list: " + str(ruleList))

        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)

        for rule in self.policyBuilder.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        self.policyBuilder.writeCodewords()

        self.hashTable.defualtRule = (["*"] * self.numberOfTrees) + ["default"]

        self.aclBuilder = ACLbuilder.ACLBuilder(
            self.treeList, self.policyBuilder, self.hashTable
        )
        self.aclBuilder.buildACL()
        self.aclBuilder.treeToVHDL(self.aclBuilder.treeList[0])
        self.aclBuilder.programCuckooHashTable(self.hashTable)

    def test_RulelistManualTest(self):
        self.treeList = []
        self.init3Trees(5, [8, 16, 16, 32, 32])

        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.hashTable = CuckooHashTable.CuckooHashTable()

        # Protocol       #Src port           #Dst Port           #SrcIP                              #dstIP
        # ruleList = [self.rules() for _ in range(5)]
        ruleList = [
            ["11111111*", "1111111111111111*", "1111111111111111*", "11111111111111111111111111111111*", "11111111111111111111111111111111*", "Aa"],
            ["00000000*", "0000000000000000*", "0000000000000000*", "00000000000000000000000000000000*", "00000000000000000000000000000000*", "Bb"],
            # ["00000000*", "*", "*", "*", "*", "B"],
            # ["11111100*", "1111111111111100*", "1111111111111100*", "*", "*","Ace"],
            # ["0000*", "*", "*", "*", "*", "A"],
            # ["0001*", "*", "*", "*", "*", "B"],
            # ["0010*", "*", "*", "*", "*", "C"],
            # ["0011*", "*", "*", "*", "*", "D"],
            # ["0100*", "*", "*", "*", "*", "E"],
            # ["0101*", "*", "*", "*", "*", "F"],
            # ["0110*", "*", "*", "*", "*", "G"],
            # ["0111*", "*", "*", "*", "*", "H"],
            # ["1111*", "*", "*", "*", "*", "I"],
            # # ["0*", "1*", "*", "*", "*", "C"],
            # ["10101010*", "1010101010101010*", "1010101010101010*", "10101010101010101010101010101010*", "10101010101010101010101010101010*", "C"],
            ["*", "*", "*", "*", "*", "default"],
        ]
        random.seed(31417)
        packetList = [self.packets() for _ in range(10000)]
        packetList = [
            ["11111111", "1111111111111111", "1111111111111111", "11111111111111111111111111111111", "11111111111111111111111111111111"],
            ["00000000", "0000000000000000", "0000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000"],
        #     # ["11111100", "1111111111111100", "1111111111111100", "11111111111111111111111111111100", "11111111111111111111111111111100"],
        #     ["10100101", "1101111010101101", "1011101010111110", "11000000111111111110111000000000", "00001111111100011100111000000000"],
        #     # ["11111111", "1111111111111111", "1111111111111111", "11111111111111111111111111111111", "11111111111111111111111111111111"],
        #     # ["00000001", "0000000000000010", "0000000000000011", "00000000000000000000000000000100", "00000000000000000000000000000101"],
        #     # ["10101010", "1010101010101010", "1010101010101010", "10101010101010101010101010101010", "10101010101010101010101010101010"],
        ]
        temp_packetList = []

        for i in range(100):
            temp_packetList.append(packetList[i % len(packetList)])

        packetList = temp_packetList
        # logging.debug("Rule list: " + str(packetList))

        logging.debug("Rule list: ")
        file = open("hardware/sim/blueprint/cuckoo_hash/rule_list.txt", "w")
        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)
            file.write(str(rule) + "\n")
        file.close()

        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)

        file_names = [
            "hardware/sim/blueprint/protocol.txt",
            "hardware/sim/blueprint/srcport.txt",
            "hardware/sim/blueprint/dstport.txt",
            "hardware/sim/blueprint/srcip.txt",
            "hardware/sim/blueprint/dstip.txt",
        ]
        length_list = ["02X", "04X", "04X", "08X", "08X"]

        for length, filename in enumerate(file_names):
            file = open(filename, "w")
            for packet in packetList:
                file.write(format(int(packet[length], 2), length_list[length]) + "\n")
            file.close()
        # ((str(format(0, '02X')) + str(format(0, '04X')) + str(format(0, '08X'))+"\n"))
        # self.treeList[4].drawGraph(html=True)
        for rule in self.policyBuilder.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        self.policyBuilder.writeCodewords()

        self.hashTable.defualtRule = (["*"] * self.numberOfTrees) + ["default"]

        self.aclBuilder = ACLbuilder.ACLBuilder(
            self.treeList, self.policyBuilder, self.hashTable
        )
        self.aclBuilder.buildACL()
        self.aclBuilder.treeToVHDL(self.aclBuilder.treeList[0])
        self.aclBuilder.programCuckooHashTable(self.hashTable)

    def test_RulelistforRandomTest(self):
        self.treeList = []
        self.init3Trees(5, [8, 16, 16, 32, 32])

        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.hashTable = CuckooHashTable.CuckooHashTable()
        random.seed(31416)
        # Protocol       #Src port           #Dst Port           #SrcIP                              #dstIP
       
        # ruleList = [self.rules() for _ in range(4)]
        # ruleList.append(["*", "*", "*", "*", "*", "default"])
        
        
        packetList = [self.packets() for _ in range(10000)]

        ruleList = [
            ["1*", "*", "*", "*", "*", "A"],
            ["0*", "*", "*", "*", "*", "B"],
            # ["00000000*", "0000000000000000*", "0000000000000000*", "0000000000000000*", "0000000000000000*", "B"],
            # ["10101010*", "1010101010101010*", "1010101010101010*", "10101010101010101010101010101010*", "10101010101010101010101010101010*", "C"],
            ["*", "*", "*", "*", "*", "default"],
        ]
        # logging.debug("Rule list: ")
        # for rule in ruleList:
        #     logging.debug(rule)

        # logging.debug("Packet List: ")
        # for rule in packetList:
        #     logging.debug(rule)



        logging.debug("Rule list: " + str(packetList))
        logging.debug("Rule list: ")
        file = open("hardware/sim/blueprint/cuckoo_hash/rule_list.txt", "w")
        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)
            file.write(str(rule) + "\n")
        file.close()

        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)

        file_names = [
            "hardware/sim/blueprint/protocol.txt",
            "hardware/sim/blueprint/srcport.txt",
            "hardware/sim/blueprint/dstport.txt",
            "hardware/sim/blueprint/srcip.txt",
            "hardware/sim/blueprint/dstip.txt",
        ]
        length_list = ["02X", "04X", "04X", "08X", "08X"]

        for length, filename in enumerate(file_names):
            file = open(filename, "w")
            for packet in packetList:
                file.write(format(int(packet[length], 2), length_list[length]) + "\n")
            file.close()
        # ((str(format(0, '02X')) + str(format(0, '04X')) + str(format(0, '08X'))+"\n"))

        for rule in self.policyBuilder.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        self.policyBuilder.writeCodewords()

        self.hashTable.defualtRule = (["*"] * self.numberOfTrees) + ["default"]

        self.aclBuilder = ACLbuilder.ACLBuilder(
            self.treeList, self.policyBuilder, self.hashTable
        )
        self.aclBuilder.buildACL()
        self.aclBuilder.treeToVHDL(self.aclBuilder.treeList[0])
        self.aclBuilder.programCuckooHashTable(self.hashTable)

        for packet in packetList:
            logging.debug(self.hashTable.lookup(self.policyBuilder.retriveCodeword(packet)))

    def test_RulelistforRandomTest(self):
        self.treeList = []
        self.init3Trees(5, [8, 16, 16, 32, 32])

        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.hashTable = CuckooHashTable.CuckooHashTable()
        random.seed(31416)
        # Protocol       #Src port           #Dst Port           #SrcIP                              #dstIP
       
        # ruleList = [self.rules() for _ in range(4)]
        # ruleList.append(["*", "*", "*", "*", "*", "default"])
        
        
        # packetList = [self.packets() for _ in range(10000)]

        ruleList = [
            # ["11111111*", "*", "*", "*", "*", "A"],
            # ["00000000*", "*", "*", "*", "*", "B"],
            ["11111111*", "1111111111111111*", "1111111111111111*", "11111111111111111111111111111111*", "11111111111111111111111111111111*", "A"],

            ["00000000*", "0000000000000000*", "0000000000000000*", "00000000000000000000000000000000*", "00000000000000000000000000000000*", "B"],
            # ["10101010*", "1010101010101010*", "1010101010101010*", "10101010101010101010101010101010*", "10101010101010101010101010101010*", "C"],
            ["*", "*", "*", "*", "*", "default"],
        ]
        # logging.debug("Rule list: ")
        # for rule in ruleList:
        #     logging.debug(rule)

        # logging.debug("Packet List: ")
        # for rule in packetList:
        #     logging.debug(rule)


        packetList = [
            ["11111111", "1111111111111111", "1111111111111111", "11111111111111111111111111111111", "11111111111111111111111111111111"],
            ["00000000", "0000000000000000", "0000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000"],
            # ["01000000", "0000000000000000", "0000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000"],
            # ["10000000", "0000000000000000", "0000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000"],
            # ["10100101", "1101111010101101", "1011101010111110", "11000000111111111110111000000000", "00001111111100011100111000000000"],
            # ["11111111", "1111111111111111", "1111111111111111", "11111111111111111111111111111111", "11111111111111111111111111111111"],
            # ["00000001", "0000000000000010", "0000000000000011", "00000000000000000000000000000100", "00000000000000000000000000000101"],
            # ["10101010", "1010101010101010", "1010101010101010", "10101010101010101010101010101010", "10101010101010101010101010101010"],
        ]
        temp_packetList = []

        for i in range(100):
            temp_packetList.append(packetList[i % len(packetList)])

        logging.debug("Rule list: " + str(packetList))
        logging.debug("Rule list: ")
        file = open("hardware/sim/blueprint/cuckoo_hash/rule_list.txt", "w")
        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)
            file.write(str(rule) + "\n")
        file.close()

        for rule in ruleList:
            logging.debug("Rule in for loop: " + str(rule))
            self.policyBuilder.insertRule(rule)

        file_names = [
            "hardware/sim/blueprint/protocol.txt",
            "hardware/sim/blueprint/srcport.txt",
            "hardware/sim/blueprint/dstport.txt",
            "hardware/sim/blueprint/srcip.txt",
            "hardware/sim/blueprint/dstip.txt",
        ]
        length_list = ["02X", "04X", "04X", "08X", "08X"]

        for length, filename in enumerate(file_names):
            file = open(filename, "w")
            for packet in packetList:
                file.write(format(int(packet[length], 2), length_list[length]) + "\n")
            file.close()
        # ((str(format(0, '02X')) + str(format(0, '04X')) + str(format(0, '08X'))+"\n"))

        

        for rule in self.policyBuilder.previousRuleTuple:
            self.hashTable.insert(rule[1], rule[0])
        self.policyBuilder.writeCodewords()

        self.hashTable.defualtRule = (["*"] * self.numberOfTrees) + ["default"]

        self.aclBuilder = ACLbuilder.ACLBuilder(
            self.treeList, self.policyBuilder, self.hashTable
        )
        self.aclBuilder.buildACL()
        self.aclBuilder.treeToVHDL(self.aclBuilder.treeList[0])
        self.aclBuilder.programCuckooHashTable(self.hashTable)

        for packet in packetList:
            logging.debug(self.hashTable.lookup(self.policyBuilder.retriveCodeword(packet)))




    def rules(self):
        decision = ["alpha", "beta", "gamma", "iota", "jota", "kappa", "zeta", "eta"]
        entry = [
            self.random_bits_for_rule(8) + "*",
            self.random_bits_for_rule(16) + "*",
            self.random_bits_for_rule(16) + "*",
            self.random_bits_for_rule(32) + "*",
            self.random_bits_for_rule(32) + "*",
        ]
        entry.append(random.choice(decision))
        return entry

    def packets(self):
        entry = [
            self.random_bits(8),
            self.random_bits(16),
            self.random_bits(16),
            self.random_bits(32),
            self.random_bits(32),
        ]
        return entry


    def random_bits_for_rule(self, length):
        if random.random() < 0.2:
            return ""
            # return "*"
        else:
            return bin(random.randint(0, 2**length - 1))[2:].zfill(length)

    def random_bits(self, length):
        if random.random() < 0:  # 0.1
            return "*"
        else:
            return bin(random.randint(0, 2**length - 1))[2:].zfill(length)

    def init3Trees(self, tree_count=3, treeDepths=[16, 16, 16]):
        if len(treeDepths) != tree_count:
            raise ValueError("Length of treeDepths must match tree_count")

        self.treeList = [self.create_tree(depth) for depth in treeDepths]
        self.policyBuilder = PolicyBuilder.PolicyBuilder(self.treeList)
        self.policyBuilder.setSeed(311415)

    def create_tree(self, tree_depth):
        tree = policyTrieTree.PolicyTrieTree()
        tree.treeDepth = tree_depth
        return tree
