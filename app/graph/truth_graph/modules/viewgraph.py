import networkx as nx
from app.graph.utility.graph_objects.reserved_node import ReservedNode
from app.graph.utility.graph_objects.reserved_edge import ReservedEdge
from app.graph.utility.model.model import model

all_i_types = [str(i[1]["key"]) for i in model.get_derived(model.identifiers.objects.interaction)]
nv_derivative = str(model.identifiers.external.derivative)
nv_synonym = str(model.identifiers.external.synonym)
class ViewGraph:
    def __init__(self, graph=None): 
        self._graph = graph if graph is not None else nx.MultiDiGraph()

    def resolve_node(func):
        def inner(self,n=None):
            if isinstance(n,ReservedNode):
                n = n.id
            elif n in self.nodes():
                n = n
            else:
                for node in self.nodes():
                    if node.get_key() == n:
                        n = node.id
            return func(self,n)
        return inner
        
    def __len__(self):
        return len(self._graph)

    def __eq__(self, obj):
        if isinstance(obj, self.__class__):
            return nx.is_isomorphic(self._graph, obj._graph)
        if isinstance(obj, nx.MultiDiGraph):
            return nx.is_isomorphic(self._graph, obj)
        return False

    def __iter__(self):
        for n in self._graph.nodes:
            yield n

    def __add__(self,viewgraph):
        return self.__class__(nx.compose(self._graph,viewgraph._graph))
    
    def __iadd__(self,viewgraph):
        return self.__class__(nx.compose(self._graph,viewgraph._graph))
        
    def _node(self,labels,id=None,properties=None):
        if properties is None:
            props = {}
        else:
            props = properties
        return ReservedNode(labels,id=id,**props)
    
    def _edge(self,n,v,e,properties=None):
        if properties is None:
            props = {}
        else:
            props = properties
        return ReservedEdge(n,v,e,**props)

    def derivatives(self,node=None):
        o_edges = list(self.out_edges(node))
        for edge in o_edges:
            if edge.get_type() == nv_derivative:
                yield edge
        for edge in self.in_edges(node):
            if edge in o_edges:
                continue
            if edge.get_type() == nv_derivative:
                e = ReservedEdge(edge.v,edge.n,edge.get_type(),
                                   **edge.get_properties())
                if e in o_edges:
                    continue
                yield e
    
    def synonyms(self,canonical=None,synonym=None):
        if isinstance(canonical,ReservedNode):
            canonical = canonical.get_key()
        if isinstance(synonym,ReservedNode):
            synonym = synonym.get_key()
        if canonical is not None:
            for edge in self.out_edges(canonical):
                if edge.get_type() != nv_synonym:
                    continue
                if synonym is None:
                    yield edge
                elif edge.v.get_key() == synonym:
                    yield edge
        elif synonym is not None:
            for edge in self.in_edges():
                if edge.get_type() != nv_synonym:
                    continue
                if edge.v.get_key() == synonym:
                    yield edge
                if edge.v.name == synonym:
                    yield edge
                
        else:
            for edge in self.edges():
                if edge.get_type() != nv_synonym:
                    continue
                yield edge


    def interactions(self,interaction=None,participant=None,i_type=None):
        if i_type is None:
            i_type = all_i_types
        if not isinstance(i_type,list):
            i_type = [i_type]

        if participant is not None:
            for edge in self.in_edges(participant):
                if interaction is not None and edge.n.get_key() == interaction:
                    return edge.n
                if interaction is None and edge.n.get_type() in i_type:
                    yield edge.n
        elif interaction is not None:
            for edge in self.out_edges(interaction):
                yield edge


    def interaction_elements(self,interaction):
        return self.out_edges(interaction)
    
    def nodes(self):
        for n,data in self._graph.nodes(data=True):
            props = data.copy()
            labels = props["key"]
            del props["key"]
            yield self._node(labels,id=n,properties=props)

    @resolve_node
    def edges(self,n=None):
        for n,v,e,d in self._graph.edges(n,keys=True,data=True):
            props = self._graph.nodes[n].copy()
            labels = props["key"]
            del props["key"]
            n = self._node(labels,id=n,properties=props)

            props = self._graph.nodes[v].copy()
            labels = props["key"]
            del props["key"]
            v = self._node(labels,id=v,properties=props)
            yield self._edge(n,v,e,properties=d)

    def get_node(self,n=None):
        if n is None:
            return list(self.nodes())
        try:
            data = self._graph.nodes[n]
            props = data.copy()
            labels = props["key"]
            del props["key"]
            return self._node(labels,id=n,properties=props)
        except KeyError:
            for node in self.nodes():
                if node.get_key() == n:
                    return node
            return None
        

    @resolve_node
    def in_edges(self, node=None):
        for n,v,e,d in self._graph.in_edges(node,keys=True,data=True):
            props = self._graph.nodes[n].copy()
            labels = props["key"]
            del props["key"]
            n = self._node(labels,id=n,properties=props)

            props = self._graph.nodes[v].copy()
            labels = props["key"]
            del props["key"]
            v = self._node(labels,id=v,properties=props)
            yield self._edge(n,v,e,properties=d)

    @resolve_node
    def out_edges(self, node=None):
        for n,v,e,d in self._graph.out_edges(node,keys=True,data=True):
            props = self._graph.nodes[n].copy()
            labels = props["key"]
            del props["key"]
            n = self._node(labels,id=n,properties=props)

            props = self._graph.nodes[v].copy()
            labels = props["key"]
            del props["key"]
            v = self._node(labels,id=v,properties=props)
            yield self._edge(n,v,e,properties=d)



    def has_edge(self,edge):
        return self._graph.has_edge(edge.n.id,edge.v.id,key=edge.get_type())
    
    def add_edge(self, edge):
        self._graph.add_edge(edge.n.id,edge.v.id,key=edge.get_type(),**edge.get_properties())

    def add_node(self, node):
        self._graph.add_node(node.id,key=node.get_key(),type=node.get_type(),**node.get_properties())

    def remove_edge(self, edge):
        self._graph.remove_edge(edge.n.id, edge.v.id, edge.get_type())

    def remove_node(self, node):
        self._graph.remove_node(node)
        
