from app.tools.data_miner.data_miner import data_miner
from app.tools.kg_expansion.expansions.abstract_expansion import AbstractExpansion
        
class TruthTextExtraction(AbstractExpansion):
    def __init__(self, truth_graph, miner):
        super().__init__(truth_graph, miner)

    def expand(self):
        pes = self._tg.get_physicalentity()
        for entity in pes:
            descs = entity.description
            for der in data_miner.mine_derivatives(descs):
                if der in pes:
                    self._tg.derivatives.positive(entity,der)
            for inter,parts in data_miner.mine_interactions(descs):
                for part,p_type in parts:
                    if part in pes:
                        self._tg.interactions.positive(inter,entity,p_type)

            
