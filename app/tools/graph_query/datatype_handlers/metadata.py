from app.graph.utility.model.model import model
from app.tools.graph_query.datatype_handlers.abstract_handler import AbstractHandler

p_description = model.identifiers.external.description
class MetadataHandler(AbstractHandler):
    def __init__(self,graph):
        super().__init__(graph)

    def get_name(self):
        return "Metadata"
    
    def get_description(self):
        return "Returns entities based on matches within metadata."
    
    def get_example(self):
        return "Repression"
    
    def handle(self,query):
        '''
        Questions posed with metadata searches.
        1. Do we take into account individual words or partial or full queries.
            1.1. For example, [Laci,Repression,plac] OR ["Laci represses pLac"]
            1.2. I think with a metadata search, a match must be within all words with removed stopwords.
        2. Do synonyms ever carry there own metadata or is the canonical entity the holder?
        3. Descriptions are captured in lists. I think there is an issue where the indexing isn't working properly.
           Try figure out if there is a special case for lists.
        4. How would the feedback even work for metadata? Perhaps it just doesnt.
         '''
        results = {}
        qry_eles = self._miner.get_entities(query)
        results[None] = self._identify_entities(qry_eles,index=p_description,
                                                       predicate="AND")
        return results


    def feedback(self, source, result, positive=True):
        pass