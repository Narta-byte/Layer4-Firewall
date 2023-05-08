import random
import logging
import time
import re


class PolicyBuilder:
    def __init__(self, treeList):
        self.treeList = treeList
        self.ruleLength = len(treeList) + 1
        self.previousRuleTuple = []
        self.ruleCodeWord = ""
        self.codewordLength = 16
        self.nextCodeword = 0
        self.treeDepth = 16
        self.store_inserted = []

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
        # result = []
        # for sublist1 in list_2d:
        #     first_element = sublist1[indexes[0]]
        #     for sublist2 in list_2d:
        #         result.append([first_element, sublist2[indexes[1]]])
        # return result

        result = []
        unique_sublists = set()
        for sublist1 in list_2d:
            first_element = sublist1[indexes[0]]
            for sublist2 in list_2d:
                new_sublist = (first_element, sublist2[indexes[1]])
                if new_sublist not in unique_sublists:
                    unique_sublists.add(new_sublist)
                    result.append(list(new_sublist))
        logging.debug("Done insertslists")
        logging.debug(result)
        return result

    def combine_2d_lists(self, list_2d):
        # if len(list_2d) > 1:
        # result = [
        #     [sublist1[0], sublist2[1]] for sublist1 in list_2d for sublist2 in list_2d
        # ]
        # return result

        logging.info("Combining:")
        # if len(list_2d) > 1:
        unique_sublists = set()
        result = []

        for i, sublist1 in enumerate(list_2d):
            for sublist2 in list_2d[i:]:
                new_sublist = (sublist1[0], sublist2[1])
                if new_sublist not in unique_sublists:
                    unique_sublists.add(new_sublist)
                    result.append(list(new_sublist))

        logging.info("Done lists:")
        logging.debug(result)
        return result

    def remove_duplicate_elements(self, array):
        unique_elements = []
        seen = {}

        logging.debug("Removed elements:")
        for element in array:
            key = tuple(element[:3]) if isinstance(element, list) else element[:3]
            if key not in seen:
                unique_elements.append(element)
                seen[key] = True
            else:
                logging.debug(element)

        return unique_elements

    def find_first_digit_index(self, sequence):
        try:
            logging.debug(
                "find_first_digit_index: "
                + str(
                    next(
                        index
                        for index, element in enumerate(sequence)
                        if str(element).isdigit()
                    )
                )
            )
            return next(
                index
                for index, element in enumerate(sequence)
                if str(element).isdigit()
            )
        except StopIteration:
            logging.debug("Found")
            return None

    def contains_star_and_digit(self, s):
        return "*" in s and any(char.isdigit() for char in s)

    def account_for_old_rules(self, old_rules, new_rule):
        logging.debug("acc for old rule ")
        permutations = []
        for rule_index, rule in enumerate(old_rules):
            temp = rule.copy()
            temparr = []
            result = []
            if temp.__contains__("*"):
                # wildcard_indices = [
                #     i for i, element in enumerate(temp) if element == "*"
                # ]  # For new * rule
                wildcard_indices = [
                    i for i, element in enumerate(temp) if element == "*"
                ]  # or self.contains_star_and_digit(element)]

                range_indices = [
                    i
                    for i, element in enumerate(temp)
                    if "*" in element and any(char.isdigit() for char in element)
                ]

                currperm = [x for x in rule if x.isdigit()]
                logging.debug(
                    "Wildcard indicies for rule old rule: "
                    + str(rule)
                    + "\nIs: "
                    + str(wildcard_indices)
                    + "\nSubrange indecies: "
                    + str(range_indices)
                    + "\nwholenum is: "
                    + str(currperm)
                )
                for i, field in enumerate(rule):
                    temp = rule.copy()
                    if field == "*":
                        temp[i] = new_rule[i]
                        logging.debug("temp in *: " + str(temp))
                        permutations.append(temp)
                        # continue
                    if self.contains_star_and_digit(field):
                        logging.debug("This contains star and digit: " + str(field))
                        field = field.split("*")
                        logging.debug("This contains digit: " + str(field[0]))
                        logging.debug(
                            "This contains digit max: "
                            + str(int(field[0].ljust(self.codewordLength, "1"), 2))
                        )
                        logging.debug(
                            "This contains digit min: "
                            + str(int(field[0].ljust(self.codewordLength, "0"), 2))
                        )
                        # logging.debug(new_rule[i] < str(int(field[0].ljust(self.codewordLength, "1"), 2)) and new_rule[i] > str(int(field[0].ljust(self.codewordLength, "0"), 2)))
                        if new_rule[i] < str(
                            int(field[0].ljust(self.codewordLength, "1"), 2)
                        ) and new_rule[i] > str(
                            int(field[0].ljust(self.codewordLength, "0"), 2)
                        ):
                            logging.debug("In if at: " + str(i))
                            logging.debug(
                                "Field is in between range: " + str(new_rule[i])
                            )
                            logging.debug(temp)
                            temp[i] = new_rule[i]
                            logging.debug(
                                "adding: " + str(temp) + " because of subrange"
                            )
                            permutations.append(temp)
                            logging.debug("Perms: " + str(permutations))
                            # break
                            # continue
                    logging.debug("Perms in loop: " + str(permutations))

                logging.debug("adding: " + str(temp) + " because of *")
                # permutations.append(temp)

                if rule.count("*") > 1:
                    # Make combine_2d_lists able to take lists * > 0
                    extended_rules = old_rules + [new_rule]
                    rest_rules_elements = [
                        extended_rules[i][:-1]
                        for i in range(rule_index + 1, len(extended_rules))
                    ]

                    for rest in rest_rules_elements:
                        temparr.append([rest[i] for i in wildcard_indices])
                    # logging.debug("temparr Before:")
                    # logging.debug(temparr)

                    temparr = self.combine_2d_lists(temparr)  # generate combinations
                    # logging.debug("temparr AFTer::")
                    # logging.debug((self.combine_2d_lists(temparr)))
                    # logging.debug(temparr)

                if temparr and currperm:
                    # index_of_digit = self.find_first_digit_index(rule)
                    # logging.debug("index_of digit: " +str(index_of_digit))

                    for i, comb in enumerate(temparr):
                        result = rule.copy()

                        for i, value in enumerate(comb):
                            result[wildcard_indices[i]] = value

                        logging.debug("Adding rule: " + str(result))
                        permutations.append(result)

        logging.debug("Final perms: " + str(permutations))
        return permutations

    def account_for_new_rule(self, old_rules, new_rule):
        logging.debug("Accounting for new rule")
        permutations = []
        wildcard_indices = [
            i for i, element in enumerate(new_rule) if element == "*"
        ]  # For new * rule
        currperm = [x for x in new_rule if x.isdigit()]  # Digit value
        # logging.debug("Combinations:")

        logging.debug(
            "Wildcard indicies for rule: "
            + str(new_rule)
            + "Is: " + str(wildcard_indices)
            + " currperm is: "
            + str(currperm)
        )

        if len(old_rules) > 1 and len(wildcard_indices) > 1:
            # logging.debug("index_of digit: " + str(next((index for index, element in enumerate(new_rule) if element.isdigit()))))
            # index_of_digit = next((index for index, element in enumerate(new_rule) if element.isdigit()))
            index_of_digit = next(index for index, element in enumerate(new_rule) if str(element).isdigit() or (('*' in element) and element.split('*')[0].isdigit()))
            # if index_of_digit is None:
            #     return None
            logging.debug("index of digit: " +str(index_of_digit))
            currperm = [x for x in new_rule if x.isdigit() or (('*' in x) and x.split('*')[0].isdigit())]
            logging.debug("currperm: " +str(currperm))

            combinations = self.combine_2d_lists_insert(old_rules, wildcard_indices)
            for comb in combinations:
                comb.insert(index_of_digit, currperm[0])
                comb.append(new_rule[-1])
                logging.debug("Combination adding: " + str(comb))
                permutations.append(comb)

        logging.debug("Perms for acc new rule: " + str(permutations))
        return permutations

    def insert_stars_in_between(self, old_rules, new_rule):
        permutations = []
        for i, value in enumerate(new_rule):  # Insert eg * 19 and 64 *
            if value == "*":
                for old_rule in old_rules:
                    temp = new_rule.copy()
                    temp[i] = old_rule[i]
                    logging.debug("Inserting starts in between: " + str(temp))
                    permutations.append(temp)
        return permutations

    def generate_permutations(self, old_rules, new_rule):
        permutations = []
        results = []
        if new_rule.count("*") == self.ruleLength - 1:
            permutations.append(new_rule)
            return permutations

        permutations.extend(self.account_for_old_rules(old_rules, new_rule))

        # logging.debug("from first:")
        # logging.debug(permutations)
        
        permutations.extend(self.account_for_new_rule(old_rules, new_rule))

        # logging.debug("From products: ")
        # logging.debug(permutations)

        permutations.extend(self.insert_stars_in_between(old_rules, new_rule))

        permutations.append(new_rule)

        permutations = self.remove_duplicate_elements(permutations)  # duplikater
        return permutations

    def is_binary(self, num):
        return all(digit == "0" or digit == "1" for digit in num)

    def to_binary_if_not_already(self, num):
        if not self.is_binary(num):
            return bin(int(num))[2:]  # .zfill(self.codewordLength)
        return num

    def insertRule(self, rule):
        # rule = [self.to_binary_if_not_already(x) if x.isdigit() else x for x in rule]
        logging.debug("_______ New inserted rule ______" + str(rule))

        if rule.count("*") == self.ruleLength - 1:
            rule_codeword = self.insertRuleIntoTree(rule, self.treeList)
            self.previousRuleTuple.append((rule, rule_codeword))
            # self.previousRulePrefixes.add(tuple(rule))
            logging.debug("Returned cus default")

        # elif self.ruleIsSubset(rule):
        #     logging.debug("Inserted rule is subset.. Return" + str(rule))
        #     return

        # for prevrules in self.previousRuleTuple:
        #     logging.debug("prevrules: " + str(prevrules[0]))
        #     if all(
        #         prev == "*" or prev == curr
        #         for prev, curr in zip(prevrules[0][:-1], rule)
        #     ):
        #         logging.debug("This rules?" + str(rule))
        #         return

        self.store_inserted.append(rule)

        rule_codeword = self.insertRuleIntoTree(rule, self.treeList)

        if not self.previousRuleTuple:
            self.previousRuleTuple.append((rule, rule_codeword))
            logging.debug("First rule. INSERT. Nothing more")
            return

        rule_permutations = self.generate_permutations(self.store_inserted, rule)

        for output_rule in rule_permutations:
            intersection_codeword = self.createIntersectionCodeword(output_rule)
            self.previousRuleTuple.append((output_rule, intersection_codeword))

        logging.debug("prevRule tuple!! ")
        for perms in self.previousRuleTuple:
            logging.debug(perms)

        logging.debug("Store inserted tuple!! ")
        for ins in self.store_inserted:
            logging.debug(ins)

    def ruleIsSubset(self, rule):
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

    def getRuleTuple(self):
        output = ""
        for rule in self.previousRuleTuple:
            output += str(rule[0]) + " " + rule[1] + "\n"
        return output

    def setSeed(self, seed):
        random.seed(seed)
