from app.tools.enhancer.enhancements.abstract_enhancements import AbstractEnhancement
from app.graph.utility.model.model import model

nv_i = model.identifiers.objects.input
nv_o = model.identifiers.objects.output
nv_p = model.identifiers.objects.protein
nv_pp = model.identifiers.objects.genetic_production
nv_template = model.identifiers.predicates.template
nv_product = model.identifiers.predicates.product

class DesignProteinProduction(AbstractEnhancement):
    '''
    It is assumed that all CDS express proteins.
    '''
    def __init__(self, world_graph, miner):
        super().__init__(world_graph, miner)

    def enhance(self,graph_name,mode="automated"):
        graph = self._wg.get_design(graph_name)
        changes = {}
        for cds in graph.get_cds():
            for i in graph.get_interactions(cds):
                if i.n.get_type() == str(nv_pp):
                    break
            else:
                comment = f'{cds} Produces Protein.'
                if mode == "automated":
                    self.apply(self._potential_change({},cds,cds,100,
                                        comment,enabled=True),graph_name)
                else:
                    changes = self._potential_change(changes,cds,cds,100,comment)
        return changes
    
    def apply(self,replacements,graph_name):
        graph = self._wg.get_design(graph_name)
        for curr,options in replacements.items():
            for option,o_data in options.items():
                if o_data["apply"]:
                    n = self._add_related_node(graph,option,nv_p)
                    v = self._add_related_node(graph,option,nv_pp)
                    edges = [(option,nv_template),
                             (n,nv_product)]
                    self._add_interaction(graph,v,edges)

class TruthProteinProduction(AbstractEnhancement):
    '''
    It is assumed that all CDS express proteins.
    '''
    def __init__(self, world_graph, miner):
        super().__init__(world_graph, miner)
    
    def enhance(self):
        graph = self._wg.truth
        for cds in graph.get_cds():
            for i in graph.interactions.get(object=cds):
                if i.n.get_type() == str(nv_pp):
                    break
            else:
                n = self._add_related_node(graph,cds,nv_pp)
                v = self._add_related_node(graph,cds,nv_p)
                self._wg.truth.interactions.positive(n,cds,nv_template,100)
                self._wg.truth.interactions.positive(n,v,nv_product,100)



