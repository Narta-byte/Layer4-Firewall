import random
import logging
import time
import re
import itertools


class PolicyBuilder:
    def __init__(self, treeList):
        self.treeList = treeList
        self.ruleLength = len(treeList) + 1
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        self.codewordLength = 16
        self.nextCodeword = 0
        self.treeDepth = 16
        self.previousRulePrefixes = (
            set()
        )  # Add this line to store previous rule prefixes
        self.tempRules = []

    def insertRuleIntoTree(self, rule, tree):
        ruleCodeword = ""
        for i, tree in enumerate(self.treeList):
            exists, codeword = tree.getCodeword(rule[i])
            if not exists:
                codeword = self.generateCodeword(self.codewordLength)
            logging.debug(f"codeword: {codeword} rule: {rule[i]} exists: {exists} ")
            ruleCodeword += codeword
            tree.insert(rule[i], codeword)
        return ruleCodeword

    def createIntersectionCodeword(self, output_rule):
        intersection_codeword = ""
        for i, tree in enumerate(self.treeList):
            exists, temp_codeword = tree.getCodeword(output_rule[i])
            if not exists:
                intersection_codeword += self.generateCodeword(self.codewordLength)
            intersection_codeword += temp_codeword
        return intersection_codeword

    def combine_2d_lists_insert(self, list_2d, indexes):
        # if len(indexes) == 1:
        #     return
        result = []
        for sublist1 in list_2d:
            first_element = sublist1[indexes[0]]
            for sublist2 in list_2d:
                result.append([first_element, sublist2[indexes[1]]])
        return result

    def combine_2d_lists(self, list_2d):
        if len(list_2d) > 1:
            result = []
            for sublist1 in list_2d:
                for sublist2 in list_2d:
                    result.append([sublist1[0], sublist2[1]])
            return result

    def remove_duplicate_elements(self, array):
        unique_elements = []
        seen = {}

        for element in array:
            key = tuple(element[:3]) if isinstance(element, list) else element[:3]

            if key not in seen:
                unique_elements.append(element)
                seen[key] = True

        return unique_elements

    def generate_permutations(self, old_rules, new_rule):
        permutations = []
        results = []
        if new_rule.count("*") == self.ruleLength - 1:
            permutations.append(new_rule)
            return permutations

        # if not new_rule.__contains__("*"):

        for rule_index, rule in enumerate(old_rules):
            temp = rule.copy()
            temparr = []
            if temp.__contains__("*"):
                wildcard_indices = [
                    i for i, element in enumerate(temp) if element == "*"
                ]  # For new * rule

                currperm = [x for x in rule if x.isdigit()]
                # logging.debug("currperm: " + str(currperm))
                for i, field in enumerate(rule):
                    if field == "*":
                        temp[i] = new_rule[i]
                permutations.append(temp)

                if (
                    rule.count("*") > 1
                ):  # Make combine_2d_lists able to take lists * > 0
                    extended_rules = old_rules + [new_rule]
                    rest_rules_elements = [
                        extended_rules[i][:-1]
                        for i in range(rule_index + 1, len(extended_rules))
                    ]
                    #    logging.debug("old rules: " + str(old_rules))
                    #   logging.debug("msg")
                    logging.debug(rest_rules_elements)
                    for rest in rest_rules_elements:
                        # logging.debug("rest:")
                        # logging.debug(rest)
                        temparr.append([rest[i] for i in wildcard_indices])

                    #                        logging.debug(temparr)

                    temparr = self.combine_2d_lists(temparr)
                    # print(self.combine_2d_lists(temparr))

                if temparr and currperm:
                    for i, comb in enumerate(temparr):
                        result = [None] * (len(new_rule) - 1)

                        for i, value in enumerate(comb):
                            result[wildcard_indices[i]] = value

                        index_of_digit = next(
                            (
                                index
                                for index, element in enumerate(rule)
                                if element.isdigit()
                            )
                        )  # FIX THIS
                        result[index_of_digit] = currperm[0]
                        result.append(rule[-1])
                        permutations.append(result)
                # permutations.append(new_rule)
        logging.debug("from first:")
        logging.debug(permutations)

        wildcard_indices = [
            i for i, element in enumerate(new_rule) if element == "*"
        ]  # For new * rule
        currperm = [x for x in new_rule if x.isdigit()]  # Digit value
        # print(wildcard_indices)
        logging.debug("Combinations:")
        # for combination in itertools.product(old_rules, repeat=len(wildcard_indices)):
        #     # print(combination)
        #     logging.debug(combination)
        #     temp_rule = list(new_rule)
        #     for i, index in enumerate(wildcard_indices):
        #         temp_rule[index] = combination[i][index]
        #     # if combination[-1].__contains__('*'):
        #     #     temp_rule[-1] = combination[-1][-1]
        #     # Check if the temp_rule is a subset of any old rules
        #     # logging.debug(temp_rule)
        #     permutations.append(temp_rule)

        if len(old_rules) > 1 and len(wildcard_indices) > 1:
            index_of_digit = next(
                (index for index, element in enumerate(new_rule) if element.isdigit())
            )
            currperm = [x for x in new_rule if x.isdigit()]
            # print(currperm)

            combinations = self.combine_2d_lists_insert(old_rules, wildcard_indices)
            for comb in combinations:
                comb.insert(index_of_digit, currperm[0])
                comb.append(new_rule[-1])
                permutations.append(comb)

        logging.debug("From products: ")
        logging.debug(permutations)

        for i, value in enumerate(new_rule):  # Insert eg * 19 and 64 *
            if value == "*":
                for old_rule in old_rules:
                    temp = new_rule.copy()
                    temp[i] = old_rule[i]
                    # results.append(temp)
                    permutations.append(temp)

        # permutations.append(results)
        permutations.append(new_rule)
        # permutations = self.remove_duplicate_elements(permutations)

        # for perm_rule in permutations:  # Set decision right
        #     for old_rule in old_rules:
        #         if all(old == "*" or old == curr for old, curr in zip(old_rule[:-1], perm_rule[:-1])):
        #             # print("Match found:", old_rule, perm_rule)
        #             perm_rule[-1] = old_rule[-1]

        # else:
        # print("No match found:", old_rule, perm_rule)
        # logging.debug("No matcho found!")
        permutations = self.remove_duplicate_elements(permutations)  # duplikater
        return permutations

    def insertRule(self, rule):
        if self.ruleIsSubset(rule):
            logging.debug("Inserted rule is subset.. Return" + str(rule))
            return

        if rule.count("*") == self.ruleLength - 1:
            rule_codeword = self.insertRuleIntoTree(rule, self.treeList)
            self.previousRuleTuple.append((rule, rule_codeword))
            # self.tempRules.append(rule)
            self.previousRulePrefixes.add(tuple(rule))
            logging.debug("Returned cus default")
            return

        # logging.debug("Check for subset manually")
        # for prevrules in self.previousRuleTuple:
        #     logging.debug("prevrules: " +str(prevrules[0]))
        #     if all(prev == '*' or prev == curr for prev, curr in zip(prevrules[0][:-1], rule)):
        #         logging.debug("This rules?" + str(rule))
        #         return

        rule_codeword = self.insertRuleIntoTree(rule, self.treeList)

        if not self.previousRuleTuple:
            self.previousRuleTuple.append((rule, rule_codeword))
            self.tempRules.append(rule)
            self.previousRulePrefixes.add(tuple(rule))
            logging.debug("First rule. INSERT. Nothing more")
            return

        # logging.debug("alle temp rules: ")
        # logging.debug(self.tempRules)
        rule_permutations = self.generate_permutations(self.tempRules, rule)

        # logging.debug("Output perms: ")
        # for rules in rule_permutations:
        #    logging.debug(rules)

        # logging.debug("prevRule tuple!! ")
        # for perms in self.previousRuleTuple:
        #     logging.debug(perms)

        logging.debug("Add codewords:")
        for output_rule in rule_permutations:
            intersection_codeword = self.createIntersectionCodeword(output_rule)
            self.previousRuleTuple.append((output_rule, intersection_codeword))
            self.tempRules.append(output_rule)

        logging.debug("prevRule tuple!! ")
        for perms in self.previousRuleTuple:
            logging.debug(perms)

    def ruleIsSubset(self, rule):
        # logging.debug("self.matches : " + str(self.matches(previousRule, currRule)))

        codeword = ""
        logging.debug("rule is subset: " + str(rule))
        rule = rule[: self.ruleLength - 1]

        for i, rule_value in enumerate(rule):
            exists, codewordSegment = self.treeList[i].getCodeword(rule_value)
            logging.debug(
                f"ruleissubset[{i}] = {rule_value} Exists{i}: {exists} subcode{i}: {codewordSegment} "
            )
            if exists:  # or codewordSegment != "0":
                # logging.debug("Exists: " str((exists) and codewordSegment)))
                codeword += str(codewordSegment)
            else:
                return False
        if codeword == "0" * (self.ruleLength - 1):
            return False
        logging.debug("rule is subset is True and codeword is " + str(codeword))
        return True

    def retriveCodeword(self, packet):
        codeword = ""
        logging.debug("Packet: " + str(packet))

        for i, packet_value in enumerate(packet):
            exists, codewordSegment = self.treeList[i].getCodeword(packet_value)
            logging.debug(
                f"packet[{i}] = {packet_value} Exists{i}: {exists} subcode{i}: {codewordSegment} "
            )
            if exists or ((not exists) and (codewordSegment != "")):
                codeword += str(codewordSegment)
            else:
                return None
        return codeword

    def generateCodeword(self, length):
        self.nextCodeword += 1
        return format(self.nextCodeword, f"0{length}b")

    def writeCodewords(self):  # Writing to "codewords.txt"
        file = open("codewords.txt", "w")
        for rule in self.previousRuleTuple:
            file.write(str(rule[0]) + " " + rule[1] + "\n")
        file.close()
        # rules_list = [list(rule) for rule in self.previousRulePrefixes]
        # file = open("codewords2.txt", "w")
        # for rules in self.previousRulePrefixes:
        #     file.write(str(rules[0]) + " " + str(rules[1]) + " " + str(rules[2]) + "\n")
        # file.close

    def getRuleTuple(self):
        output = ""
        for rule in self.previousRuleTuple:
            output += str(rule[0]) + " " + rule[1] + "\n"
        return output

    def setSeed(self, seed):
        random.seed(seed)


# def remove_duplicate_elements(array):
#     unique_elements = []

#     for element in array:
#         duplicate = False
#         for unique_element in unique_elements:
#             if element[:3] == unique_element[:3]:
#                 duplicate = True
#                 break

#         if not duplicate:
#             unique_elements.append(element)

#     return unique_elements
