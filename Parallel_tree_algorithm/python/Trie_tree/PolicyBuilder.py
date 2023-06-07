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
        self.codewordLength = 32
        self.codewordLength_for_tree = 32
        self.nextCodeword = 0
        self.treeDepth = 4
        self.store_inserted = []
        self.store_prev_rules = set()

        self.insert_packet_time = 0
        self.lookup_time = 0
        self.counter = 1

    def insertRuleIntoTree(self, rule, tree):
        ruleCodeword = ""
        for i, tree in enumerate(self.treeList):
            exists, codeword = tree.getCodeword(rule[i])
            if not exists:
                codeword = self.generateCodeword(self.codewordLength_for_tree)  # Maybe +2???
            logging.debug(f"codeword: {codeword} rule: {rule[i]} exists: {exists} ")
            ruleCodeword += codeword
            tree.insert(rule[i], codeword)
        return ruleCodeword

    def _duplicate_elements(self, array):
        unique_elements = []
        seen = {}

        logging.debug("removed elements:")
        for element in array:
            key = tuple(element[:-1]) if isinstance(element, list) else element[:-1]
            if key not in seen:
                unique_elements.append(element)
                seen[key] = True
            else:
                logging.debug(element)
        return unique_elements

    def combine_2d_lists(self, list_2d):
        if list_2d == []:
            logging.debug("Empty list return [[]]")
            return [[]]
        sublist_len = len(list_2d[0])
        logging.debug("sublist len: " + str(sublist_len))

        if sublist_len == 1:
            logging.debug("Returning input again")
            return list_2d

        elif sublist_len == 2:
            return [list(item)for item in set(tuple(sublist)for sublist in [[list_2d[i][0], list_2d[j][1]]for i in range(len(list_2d))for j in range(len(list_2d))])if list(item) != ["*", "*"] and len(item) == 2]

        elif sublist_len == 3:
            return [list(item) for item in set(tuple(sublist) for sublist in [[list_2d[i][0], list_2d[j][1], list_2d[k][2]] for i in range(len(list_2d)) for j in range(len(list_2d)) for k in range(len(list_2d))]) if list(item) != ["*", "*", "*"]]
            #return [list(item) for item in set(tuple(sublist) for sublist in [[list_2d[i][0], list_2d[j][1], list_2d[k][2]] for i in range(len(list_2d)) for j in range(len(list_2d)) for k in range(len(list_2d)) if list_2d[i][0] != '' and list_2d[j][1] != '' and list_2d[k][2] != '']) if list(item) != ['*', '*', '*']]
            #return [list(item) for item in set(tuple(item) for item in zip(*list_2d) if all(i != "" for i in item) and list(item) != ["*", "*", "*"])]


        elif sublist_len == 4:
            return [list(item)for item in set(tuple(sublist)for sublist in [[list_2d[i][0], list_2d[j][1], list_2d[k][2], list_2d[l][3]]for i in range(len(list_2d))for j in range(len(list_2d))for k in range(len(list_2d))for l in range(len(list_2d))])if list(item) != ["*", "*", "*", "*"] and len(item) == 4]

        elif sublist_len == 5:
            return [list(item)for item in set(tuple(sublist)for sublist in [[list_2d[i][0],list_2d[j][1],list_2d[k][2],list_2d[l][3],list_2d[m][4],]for i in range(len(list_2d))for j in range(len(list_2d))for k in range(len(list_2d))for l in range(len(list_2d))for m in range(len(list_2d))])if list(item) != ["*", "*", "*", "*", "*"] and len(item) == 5]

        ### ADD MORE ELIFs LIKE THIS IF YOU NEED MORE TREES!!!
        return []
    
    def remove_empty_indices(self, list_2d):
        return [[item for i, item in enumerate(sublist) if any(list_2d[j][i] for j in range(len(list_2d)))] for sublist in list_2d]

        non_empty_indices = {i for i in range(len(list_2d[0])) if any(sublist[i] != '' for sublist in list_2d)}
        # only keep these indices in all sublists
        return [[item for i, item in enumerate(sublist) if i in non_empty_indices] for sublist in list_2d]


    def account_for_old_rules(self, old_rules, new_rule):
        if new_rule.count("*") == self.ruleLength - 1:
            return []
        logging.debug("acc for old rule")
        permutations = []
        for rule_index, rule in enumerate(old_rules):
            logging.debug(" New rule is still: " + str(new_rule))
            logging.debug("_____Curr old rule: " + str(rule) + " rule index: " + str(rule_index))
            temp = rule.copy()
            temparr = []

            result = []
            if temp.__contains__("*") or any((item[0] == "0" or item[0] == "1") and item[-1] == "*" for item in temp):
                for i, field in enumerate(rule):
                    if rule == new_rule:  # Saves space in logg
                        continue
                    logging.debug("rule: "+ str(rule)+ " new rule: "+ str(new_rule)+ " i: "+ str(i))
                    temp = rule.copy()
                    if field == "*":
                        temp[i] = new_rule[i]
                        if temp != rule:
                            if tuple(temp[:-1]) not in self.store_prev_rules:
                                logging.debug("added temp in *: " + str(temp))
                                permutations.append(temp)  # needed for a single test
                        continue  # idk
                    if new_rule[i] == "*":
                        continue  # Maybe faster?
                    logging.debug("Perms in loop: " + str(permutations))

                for rest in self.store_inserted:
                    if rest == temp:
                        continue
                    temp = rule.copy()
                    logging.debug("this is curr temp: " + str(temp))
                    logging.debug("This is curr rest: " + str(rest))

                    wildcard_indices = [i for i, element in enumerate(temp) if element == "*"or (element[-1] == "*" and (element[0] == "1" or element[0] == "0") and rest[i].startswith(element[:-1]))]
                    if wildcard_indices == []:
                        continue

                    logging.debug("Wildcard indicies for rule old rule: "+ str(rule)+ "\nIs: "+ str(wildcard_indices)+ "\nwholenums ")  # in rule is: "+ str(currperm))

                    # temparr.append([rest[i] for i in wildcard_indices])
                    temparr.append([rest[i] if i in wildcard_indices else '' for i in range(len(rest) - 1)])
                    logging.debug("curr temp arr: " + str(temparr))

                logging.debug("temparr Before:")
                logging.debug(temparr)

                temparr = self.remove_empty_indices(temparr)

                logging.debug("temparr Before:")
                logging.debug(temparr)

                # temparr = [[item for item in sublist if item != ''] for sublist in temparr]
                temparr = self.combine_2d_lists(temparr)  # , wildcard_indices)  # generate combinations

                logging.debug("temparr AFTer::")
                logging.debug(temparr)

                logging.debug("This is rule: " + str(rule))
                for i, comb in enumerate(temparr):
                    result = rule.copy()  # Should be every comb in the prev rule
                    logging.debug("New one: " + str(result))
                    for q, j in enumerate(wildcard_indices):
                        # logging.debug("j: " + str(j) + " q: " + str(q))
                        # logging.debug("i: " + str(i))
                        # logging.debug("temparr ij: " +str(temparr[i]))
                        if temparr[i][q] == '':
                            logging.debug("comb == '' so skip")
                            continue

                        result[j] = temparr[i][q]
                    logging.debug("rule maybe adding: " + str(result))
                    if (tuple(result[:-1]) not in self.store_prev_rules):  # test packet 15 maybe append to store_inserted?
                        logging.debug("Adding rule: " + str(result))
                        permutations.append(result)

        logging.debug("Final perms!: " + str(permutations))
        return permutations

    def insert_stars_in_between(self, old_rules, new_rule):
        permutations = []
        if new_rule.count("*") == self.ruleLength - 1:
            return []
        for i, value in enumerate(new_rule):  # Insert eg * 19 and 64 *
            if value == "*":
                for old_rule in old_rules:
                    temp = new_rule.copy()
                    temp[i] = old_rule[i]
                    if (tuple(temp[:-1]) not in self.store_prev_rules and temp != new_rule):
                        logging.debug("Inserting starts in between: "+ str(temp)+ " from "+ str(old_rule))
                        permutations.append(temp)
        return permutations

    def generate_permutations(self, old_rules, new_rule):
        permutations = []

        permutations.extend(self.account_for_old_rules(old_rules, new_rule))
        permutations.extend(self.insert_stars_in_between(old_rules, new_rule))  # TODO: no real need for this, exept 2 tests

        permutations.append(new_rule)
        permutations = self._duplicate_elements(permutations)  # duplikater
        return permutations

    def is_subset(self, rule):
        for stored_rule in self.store_inserted:
            if all(stored_pattern == "*" or stored_pattern == current_pattern or (stored_pattern[0] in "01" and stored_pattern[-1] == "*" and current_pattern.startswith(stored_pattern[:-1])) for stored_pattern, current_pattern in zip(stored_rule[:-1], rule[:-1])):
                return True
        return False

    def insertRule(self, rule):
        start = time.time()
        if rule.count("*") == self.ruleLength - 1:
            logging.debug("rule count * == max: " + str(rule))
            rule_codeword = self.insertRuleIntoTree(rule, self.treeList)
            self.previousRuleTuple.append((rule, rule_codeword))
            logging.debug("Returned cus default")
            return

        if tuple(rule[:-1]) in self.store_prev_rules:
            logging.debug("inserted rule in already inserted or a perm")
            return

        rule = [str(bin(int(element[:-1], 2))[2:]) if (len(element) == self.codewordLength + 1 and element[-1] == "*" and element[:-1].isdigit()) else element for element in rule]
        logging.debug("_______ New inserted rule ______:" + str(rule))

        if self.is_subset(rule):
            logging.debug("We are the same subset..." + str(rule))
            return

        self.store_inserted.append(rule)
        rule_codeword = self.insertRuleIntoTree(rule, self.treeList)

        if not self.previousRuleTuple:
            self.previousRuleTuple.append((rule, rule_codeword))
            self.store_prev_rules.add(tuple(rule[:-1]))
            logging.debug("First rule. INSERT. Nothing more")
            return

        rule_permutations = self.generate_permutations(self.store_inserted, rule)

        for output_rule in rule_permutations:
            intersection_codeword = self.createIntersectionCodeword(output_rule)
            self.previousRuleTuple.append((output_rule, intersection_codeword))
            self.store_prev_rules.add(tuple(output_rule[:-1]))

        # logging.debug("store prevrule tuple!! ")
        # for perms in self.store_prev_rules:
        #     logging.debug(perms)

        end = time.time()
        self.insert_packet_time += end - start

        file_path = "len_previousRuleTuple.txt"
        file = open(file_path, "a")
        print(str(self.counter)+ ","+ str(len(self.previousRuleTuple))+ ","+ str(self.counter)+ ","+ str(self.insert_packet_time),file=file,)

        file.close()
        self.counter += 1
        logging.debug("Len of prev rule tuple " + str(len(self.previousRuleTuple)))
        logging.debug("Store time!!!: " + str(self.insert_packet_time))

    def retriveCodeword(self, packet):
        start = time.time()
        codeword = ""
        logging.debug("Packet: " + str(packet))

        for i, packet_value in enumerate(packet):
            exists, codewordSegment = self.treeList[i].getCodeword(packet_value)
            logging.debug(f"packet[{i}] = {packet_value} Exists{i}: {exists} subcode{i}: {codewordSegment} ")
            if exists or ((not exists) and (codewordSegment != "")):
                codeword += str(codewordSegment)
            else:
                return None
        end = time.time()
        self.lookup_time += end - start
        logging.debug("Lookup time in trees: " + str(self.lookup_time))
        return codeword

    def createIntersectionCodeword(self, output_rule):
        intersection_codeword = ""
        for i, tree in enumerate(self.treeList):
            exists, temp_codeword = tree.getCodeword(output_rule[i])
            if not exists:
                intersection_codeword += self.generateCodeword(self.codewordLength_for_tree)
            intersection_codeword += temp_codeword
        return intersection_codeword

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
