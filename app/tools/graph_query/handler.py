from app.tools.graph_query.datatype_handlers.canonical import CanonicalHandler
from app.tools.graph_query.datatype_handlers.derivative import DerivativeHandler
from app.tools.graph_query.datatype_handlers.interaction import InteractionHandler
from app.tools.graph_query.datatype_handlers.metadata import MetadataHandler
class GraphQueryHandler:
    def __init__(self,graph):
        self._graph = graph
        self._handlers = [CanonicalHandler(graph),
                        DerivativeHandler(graph),
                        InteractionHandler(graph),
                        MetadataHandler(graph)]

    def get_handlers(self):
        return self._handlers

    def query(self,datatype,query):
        for handler in self._handlers:
            if handler.get_name() == datatype:
                return handler.handle(query)
        raise ValueError(f'{datatype} is not a valid datatype.')
    
    def feedback(self,datatype,source,result,positive=True):
        for handler in self._handlers:
            if handler.get_name() == datatype:
                return handler.feedback(source,result,positive=positive)
        raise ValueError(f'{datatype} is not a valid datatype.')