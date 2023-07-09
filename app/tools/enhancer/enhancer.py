import os
from app.tools.data_miner.data_miner import data_miner
from app.tools.enhancer.enhancements.canonicaliser import Canonicaliser
from app.tools.enhancer.enhancements.tg_interactions import TruthInteractions
from app.tools.enhancer.enhancements.text_extraction import TextExtraction
tg_initial_fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),"seeder","tg_initial.json")

class Enhancer:
    def __init__(self,graph):
        self._graph = graph
        self._miner = data_miner
        self._canonicaliser = Canonicaliser(graph,self._miner)
        self._enhancers = [TruthInteractions(graph,self._miner),
                           TextExtraction(graph,self._miner)]
    
    def get_canonical_entity(self,entity,gn):
        print("get_canonical_entity not implemented.")
        return {}

    # --- Design ---
    def canonicalise(self,graph_name,automated=True):
        return self._canonicaliser.enhance(graph_name,automated=automated)
    
    def apply_canonicalise(self,replacements,graph_name):
        return self._canonicaliser.apply(replacements,graph_name)
    
    def enhance(self,graph_name,automated=True):
        res = {}
        if len(self._enhancers) == 0:
            return res
        for e in self._enhancers:
            res[e.name] = e.enhance(graph_name,automated=automated)
        return res
    
    def apply_enhance(self,replacements,graph_name):
        for evaluator in self._enhancers:
            evaluator.apply(graph_name,replacements)

