import os
from app.tools.data_miner.data_miner import data_miner
from app.tools.kg_expansion.expansions.derivative import TruthDerivative
from app.tools.kg_expansion.expansions.protein_production import TruthProteinProduction

tg_initial_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),"seeder","tg_initial.json")

class TruthGraphBuilder:
    def __init__(self,graph):
        self._graph = graph
        self._miner = data_miner
        self._modules = [TruthDerivative(self._graph,self._miner),
                         TruthProteinProduction(self._graph,self._miner)]
    
    def seed(self):
        '''
        Keep it seperate because it should only need to be loaded once ever.
        '''
        from app.tools.kg_expansion.seeder.seeder import Seeder
        if os.path.isfile(tg_initial_fn):
            print("Truth Graph present, building from file.")
            self._graph.drop()
            self._graph.load(tg_initial_fn)
        else:
            self._graph.drop()
            seeder = Seeder(self._graph,self._miner)
            seeder.enable_all()
            seeder.build()
            self._graph.truth.save(tg_initial_fn)
    
    def expand(self):
        for mod in self._modules:
            mod.expand()

