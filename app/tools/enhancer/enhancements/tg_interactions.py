from app.tools.enhancer.enhancements.abstract_enhancements import AbstractEnhancement
from app.graph.utility.model.model import model

class TruthInteractions(AbstractEnhancement):
    '''
    Extracts all entities from the truth graph 
    into the design graph (assumes canonical)
    '''
    def __init__(self, world_graph, miner):
        super().__init__(world_graph, miner)

    def enhance(self,graph_name,automated=False):
        '''
        Considerations:
            1. When only one participant of an interaction is in the TG.
            2. When both are in the TG & DG, dont duplicate interactions.
            3. When the interaction of TG is already in DG.

        For each pe: 
            If pe not in tg: Continue
            For each interaction (I) of pe in tg:
                If seen: Continue
                If interaction in DG: Continue
                Get other participants of I
                For each other part (P):
                    If p not in TG:
                        ??
                Add new interaction.
                
        '''
        graph = self._wg.get_design(graph_name)
        changes = {}
        return changes
    
    def apply(self,replacements,graph_name):
        graph = self._wg.get_design(graph_name)



