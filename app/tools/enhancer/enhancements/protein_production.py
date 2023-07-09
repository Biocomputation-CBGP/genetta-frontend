from app.tools.enhancer.enhancements.abstract_enhancements import AbstractEnhancement
from app.graph.utility.model.model import model
from app.graph.utility.graph_objects.node import Node


nv_p = str(model.identifiers.objects.protein)
nv_cds = str(model.identifiers.objects.cds)
nv_pp = str(model.identifiers.objects.genetic_production)
nv_template = str(model.identifiers.predicates.template)
nv_product = str(model.identifiers.predicates.product)
nv_activation = str(model.identifiers.objects.activation)
nv_repression = str(model.identifiers.objects.repression)
defered_int_types = [nv_activation,nv_repression]

class ProteinProduction(AbstractEnhancement):
    '''
    Created protein production and proteins of CDS entities if required.
    Any Regulatory interactions on the CDS are swapped to the protein. 
    '''
    def __init__(self, world_graph, miner):
        super().__init__(world_graph, miner)


    def enhance(self,graph_name,automated=False):
        graph = self._wg.get_design(graph_name)
        changes = {}
        for cds in graph.get_cds():
            cds_ints = graph.get_interactions(cds)
            pp_int = []
            defered_ints = []
            for i in cds_ints:
                if i.n.get_type() == nv_pp:
                    pp_int.append(i)
                elif i.n.get_type() in defered_int_types:
                    defered_ints.append(i)
        
            if len(pp_int) == 0:
                prot = self._create_uri(cds.get_key(),nv_p)
                comment = f'{cds} Produces Protein.'
                if automated:
                    self.apply({cds:prot},graph_name)
                else:
                    changes= self._potential_change(changes,cds,prot,
                                                    100,comment)
            else:
                i_eles = graph.get_interaction_elements(pp_int[0].n)
                for ie in i_eles:
                    if ie.get_type() == nv_product:
                        protein = ie.v
                        break
                else:
                    raise ValueError(f'{ie} doesnt have a product.')
                if automated:
                    self.apply({protein:cds},graph_name)
                else:
                    comment = f'Swap interactions from {cds} to {protein}.'
                    changes= self._potential_change(changes,protein,cds,
                                                    100,comment)
        if automated:
            return self.apply(changes,graph_name)
        return changes
    
    def apply(self,replacements,graph_name):
        graph = self._wg.get_design(graph_name)
        for k,v in replacements.items():
            if not isinstance(k,Node):
                k = graph.nodes(k)
                assert(len(k) == 1)
                k = k[0]
            if k.get_type() == nv_cds:
                n = self._add_related_node(graph,k,nv_pp)
                protein = self._add_related_node(graph,k,nv_p)
                parts = [(protein,nv_product),
                        (k,nv_template)]
                self._add_interaction(graph,n,parts)
                self._replace_interactions(graph,k,protein)
            elif k.get_type() == nv_p:
                self._replace_interactions(graph,v,k)
            else:
                raise ValueError(f'{k} isnt Protein or CDS.')

    def _replace_interactions(self,graph,cds,protein):
        for i in graph.get_interactions(cds):
            if i.n.get_type() in defered_int_types:
                graph.remove_edges([i])
                i.v = protein
                graph.add_edges([i])