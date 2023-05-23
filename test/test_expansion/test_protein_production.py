import sys
import os
import unittest
sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
sys.path.insert(0, os.path.join("..","..",".."))
sys.path.insert(0, os.path.join("..","..","..",".."))
from app.graph.world_graph import WorldGraph
from app.graph.utility.model.model import model
from app.tools.kg_expansion.expansions.protein_production import TruthProteinProduction
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

class TestEnhancements(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.wg = WorldGraph(uri,db_auth,reserved_names=[login_graph_name])
        self.tg = self.wg.truth

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_protein_production_expansion(self):
        ppe = TruthProteinProduction(self.wg,data_miner)
        pre_e = self.tg.edges()
        ppe.enhance()
        post_e = self.tg.edges()
        diff = list(set(post_e) - set(pre_e))
        for d in diff:
            e_type = d.get_type()
            interaction = d.n.get_type()
            pe = d.v.get_type()

            self.assertEqual(interaction,nv_pp)
            if e_type == nv_template:
                self.assertEqual(pe,nv_cds)
            elif e_type == nv_product:
                self.assertEqual(pe,nv_p)
            else:
                self.fail()

