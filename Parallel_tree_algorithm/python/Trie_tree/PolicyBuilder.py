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
        self.codewordLength = 4 #16
        self.nextCodeword = 0
        self.treeDepth = 16
        self.store_inserted = []
        self.unique_sublists = set()
        self.store_prev_rules = set()
        self.store_rules = []

    def insertRuleIntoTree(self, rule, tree):
        ruleCodeword = ""
        for i, tree in enumerate(self.treeList):
            exists, codeword = tree.getCodeword(rule[i])
            if not exists:
                codeword = self.generateCodeword(self.codewordLength +2) #Maybe +2???
            logging.debug(f"codeword: {codeword} rule: {rule[i]} exists: {exists} ")
            ruleCodeword += codeword
            tree.insert(rule[i], codeword)
        return ruleCodeword

    def createIntersectionCodeword(self, output_rule):
        intersection_codeword = ""
        for i, tree in enumerate(self.treeList):
            exists, temp_codeword = tree.getCodeword(output_rule[i])
            if not exists:
                intersection_codeword += self.generateCodeword(self.codewordLength +2)
            intersection_codeword += temp_codeword
        return intersection_codeword

    def combine_2d_lists(self, list_2d):
        # result = []
        # sublist_len = len(list_2d[0])

        # def recursive_append(res_list, tmp_list, depth):
        #     if depth == sublist_len:
        #         res_list.append(list(tmp_list))
        #         return
        #     for i in range(len(list_2d)):
        #         tmp_list[depth] = list_2d[i][depth]
        #         recursive_append(res_list, tmp_list, depth + 1)

        # recursive_append(result, [0] * sublist_len, 0)
        # return result

        # result = []
        # Determine the length of the first sublist to decide the operation
        # sublist_len = len(list_2d[0])

        # if sublist_len == 2:
        #     for i in range(len(list_2d)):
        #         for j in range(len(list_2d)):
        #             new_sublist = (list_2d[i][0], list_2d[j][1])
        #             result.append(list(new_sublist))

        # elif sublist_len == 3:
        #     for i in range(len(list_2d)):
        #         for j in range(len(list_2d)):
        #             for k in range(len(list_2d)):
        #                 new_sublist = (list_2d[i][0], list_2d[j][1], list_2d[k][2])
        #                 result.append(list(new_sublist))

        # return result

        sublist_len = len(list_2d[0])

        if sublist_len == 2:
            return [
                [list_2d[i][0], list_2d[j][1]]
                for i in range(len(list_2d))
                for j in range(len(list_2d))
            ]

        elif sublist_len == 3:
            return [
                [list_2d[i][0], list_2d[j][1], list_2d[k][2]]
                for i in range(len(list_2d))
                for j in range(len(list_2d))
                for k in range(len(list_2d))
            ]

        return []

    def combinations(self, inlist):
        # list_of_lists = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        # list_of_lists = [['12', '15'], ['5', '7']]#, 6], [7, 8, 9]]
        permutation_cases = list(
            itertools.permutations(range(len(inlist)), 2)
        )  # len(inlist) - 1))
        select_from = list(itertools.combinations(range(len(inlist)), len(inlist)))

        all_possibility = []
        for elem in inlist:
            all_possibility.append(elem)
        for selecting_index in select_from:
            selected = [inlist[i] for i in selecting_index]
            cases = list([selected[k][i] for i, k in enumerate(comb)]for comb in permutation_cases)
            for item in cases:
                all_possibility.append(item)
        # print(all_possibility)
        return all_possibility

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

    def contains_star_and_digit(self, s):
        return bool(re.search(r"\d+\*", s))

    def account_for_old_rules(self, old_rules, new_rule):
        logging.debug("acc for old rule ")
        permutations = []
        for rule_index, rule in enumerate(old_rules):
            logging.debug("New rule is still: " + str(new_rule))
            logging.debug(
                "_____Curr old rule: " + str(rule) + " rule index: " + str(rule_index)
            )
            temp = rule.copy()
            temparr = []
            result = []
            if temp.__contains__("*") or any(
                self.contains_star_and_digit(item) for item in temp
            ):
                currperm = [x for x in rule if x.isdigit() or (("*" in x) and x.split("*")[0].isdigit())]

                for i, field in enumerate(rule):
                    temp = rule.copy()
                    logging.debug("Temp is equal to: " + str(temp))
                    if field == "*":
                        temp[i] = new_rule[i]
                        if temp != rule:
                            if tuple(temp[:-1]) not in self.store_prev_rules:
                                logging.debug("added temp in *: " + str(temp))
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
                        logging.debug("Field is in between range?: " + str(new_rule[i]))
                        logging.debug(int(field[0].ljust(self.codewordLength, "0"), 2))

                        if (
                            self.contains_star_and_digit(new_rule[i])
                            or new_rule[i] == "*"
                        ):
                            logging.debug("new rule contains star and digit: ")
                            if len(new_rule[i]) != field:
                                logging.debug("lengths are different")
                                break

                        if new_rule[i] == "*":
                            logging.debug(
                                "new rule i == * "
                                + str(new_rule[i])
                                + " With "
                                + str(new_rule)
                                + " And rule: "
                                + str(rule)
                            )
                            # temp[i] = new_rule[i]
                            # #if temp.count('*') != self.ruleLength -1:
                            # logging.debug("adding rule in *: " + str(temp))
                            # logging.debug(self.ruleLength -1)
                            # permutations.append(temp)
                            continue  # THIS IS SUS

                        logging.debug(
                            int(new_rule[i])
                            <= int(field[0].ljust(self.codewordLength, "1"), 2)
                            and int(new_rule[i])
                            >= int(field[0].ljust(self.codewordLength, "0"), 2)
                        )
                        if int(new_rule[i]) <= int(
                            field[0].ljust(self.codewordLength, "1"), 2
                        ) and int(new_rule[i]) >= int(
                            field[0].ljust(self.codewordLength, "0"), 2
                        ):
                            logging.debug("In if at pos: " + str(i))
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

                if rule.count("*") > 1:
                    # Make combine_2d_lists able to take lists * > 0
                    logging.debug(
                        "count * > 1 before old: " + str(rule) + "new: " + str(new_rule)
                    )
                    # extended_rules = old_rules + [new_rule]
                    # rest_rules_elements = [
                    #     extended_rules[i][:-1]
                    #     for i in range(rule_index + 1, len(extended_rules))
                    # ]

                    # for rest in reversed(self.store_inserted): #rest_rules_elements:
                    for rest in self.store_inserted:  # rest_rules_elements:
                        wildcard_indices = [
                            i for i, element in enumerate(temp) if element == "*"
                        ]  # or self.contains_star_and_digit(element)]
                        # wildcard_indices = [0,1,2]
                        range_indices = [
                            i
                            for i, element in enumerate(temp)
                            if "*" in element
                            and any(char.isdigit() for char in element)
                        ]

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
                        # if len(wildcard_indices) >= 2:
                        min_value, max_value = (
                            0,
                            self.ruleLength - 2,
                        )  # max(wildcard_indices)

                        # Create a list of all numbers between the minimum and maximum values
                        all_numbers = list(range(min_value, max_value + 1))

                        # Find the missing numbers using a list comprehension
                        missing_numbers = [
                            num for num in all_numbers if num not in wildcard_indices
                        ]

                        logging.debug("Missing nums: " + str(missing_numbers))
                        if missing_numbers:
                            logging.debug(
                                "rule[missingnums]: " + str(rule[missing_numbers[0]])
                            )
                            logging.debug("old rule: " + str(rule))
                            logging.debug("new rule: " + str(new_rule))
                            # rule here or rest...
                            if (
                                self.contains_star_and_digit(rule[missing_numbers[0]])
                                and new_rule[missing_numbers[0]] != "*"
                                and not self.contains_star_and_digit(
                                    new_rule[missing_numbers[0]]
                                )
                            ):
                                logging.debug("fields:")
                                fieldmax = int(
                                    rule[missing_numbers[0]]
                                    .split("*")[0]
                                    .ljust(self.codewordLength, "1"),
                                    2,
                                )
                                fieldmin = int(
                                    rule[missing_numbers[0]]
                                    .split("*")[0]
                                    .ljust(self.codewordLength, "0"),
                                    2,
                                )
                                logging.debug(
                                    "rule missing num: "
                                    + str(new_rule[missing_numbers[0]])
                                )
                                logging.debug(
                                    "fieldmax: "
                                    + str(fieldmax)
                                    + " min: "
                                    + str(fieldmin)
                                )
                                if (
                                    int(new_rule[missing_numbers[0]]) <= fieldmax
                                    and int(new_rule[missing_numbers[0]]) >= fieldmin
                                ):
                                    wildcard_indices.insert(
                                        missing_numbers[0], missing_numbers[0]
                                    )

                        logging.debug(
                            "WILDCARD INDICIES after if: " + str(wildcard_indices)
                        )
                        # wildcard_indices = [0,1,2]
                        # for rest in rest_rules_elements:
                        temparr.append([rest[i] for i in wildcard_indices])
                        # Something with the wildcards and this combine thing not getting the right result

                    logging.debug("temparr Before:")
                    logging.debug(temparr)

                    temparr = self.combine_2d_lists(temparr)  # generate combinations
                    # temparr = self.combinations(temparr)
                    logging.debug("temparr AFTer::")
                    logging.debug(temparr)

                if temparr and currperm:
                    # index_of_digit = self.find_first_digit_index(rule)
                    # logging.debug("index_of digit: " +str(index_of_digit))

                    result2 = self.subsetw_ranges(rule)
                    logging.debug(result2)
                    if result2:
                        result2 = result2[0]
                    logging.debug("result 2: " + str(result2))

                    for i, comb in enumerate(temparr):
                        result = rule.copy()  # Should be every comb in the prev rule

                        for i, value in enumerate(comb):
                            result[wildcard_indices[i]] = value
                            if result2:
                                # if value != '*':
                                result2[wildcard_indices[i]] = value

                        if tuple(result[:-1]) not in self.store_prev_rules:
                            logging.debug("Adding rule: " + str(result))
                            # if result[:-1]
                            permutations.append(result)
                            if result2:
                                if result2[:-1] != ["*", "*", "*"]:
                                    logging.debug("Adding rule2: " + str(result2))
                                    permutations.append(result2)

        logging.debug("Final perms: " + str(permutations))
        return permutations

    def insert_stars_in_between(self, old_rules, new_rule):
        permutations = []
        for i, value in enumerate(new_rule):  # Insert eg * 19 and 64 *
            if value == "*":
                for old_rule in old_rules:
                    temp = new_rule.copy()
                    temp[i] = old_rule[i]
                    if tuple(temp[:-1]) not in self.store_prev_rules:
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

        # permutations.extend(self.account_for_new_rule(old_rules, new_rule))

        # logging.debug("From products: ")
        # logging.debug(permutations)

        permutations.extend(self.insert_stars_in_between(old_rules, new_rule))

        permutations.append(new_rule)

        permutations = self.remove_duplicate_elements(permutations)  # duplikater
        return permutations

    def subset(self, rule):
        for prevrules in self.store_inserted:
            if all(
                prev == "*" or prev == curr
                for prev, curr in zip(prevrules[:-1], rule[:-1])
            ):
                logging.debug("prevrule: " + str(prevrules))
                logging.debug("This is subset?" + str(rule))
                return True

    def subsetw_ranges(self, rule):
        ruels = []
        temp = []
        logging.debug("printing pre_rules in subranges: " + str(self.store_rules))
        # for elem in self.store_rules:
        for prevrules in self.store_rules:
            if prevrules == rule:
                continue
            logging.debug("PLS VIRK: " + str(prevrules))
            # if prevrules == rule:
            #     return
            if self.subsetwrange_helper(prevrules, rule):
                prevrules[-1] = rule[-1]
                temp = rule
                #ruels.append(prevrules)
                ruels.append(temp)
                logging.debug("We return in subwrange: " + str(ruels))
            # logging.debug("This possibly subset w range. Prevrule: " + str(prevrules))
            # if prevrules == rule:
            #     return
            # for prev, curr in zip(prevrules[:-1], rule[:-1]):
            #     if not self.contains_star_and_digit(curr):
            #         logging.debug("Contains 1010* prev: " + str(prev))
            #         fieldmax = int(prev.split("*")[0].ljust(self.codewordLength, "1"),2,)
            #         fieldmin = int(prev.split("*")[0].ljust(self.codewordLength, "0"),2,)
            #         if (int(curr) <= fieldmax and int(curr) >= fieldmin):
            #             logging.debug("This field be a subset of prev rules. curr: " +str(curr))
            #             #logging.debug("so this prevrule returned: " +str(prevrules))
            #             ruels.append(prevrules)
            # logging.debug("We return in subwrange: " + str(ruels))
        return ruels

    def subsetwrange_helper(self, supert, rule):
        for prev, curr in zip(supert, rule):
            # if prev == "*" or prev == curr:
            #     return True
            logging.debug("checking sub for: " + str(supert) + "vs: " + str(rule))

            # if prev == "*" and curr != "*":
            #     logging.debug("Prev is super since it is *")
            #     return True
            if (not self.contains_star_and_digit(prev) and self.contains_star_and_digit(curr) and curr != "*" and prev != "*"):
                logging.debug("in first if prev: " + str(prev) + " curr: " + str(curr))
                fieldmax = int(curr.split("*")[0].ljust(self.codewordLength, "1"),2,)
                fieldmin = int(curr.split("*")[0].ljust(self.codewordLength, "0"),2,)
                if int(prev) <= fieldmax and int(prev) >= fieldmin:
                    logging.debug("rule is subset of an old rule: "+ str(supert)+ "rule: "+ str(rule))
                    return True

            if self.contains_star_and_digit(prev) and self.contains_star_and_digit(curr):
                if (len(prev.split("*")[0]) == len(curr.split("*")[0]) and prev.split("*")[0] != curr.split("*")[0]):
                    logging.debug("rules cannot be subset: " + str(supert) + "rule: " + str(rule))
                    return False

    def insertRule(self, rule):
        # rule = [self.to_binary_if_not_already(x) if x.isdigit() else x for x in rule]
        if rule.count("*") == self.ruleLength - 1:
            logging.debug("rule count * == 3: " + str(rule))
            rule_codeword = self.insertRuleIntoTree(rule, self.treeList)
            self.previousRuleTuple.append((rule, rule_codeword))
            logging.debug("Returned cus default")
            # return

        if tuple(rule[:-1]) in self.store_prev_rules:
            logging.debug("inserted rule in already inserted or a perm")
            return

        # for prevrules in self.store_inserted:  # TODO: Should add for ranges too
        #     # logging.debug("prevrules: " + str(prevrules))
        #     if all(prev == "*" or prev == curr for prev, curr in zip(prevrules[:-1], rule[:-1])):
        #         logging.debug("This is subset?" + str(rule))
        #         return
        if self.subset(rule):
            logging.debug("We aint gonn insert u cus of subset..." + str(rule))
            return

        rule = [
            str(int(element[:-1], 2))
            if (
                len(element) == self.codewordLength + 1
                and element[-1] == "*"
                and element[:-1].isdigit()
            )
            else element
            for element in rule
        ]
        logging.debug("_______ New inserted rule ______:" + str(rule))

        # elif self.ruleIsSubset(rule):
        #     logging.debug("Inserted rule is subset.. Return" + str(rule))
        #     return

        self.store_inserted.append(rule)

        rule_codeword = self.insertRuleIntoTree(rule, self.treeList)

        if not self.previousRuleTuple:
            self.previousRuleTuple.append((rule, rule_codeword))
            self.store_prev_rules.add(tuple(rule[:-1]))
            self.store_rules.append(rule)
            logging.debug("First rule. INSERT. Nothing more")
            return

        rule_permutations = self.generate_permutations(self.store_inserted, rule)
        # logging.debug("prevrule0: " + str(self.previousRuleTuple))
        # logging.debug("prev inserted: " + str(self.store_inserted))
        # rule_permutations = self.generate_permutations(self.previousRuleTuple[0][0], rule)

        for output_rule in rule_permutations:
            intersection_codeword = self.createIntersectionCodeword(output_rule)
            self.previousRuleTuple.append((output_rule, intersection_codeword))
            self.store_prev_rules.add(tuple(output_rule[:-1]))
            self.store_rules.append(rule)

        # logging.debug("prevRule tuple!! ")
        # for perms in self.previousRuleTuple:
        #     logging.debug(perms[0])

        # logging.debug("store prevrule tuple!! ")
        # for perms in self.store_prev_rules:
        #     logging.debug(perms)

        logging.debug("Store inserted tuple!! ")
        for ins in self.store_inserted:
            logging.debug(ins)

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
