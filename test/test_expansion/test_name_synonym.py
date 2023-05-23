import sys
import os
import unittest
sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..","..","..",".."))
from app.graph.world_graph import WorldGraph
from app.graph.utility.model.model import model
from app.tools.kg_expansion.expansions.name_synonym import TruthNameSynonym
from app.tools.data_miner.data_miner import data_miner
curr_dir = os.path.dirname(os.path.realpath(__file__))

db_host = os.environ.get('NEO4J_HOST', 'localhost')
db_port = os.environ.get('NEO4J_PORT', '7687')
db_auth = os.environ.get('NEO4J_AUTH', "neo4j/Radeon12300")
db_auth = tuple(db_auth.split("/"))
uri = f'neo4j://{db_host}:{db_port}'
login_graph_name = "login_manager"


nv_p = str(model.identifiers.objects.protein)
nv_pp = str(model.identifiers.objects.genetic_production)
nv_cds = str(model.identifiers.objects.cds)
nv_template = str(model.identifiers.predicates.template)
nv_product = str(model.identifiers.predicates.product)

class TestDerivativeExpansion(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.wg = WorldGraph(uri,db_auth,reserved_names=[login_graph_name])
        self.tg = self.wg.truth

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_tg_derivative_enhancements(self):
        tns = TruthNameSynonym(self.tg,data_miner)
        pre_e = self.tg.edges()
        tns.expand()
        post_e = self.tg.edges()
        diff = list(set(post_e) - set(pre_e))
        s_graph = self.tg.synonyms.get()
        for entity in self.tg.get_physicalentity():
            e_name = tns._get_name(entity.get_key())
            e_s = [s for s in s_graph.synonyms(entity) 
                   if s.v.get_key() == e_name]
            self.assertEqual(len(e_s),1)

        s_g_edges = list(s_graph.synonyms())
        self.assertEqual(len(s_g_edges),len(list(set(s_g_edges))))

        tns.expand()
        post_post_e = list(self.tg.edges())
        diff2 = list(set(post_post_e) - set(post_e))
        self.assertEqual(len(diff2),0)

        self.tg.remove_edges(diff)
        final_e = list(self.tg.edges())
        self.assertCountEqual(final_e,pre_e)