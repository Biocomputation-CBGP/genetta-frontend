from app.tools.graph_query.datatype_handlers.abstract_handler import AbstractHandler
class InteractionHandler(AbstractHandler):
    def __init__(self,graph):
        super().__init__(graph)

    def get_name(self):
        return "Interaction"
    
    def get_description(self):
        '''
        Consider if also, this could be expanded.
        Some ideas follow (Increasing complexity):
            1. Given an interaction type, each record returned 
                is the systems which implement this regulation.
            2. Returns interactions between provided entities (Multiple Inputs).
            3. Given an abstract function for example NOR, returns implementations. (This might be better on its own Handler.)
        '''
        return "Returns interactions of a provided entity."
    
    def get_example(self):
        return "pAmtR"
    
    def handle(self,query):
        results = {}
        graph = self._graph.interactions.get(threshold=0)
        graph += self._graph.synonyms.get(threshold=0)
        for qry_ele in self._miner.get_entities(query):
            entities = self._identify_entities(qry_ele,graph)
            entities = self._cast_synonyms(entities,graph)
            for entity in entities:
                e_res = []
                for inter in graph.interactions(participant=entity):
                    conf = 0
                    description = f'{self._get_name(inter.get_type())}:\n'
                    i_eles = list(graph.interactions(interaction=inter))
                    for i in i_eles:
                        description += f'''{self._get_name(i.v.get_key())} 
                                          ({self._get_name(i.get_type())})\n'''
                        conf += i.confidence
                    conf = int(conf / len(i_eles))
                    e_res.append((conf,{"description" : description, 
                                        "entity" : inter.get_key()}))
                if len(e_res) > 0:
                    entity = entity.get_key()
                    if entity in results:
                        e_res = self._merge_duplicates(results[entity],e_res)
                    e_res = self._rank_result(e_res)
                    results[entity] = e_res
        return results

    def feedback(self, source, result, positive=True):
        print(source,result)
        