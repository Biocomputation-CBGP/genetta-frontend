import sys
import os
import unittest
from rdflib import URIRef
sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..","..","..",".."))
from app.graph.world_graph import WorldGraph
from app.graph.utility.model.model import model
from app.tools.kg_expansion.expansions.text_extraction import TruthTextExtraction
from app.tools.data_miner.data_miner import data_miner
curr_dir = os.path.dirname(os.path.realpath(__file__))


class TestEnhancements(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.wg = WorldGraph()
        self.tg = self.wg.truth


    @classmethod
    def tearDownClass(self):
        pass
    
    def test_text_extraction_expansion(self):
        ppe = TruthTextExtraction(self.wg,data_miner)
        pre_e = self.tg.edges()
        ppe.enhance()
        post_e = self.tg.edges()
