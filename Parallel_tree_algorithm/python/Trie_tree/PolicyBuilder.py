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
        self.codewordLength = 4
        self.codewordLength_for_tree = 32
        self.nextCodeword = 0
        self.treeDepth = 5
        self.store_inserted = []
        self.unique_sublists = set()
        self.store_prev_rules = set()

        self.insert_packet_time = 0
        self.lookup_time = 0
        self.pattern = re.compile(r"^[01]+\*$")
        self.counter = 0

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

    def contains_star_and_digit(self, s): #Check
        #return bool(re.match(r"^[01]+\*$", s))
        #return bool(self.pattern.match(s))
        if s[0] != '*' and s[-1] == '*':
            return True
        return False
        #return bool(re.search(r"\d+\*", s))
    
    def subsetrange(self, curr, value):
        if not self.contains_star_and_digit(curr):
            return True
        for currrule, val in zip(curr, value):
            if currrule == '*':
                return False
            if currrule != val:
                return True
        
                # 010*
                # 01010*

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
            return [list(item) for item in set(tuple(sublist) for sublist in [[list_2d[i][0], list_2d[j][1]] for i in range(len(list_2d)) for j in range(len(list_2d))]) if list(item) != ['*', '*'] and len(item) == 2]

        elif sublist_len == 3:
            return [list(item) for item in set(tuple(sublist) for sublist in [[list_2d[i][0], list_2d[j][1], list_2d[k][2]] for i in range(len(list_2d)) for j in range(len(list_2d)) for k in range(len(list_2d))]) if list(item) != ['*', '*', '*']]

        elif sublist_len == 4:
            return [list(item) for item in set(tuple(sublist) for sublist in [[list_2d[i][0], list_2d[j][1], list_2d[k][2], list_2d[l][3]] for i in range(len(list_2d)) for j in range(len(list_2d)) for k in range(len(list_2d)) for l in range(len(list_2d))]) if list(item) != ['*', '*', '*', '*'] and len(item) == 4]

        elif sublist_len == 5:
            return [list(item) for item in set(tuple(sublist) for sublist in [[list_2d[i][0], list_2d[j][1], list_2d[k][2], list_2d[l][3], list_2d[m][4]] for i in range(len(list_2d)) for j in range(len(list_2d)) for k in range(len(list_2d)) for l in range(len(list_2d)) for m in range(len(list_2d))]) if list(item) != ['*', '*', '*', '*', '*'] and len(item) == 5]

        ### ADD MORE ELIFs LIKE THIS IF YOU NEED MORE TREES!!!
        return []

    def insert_singletons(self, tempar, storear):
        if not storear:
            logging.debug("No singletons to insert.")
            return tempar
        result = []

        if tempar:  # If tempar is not empty
            for sublist in storear:
                for sublist2 in tempar:
                    modified_sublist = sublist2.copy()  # make a copy of the sublist from tempar
                    modified_sublist.insert(sublist[1], sublist[0])  # insert the element from storear at the specified position
                    logging.debug("Appending: " + str(modified_sublist))
                    result.append(modified_sublist)
        else:  # If tempar is empty
            for sublist in storear:
                temp = [''] * len(self.treeList)
                logging.debug("Appending0: " + str(sublist[0]))
                temp[sublist[1]] = sublist[0]
                result.append(temp)

        logging.debug("Returning in singoton: " + str(result))
        return result


    def account_for_old_rules(self, old_rules, new_rule):
        if new_rule.count("*") == self.ruleLength - 1:
            logging.debug("rule count * == ruleLength: " + str(new_rule))
            return []
        logging.debug("acc for old rule ")
        permutations = []
        for rule_index, rule in enumerate(old_rules):
            logging.debug(" New rule is still: " + str(new_rule))
            logging.debug("_____Curr old rule: " + str(rule) + " rule index: " + str(rule_index))
            temp = rule.copy()
            temparr = []
            
            result = []
            if temp.__contains__("*") or any(self.contains_star_and_digit(item) for item in temp):

                for i, field in enumerate(rule): # TODO: This loop could be deleted?
                    if rule != new_rule:
                        logging.debug("rule: " + str(rule) + " new rule: " + str(new_rule) + " i: " + str(i))
                    if rule == new_rule: #Saves space in logg
                        #logging.debug("rule in loop equal to inserted rule " )
                        continue
                    temp = rule.copy()
                    # logging.debug("Temp is equal to: " + str(temp))
                    # logging.debug("curr field in old: " + str(field) + " and curr  new: " + str(new_rule[i]))
                    if field == "*":
                        logging.debug("we change oldrule field: " + str(field) + " to " + str(new_rule[i]))
                        temp[i] = new_rule[i]

                        if temp != rule:
                            if tuple(temp[:-1]) not in self.store_prev_rules:
                                logging.debug("added temp in *: " + str(temp))
                                permutations.append(temp)
                        continue# idk
                    
                    if new_rule[i] == '*':
                        continue #Maybe faster?
                    logging.debug("New rule contains star and digit?: " + str(new_rule[i]))

                    if (field[0] == '0' or field[0] == '1') and field[-1] == '*':
                        #logging.debug("This contains star and digit: " + str(field))
                        field = field.split("*")
                        # logging.debug("This contains digit: " + str(field[0]))
                        # logging.debug("This contains digit max: "+ str(int(field[0].ljust(self.codewordLength, "1"), 2)))
                        # logging.debug("This contains digit min: "+ str(int(field[0].ljust(self.codewordLength, "0"), 2)))
                        # logging.debug("Field is in between range?: " + str(new_rule[i]))

                        if not self.contains_star_and_digit(new_rule[i]):
                            logging.debug("compare!:")
                            logging.debug("new_rule: " + str(new_rule[0]) + " and rule: " + str(field[0]))
                            logging.debug(int(new_rule[i])<= int(field[0].ljust(self.codewordLength, "1"), 2)and int(new_rule[i])>= int(field[0].ljust(self.codewordLength, "0"), 2))
                            #logging.debug(new_rule[i].startswith(field[0]))
                            #logging.debug(field[0].startswith(new_rule[i]))
                            #if new_rule[i].startswith(field[0]):
                            if int(new_rule[i]) <= int(field[0].ljust(self.codewordLength, "1"), 2) and int(new_rule[i]) >= int(field[0].ljust(self.codewordLength, "0"), 2):
                                logging.debug("In if at pos: " + str(i))
                                logging.debug(temp)
                                temp[i] = new_rule[i]
                                logging.debug("adding: " + str(temp) + " because of subrange")
                                #permutations.append(temp)
                                logging.debug("Also adding " + str(temp) + " to store inserted because we have to")
                                self.store_inserted.append(temp)
                                #arr[rule_index][i] = temp
                                #arr[rule_index] = temp
                                logging.debug("Perms: " + str(permutations))
                                # break
                                # continue

                    logging.debug("Perms in loop: " + str(permutations))

                storearr = []
                for rest in self.store_inserted:
                    if rest == temp:
                        continue
                    temp = rule.copy()
                    logging.debug("TEMP: " + str(temp) + " TEMP")
                    logging.debug("this is curr temp: " + str(temp))
                    logging.debug("This is curr rest: " + str(rest))

                    wildcard_indices = [i for i, element in enumerate(temp) if element == "*" 
                    or (element[-1] == '*' and (element[0] == '1' or element[0] == '0') and rest[i].startswith(element[:-1]))
                    ]

                    logging.debug("Wildcard indicies for rule old rule: "+ str(rule)+ "\nIs: "+ str(wildcard_indices)+ "\nwholenums ")#in rule is: "+ str(currperm))
                    #if wildcard_indices > 1 or wildcard_indices == 0:
                    temparr.append([rest[i] for i in wildcard_indices])
                    logging.debug("curr temp arr: "+ str(temparr))
                    
                    if len(temparr[-1]) == 1:
                        storearr.append([temparr[-1][0], wildcard_indices[0]])
                        

                temparr = [sublist for sublist in temparr if len(sublist) > 1]
                storearr = [list(x) for x in set(tuple(x) for x in storearr)]
                logging.debug("Store arr: " + str(storearr))
                logging.debug("temparr Before:")
                logging.debug(temparr)

                temparr = self.insert_singletons(temparr, storearr)

                temparr = [[item for item in sublist if item != ''] for sublist in temparr]
                logging.debug("temparr Before:")
                logging.debug(temparr)
                temparr = self.combine_2d_lists(temparr)#, wildcard_indices)  # generate combinations
                
                logging.debug("temparr AFTer::")
                logging.debug(temparr)

                logging.debug("This is rule: " + str(rule))
                # if not wildcard_indices:
                #     continue
                for i, comb in enumerate(temparr):
                    result = rule.copy()  # Should be every comb in the prev rule
                    logging.debug("New one: " + str(result))
                    #for i, value in enumerate(comb):
                    for q, j in enumerate(wildcard_indices):
                        # logging.debug("j: " + str(j))
                        # logging.debug("i: " + str(i))
                        # logging.debug("temparr ij: " +str(temparr[i]))

                        result[j] = temparr[i][q]
                    logging.debug("rule maybe adding: " +str(result))
                    if tuple(result[:-1]) not in self.store_prev_rules: #test packet 15maybe append to store_inserted?
                        logging.debug("Adding rule: " + str(result))
                        permutations.append(result)

        logging.debug("Final perms: " + str(permutations))
        return permutations


    def insert_stars_in_between(self, old_rules, new_rule):
        permutations = []
        #store = []
        if new_rule.count("*") == self.ruleLength - 1:
            #logging.debug("rule count * == ruleLength in insert: " + str(new_rule))
            return []
        #logging.debug("new_rule in stars: " + str(new_rule))
        for i, value in enumerate(new_rule):  # Insert eg * 19 and 64 *
            if value == "*" or self.contains_star_and_digit(value):
                for old_rule in old_rules:
                    #logging.debug("old rule in stars: " + str(old_rule) + " With new rule: " + str(new_rule) + " i: " + str(i))
                    if self.contains_star_and_digit(value):
                        if self.subsetrange(value, old_rule[i]):
                            #logging.debug("We here with " + str(value) + " and " + str(new_rule[i]))
                            continue
                    temp = new_rule.copy()
                    temp[i] = old_rule[i]
                    if tuple(temp[:-1]) not in self.store_prev_rules and temp != new_rule:
                        logging.debug("Inserting starts in between: " + str(temp) + " from " + str(old_rule))
                        permutations.append(temp)
        return permutations


    def generate_permutations(self, old_rules, new_rule):
        permutations = []

        permutations.extend(self.account_for_old_rules(old_rules, new_rule))
        permutations.extend(self.insert_stars_in_between(old_rules, new_rule)) # TODO: no real need for this, exept 2 tests

        permutations.append(new_rule)
        permutations = self._duplicate_elements(permutations)  # duplikater
        return permutations

    def subset(self, rule):
        for prevrules in self.store_inserted:
            if all(prev == "*" or prev == curr for prev, curr in zip(prevrules[:-1], rule[:-1])):
                logging.debug("prevrule: " + str(prevrules))
                logging.debug("This is subset?" + str(rule))
                return True

    def insertRule(self, rule):
        # rule = [self.to_binary_if_not_already(x) if x.isdigit() else x for x in rule]
        start = time.time()
        # logging.debug("store prevrule tuple Start!! ")
        # for perms in self.store_prev_rules:
        #     logging.debug(perms)
        logging.debug("NEWLY INSERTED RULE: " + str(rule))
        logging.debug("COUNT: " + str(rule.count('*')))
        if rule.count("*") == self.ruleLength - 1:
            logging.debug("rule count * == 3: " + str(rule))
            rule_codeword = self.insertRuleIntoTree(rule, self.treeList)
            self.previousRuleTuple.append((rule, rule_codeword))
            logging.debug("Returned cus default")
            return #

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

        rule = [str(int(element[:-1], 2)) if (len(element) == self.codewordLength + 1 and element[-1] == "*"and element[:-1].isdigit()) else element for element in rule]
        logging.debug("_______ New inserted rule ______:" + str(rule))

        # elif self.ruleIsSubset(rule):
        #     logging.debug("Inserted rule is subset.. Return" + str(rule))
        #     return

        self.store_inserted.append(rule)

        rule_codeword = self.insertRuleIntoTree(rule, self.treeList)

        if not self.previousRuleTuple:
            self.previousRuleTuple.append((rule, rule_codeword))
            self.store_prev_rules.add(tuple(rule[:-1]))
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


        logging.debug("store prevrule tuple!! ")
        for perms in self.store_prev_rules:
            logging.debug(perms)

        # logging.debug("Store inserted tuple!! ")
        # for ins in self.store_inserted:
        #     logging.debug(ins)
        end = time.time()
        self.insert_packet_time += end - start
        
        file_path = "len_previousRuleTuple.txt"
        file = open(file_path, "a")
        print(str(self.counter) + "," + str(len(self.previousRuleTuple)) + "," + str(self.counter) + "," + str(self.insert_packet_time), file=file)

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
