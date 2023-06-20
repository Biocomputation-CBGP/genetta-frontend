from app.graph.utility.graph_objects.reserved_edge import ReservedEdge
from app.graph.utility.model.model import model
from app.graph.truth_graph.modules.abstract_module import AbstractModule

confidence = str(model.identifiers.external.confidence)
p_derivative = str(model.identifiers.external.derivative)

class DerivativeModule(AbstractModule):
    def __init__(self,truth_graph):
        super().__init__(truth_graph)
    
    def get(self,subject=None,derivative=None,threshold=None,directed=False):
        if threshold is None:
            threshold = self._default_threshold
        e = ReservedEdge(n=subject,v=derivative,type=p_derivative,
                         graph_name=self._tg.name)
        res = self._tg.edge_query(e=e,directed=directed,
                                  threshold=threshold)
        return self._to_graph(res)

    def positive(self,subject,derivative,score=None):
        subject = self._cast_node(subject)
        derivative = self._cast_node(derivative)
        # Check if the subject is in the graph.
        if score is None:
            score = self._standard_modifier
        if score < 1:
            score = int(score *100)
        res = self._tg.edge_query(n=subject,v=derivative,e=p_derivative)
        if len(res) != 0:
            assert(len(res) == 1)
            return self._update_confidence(res[0],score)
        res = self._tg.edge_query(n=derivative,v=subject,e=p_derivative)
        if len(res) != 0:
            assert(len(res) == 1)
            return self._update_confidence(res[0],score)
        edge = self._cast_edge(subject,derivative,p_derivative,name="Derivative")
        return self._add_new_edge(edge,score)



    def negative(self,subject,derivative,score=None):
        subject = self._cast_node(subject)
        derivative = self._cast_node(derivative)
        # Check if the subject is in the graph.
        if score is None:
            score = self._standard_modifier
        if score < 1:
            score = int(score *100)
        res = self._tg.edge_query(n=subject,v=derivative,e=p_derivative)
        if len(res) != 0:
            assert(len(res) == 1)
            return self._update_confidence(res[0],-score)
        res = self._tg.edge_query(n=derivative,v=subject,e=p_derivative)
        if len(res) != 0:
            assert(len(res) == 1)
            return self._update_confidence(res[0],-score)

