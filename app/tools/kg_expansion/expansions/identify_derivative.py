from app.tools.kg_expansion.expansions.abstract_expansion import AbstractExpansion
from app.graph.utility.model.model import model

nv_dna = str(model.identifiers.objects.dna)
nv_dna_cc = model.get_class_code(nv_dna)


class TruthDerivative(AbstractExpansion):
    def __init__(self, truth_graph, miner):
        super().__init__(truth_graph, miner)

    def expand(self):
        '''
        This is more of an open question. For derivatives and synonyms. When new entities are added after creation.
        During expansion runs, do we try to identify if they are synonyms or derivative of other entities.
        I.e. the stuff we did during build, do we do this during expansion?
        '''
