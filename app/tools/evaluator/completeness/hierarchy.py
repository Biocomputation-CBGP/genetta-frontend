import uuid
from neo4j.exceptions import ClientError
from app.tools.evaluator.abstract_evaluator import AbstractEvaluator


class HierarchyEvaluator(AbstractEvaluator):
    '''
    Evaluates how well the design is structurally encoded, 
    i.e. how much of a hierarchy of parts is described.
    '''
    def __init__(self, world_graph, miner):
        super().__init__(world_graph, miner)
        
    def evaluate(self,graph):
        score = self._initial_score
        comments = {}
        proj_name = str(uuid.uuid4())

        try:
            res = graph.project.hierarchy(proj_name)
        except ClientError:
            comments['Design'] = ("No Hierarchy encoded.")
            return {"score": 0,"comments": comments}
        
        roots = graph.get_root_entities()
        if len(roots) == 0:
            comments['Design'] = ("Circular Hierarchy")
            return {"score": 0,"comments": comments}
        hierarchies = []
        if not graph.procedure.is_connected(proj_name):
            comments["Design"] = "DNA Hierarchy graph disconnected. (Not error if multi-cellular)"
        r_level = []
        def _walk(element,level,seens):
            nonlocal r_level
            nonlocal score
            children = [c.v for c in graph.get_children(element)]
            if len(children) == 0:
                return
            if len(r_level) <= level:
                r_level.append([])
            r_level[level] = list(set(r_level[level] + children))
            for child in children:  
                if child in seens:
                    comments[element] = f'{element} and {child} makes the hierarchy circular.'
                    return -1
                rv = self._child_previous_check(child,r_level)
                if rv is not None:
                    comments[child] = f'{child} is in hierarchy levels {level} and {rv} consider adding intermediate.'
            # Makes its BFS as all children are considered before moving on.
            for child in children:
                if _walk(child,level+1,seens+[child]) == -1:
                    return -1

        increment = self._get_increment(len(graph.get_dna())) # ?? How do we score this ??
        for root in roots:
            r_level = [[root]]
            _walk(root,1,roots)
            hierarchies.append(r_level.copy())
            r_level.clear() 
        return {"score": int(score),
                "comments": comments}

    def _child_previous_check(self,child,levels):
        for index,level in enumerate(levels[:-1]):
            if child in level:
                return index
        return None