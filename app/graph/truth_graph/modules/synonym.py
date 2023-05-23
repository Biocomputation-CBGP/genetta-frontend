from app.graph.utility.graph_objects.reserved_edge import ReservedEdge
from app.graph.utility.graph_objects.reserved_node import ReservedNode
from app.graph.utility.model.model import model
from app.graph.truth_graph.modules.abstract_module import AbstractModule

confidence = str(model.identifiers.external.confidence)
p_synonym = str(model.identifiers.external.synonym)
o_synonym = str(model.identifiers.objects.synonym)
class SynonymModule(AbstractModule):
    def __init__(self,truth_graph):
        super().__init__(truth_graph)
    
    def get(self,subject=None,synonym=None,threshold=90):
        e = ReservedEdge(n=subject,v=synonym,type=p_synonym,
                         graph_name=self._tg.name)
        res = self._tg.edge_query(e=e)
        if len(res) != 0:
            return self._to_graph(res)
        if synonym is not None:
            edges = []
            for r in self._tg.node_query(name=synonym):
                edges += self._tg.edge_query(v=r,e=p_synonym,
                                             threshold=threshold)
            return self._to_graph(edges)
        return self._to_graph([])


    def positive(self,subject,synonym,score=None):
        if score is None:
            score = self._standard_modifier
        subject = self._cast_node(subject)
        if not isinstance(synonym,ReservedNode):
            synonym = self._cast_node(synonym,o_synonym)
        synonym = self._cast_node(synonym)
        # Check if the subject is in the graph.
        res = self._tg.edge_query(subject,e=p_synonym)
        if len(res) != 0:
            for edge in res:
                # Full edge exists.
                if synonym.get_key() == edge.v.get_key():
                    return self._update_confidence(res[0],score)
            else:
                # New synonym to existing subject
                edge = self._cast_edge(subject,synonym,p_synonym,name="Synonym")
                return self._add_new_edge(edge,confidence=score)
        # Add new edge
        # Even where the synonym node may exist 
        # already we still add the node.
        edge = self._cast_edge(subject,synonym,p_synonym,name="Synonym")
        return self._add_new_edge(edge)


    def negative(self,subject,synonym):
        # Same as positive but without adding any new edges.
        subject = self._cast_node(subject)
        synonym = self._cast_node(synonym)
        res = self._tg.edge_query(subject,e=p_synonym)
        if len(res) != 0:
            for edge in res:
                if synonym.get_key() == edge.v.get_key():
                    return self._update_confidence(
                        res[0],-self._standard_modifier)

