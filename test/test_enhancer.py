import sys
import os
import unittest

sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..","..","..",".."))
from app.graph.world_graph import WorldGraph
from app.tools.enhancer.enhancer import Enhancer
from app.tools.enhancer.enhancements.tg_interactions import TruthInteractions
from app.tools.enhancer.enhancements.protein_production import ProteinProduction
from app.tools.enhancer.enhancements.protein_production import defered_int_types
from app.tools.enhancer.enhancements.text_extraction import TextExtraction
from app.converter.sbol_convert import convert
from app.converter.sbol_convert import export
from app.graph.utility.graph_objects.node import Node
from app.graph.utility.model.model import model

curr_dir = os.path.dirname(os.path.realpath(__file__))
fn = os.path.join("test","files","canonical_AND.xml")

db_host = os.environ.get('NEO4J_HOST', 'localhost')
db_port = os.environ.get('NEO4J_PORT', '7687')
db_auth = os.environ.get('NEO4J_AUTH', "neo4j/Radeon12300")
db_auth = tuple(db_auth.split("/"))
uri = f'neo4j://{db_host}:{db_port}'
login_graph_name = "login_manager"

nv_pp = str(model.identifiers.objects.genetic_production)
class TestEnhancer(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.gn = "test_enhancer"
        self.wg = WorldGraph(uri,db_auth,reserved_names=[login_graph_name])
        self.enhancer = Enhancer(self.wg)
        self.miner = self.enhancer._miner
        self.wg.remove_design(self.gn)
        convert(fn,self.wg.driver,self.gn)
        

    def tearDown(self):
        self.wg.remove_design(self.gn)


    def test_enhance_protein_production_manual_AND(self):
        enhancer = ProteinProduction(self.wg,self.miner)
        changes = enhancer.enhance(self.gn,automated=False)
        graph = self.wg.get_design(self.gn)
        cds = [k.get_key() for k in graph.get_cds()]
        replacements = {}
        for k,v in changes.items():
            self.assertIn(k,cds)
            replacements[k] = list(v.keys())[0]
        enhancer.apply(replacements,self.gn)
        for cd in cds:
            cd_ints = graph.get_interactions(cd)
            for cdi in cd_ints:
                if cdi.n.get_type() == nv_pp:
                    break
            else:
                self.fail()

    def test_enhance_protein_production_automated_AND(self):
        enhancer = ProteinProduction(self.wg,self.miner)
        enhancer.enhance(self.gn,automated=True)
        graph = self.wg.get_design(self.gn)
        cds = graph.get_cds()
        for cd in cds:
            cd_ints = graph.get_interactions(cd)
            for cdi in cd_ints:
                if cdi.n.get_type() == nv_pp:
                    break
            else:
                self.fail()

    def test_enhance_protein_production_manual_existing_interactions(self):
        t_fn = os.path.join("test","files","protein_production_existing_interactions.xml")
        gn = "test_enhance_protein_production_existing_interactions"
        self.wg.remove_design(gn)
        convert(t_fn,self.wg.driver,gn)
        enhancer = ProteinProduction(self.wg,self.miner)
        changes = enhancer.enhance(gn,automated=False)
        graph = self.wg.get_design(gn)
        cds = [k.get_key() for k in graph.get_cds()]
        replacements = {}
        for k,v in changes.items():
            val = list(v.keys())[0]
            replacements[k] = val
        enhancer.apply(replacements,gn)
        for cd in cds:
            cd_ints = [i.n.get_type() for i in graph.get_interactions(cd)]
            self.assertIn(nv_pp,cd_ints)
            for def_int in defered_int_types:
                self.assertNotIn(def_int,cd_ints)
        self.wg.remove_design(gn)

    def test_enhance_protein_production_automated_existing_interactions(self):
        t_fn = os.path.join("test","files","protein_production_existing_interactions.xml")
        gn = "test_enhance_protein_production_existing_interactions"
        self.wg.remove_design(gn)
        convert(t_fn,self.wg.driver,gn)
        enhancer = ProteinProduction(self.wg,self.miner)
        changes = enhancer.enhance(gn,automated=True)
        graph = self.wg.get_design(gn)
        cds = graph.get_cds()
        for cd in cds:
            cd_ints = graph.get_interactions(cd)
            for cdi in cd_ints:
                if cdi.n.get_type() == nv_pp:
                    break
            else:
                self.fail()
        self.wg.remove_design(gn)


    def test_enhance_interactions_manual_AND(self):
        enhancer = TruthInteractions(self.wg,self.miner)
        enhancer.enhance(self.gn,automated=False)

    def test_enhance_interactions_automated_AND(self):
        enhancer = TruthInteractions(self.wg,self.miner)
        enhancer.enhance(self.gn,automated=False)



    def test_enhance_text_extraction_manual_AND(self):
        enhancer = TextExtraction(self.wg,self.miner)
        enhancer.enhance(self.gn,automated=False)

    def test_enhance_text_extraction_automated_AND(self):
        enhancer = TextExtraction(self.wg,self.miner)
        enhancer.enhance(self.gn,automated=False)



    def test_enhance_automated(self):
        self.enhancer.enhance(self.gn,automated=False)

    def test_enhance_manual(self):
        self.enhancer.enhance(self.gn,automated=False)
        





