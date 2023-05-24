from app.tools.graph_query.datatype_handlers.abstract_handler import AbstractHandler
from app.graph.utility.model.model import model

class SequenceHandler(AbstractHandler):
    def __init__(self,graph):
        super().__init__(graph)

    def get_name(self):
        return "Sequence"
    
    def get_description(self):
        return "Returns genetic parts based on sequence matching."
    
    def get_example(self):
        return "tttaattatatatatatatatatataatggaagcgtttt"
    
    def handle(self,query):
        query = query.replace(" ","")
        for entity in self._graph.sequence_query(query):
            pass
        
        return results
    
    def feedback(self, source, result, positive=True):
        pass