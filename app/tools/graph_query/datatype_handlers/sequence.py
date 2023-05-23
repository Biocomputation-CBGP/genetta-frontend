from app.tools.graph_query.datatype_handlers.abstract_handler import AbstractHandler
class SequenceHandler(AbstractHandler):
    def __init__(self,graph):
        super().__init__(graph)

    def get_name(self):
        return "Sequence"
    
    def get_description(self):
        return "Returns genetic parts based on sequence matching."
    
    def get_example(self):
        return ""
    
    def handle(self,query):
        '''
        The sequence data is stored as a URI. This introduces an issue at scale.
        I really can't think of a good way of doing this...
        You could try a custom sparql query to return the sequence only.
        However, even this is a limited solution.
        '''
        pass

    def feedback(self, source, result, positive=True):
        pass