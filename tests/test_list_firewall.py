import random
import unittest
import Parallel_tree_algorithm.python.listFirewall.listFirewall as listFirewall
import logging


class TestListFirewall(unittest.TestCase):
    def setUp(self):
        self.listFirewall = listFirewall.ListFirewall()
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt')
        
    def test_insert(self):
        rule0 = ["*","1","1","alpha"]
        rule1 = ["1","1","*","beta"]
        self.listFirewall.insert(rule0)
        self.listFirewall.insert(rule1)
        logging.debug("firewall list" + str(self.listFirewall.rules))
        self.assertEqual(self.listFirewall.lookup(["1","1","1"]), "alpha")
        self.assertNotEqual(self.listFirewall.lookup(["1","1","1"]), "beta")
        
    def test_insert_ranges(self):
        rule0 = ["1","1-2","*","alpha"]
        rule1 = ["1","2-4","*","beta"]
        rule2 = ["*","*","*","gamma"]
        self.listFirewall.insertRange(rule0)
        self.listFirewall.insertRange(rule1)
        self.listFirewall.insertRange(rule2)
        logging.debug("firewall list" + str(self.listFirewall.rules))
        self.assertEqual(self.listFirewall.lookup(["1","1","1"]), "alpha")
        self.assertEqual(self.listFirewall.lookup(["1","2","2"]), "alpha")

        self.assertEqual(self.listFirewall.lookup(["1","3","3"]), "beta")
        self.assertEqual(self.listFirewall.lookup(["1","4","4"]), "beta")
        self.assertEqual(self.listFirewall.lookup(["2","34","56"]), "gamma")
    