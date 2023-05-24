from app.tools.kg_expansion.expansions.abstract_expansion import AbstractExpansion
from app.graph.utility.model.model import model
from app.tools.aligner import aligner
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
        existing_seqs = {}
        threshold = 80
        d_graph = self._tg.derivatives.get()
        for entity in self._tg.get_physicalentity():
            print(entity)
            e_dirs = [e.v for e in d_graph.derivatives(entity)]
            if model.is_derived(entity.get_type(),nv_dna_cc):
                seq = entity.hasSequence.lower()
                if seq in existing_seqs:
                    self._graph.merge_nodes(existing_seqs[seq],entity)
                    self._graph.synonyms.positive(existing_seqs[seq],
                                                  entity,score=100)
                    continue
                highest_score = [0,None]
                for k,v in existing_seqs.items():
                    if v in e_dirs:
                        continue
                    score = aligner.sequence_match(k,seq)
                    if score > highest_score[0]:
                        highest_score = [score,v]
                print(highest_score)
                if highest_score[0] > threshold:
                    self._graph.derivatives.positive(highest_score[1],
                                                     entity,
                                                     highest_score[0])
                existing_seqs[seq] = entity
