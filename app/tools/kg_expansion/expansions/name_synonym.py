from app.tools.kg_expansion.expansions.abstract_expansion import AbstractExpansion
from app.graph.utility.model.model import model

nv_dna = str(model.identifiers.objects.dna)
nv_dna_cc = model.get_class_code(nv_dna)


class TruthNameSynonym(AbstractExpansion):
    def __init__(self, truth_graph, miner):
        super().__init__(truth_graph, miner)

    def expand(self):
        '''
        For each physcial entity, set a synonym node 
        with the name of the entity as value.
        If multiple nodes have the same name, 
        share the confidence.
        '''
        name_map = {}
        s_graph = self._tg.synonyms.get()
        for entity in self._tg.get_physicalentity():
            e_name = self._get_name(entity.get_key())
            e_synonyms = [s.v.get_key() for s in s_graph.synonyms(entity)]
            if e_name in e_synonyms:
                continue
            if e_name in name_map:
                name_map[e_name].append(entity)
            else:
                name_map[e_name] = [entity]
        for name,entities in name_map.items():
            conf = int(100/len(entities))
            for entity in entities:
                self._tg.synonyms.positive(entity,name,score=conf)
