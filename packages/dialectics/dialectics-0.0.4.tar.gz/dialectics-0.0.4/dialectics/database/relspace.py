from lib2to3.pytree import Base
from dialectics.imports import *
from .docspace import DocspaceModel
log=Log()
from arango import DocumentInsertError


class RelspaceModel(DocspaceModel):
    def __init__(self,
            name=RELSPACE_DEFAULT,
            from_collections=FROM_DEFAULT,
            to_collections=TO_DEFAULT,
            dbname=DATABASE+'_'+VNUM,
            _client=None,
            _db=None,
            _coll=None,
            ):
        self.name=name
        self.name_v=from_collections[0]
        self.dbname=dbname
        self._client=None
        self._db=None
        self._coll=None
        self._from=from_collections
        self._to=to_collections
        self._graph=None
        self._edgedf=None


        self.init_database()
        self.init_graph()
        self.init_collection()

    @property
    def graph(self):
        if self._graph is None: self.init_graph()
        return self._graph

    def __repr__(self):
        return f"Relspace('{self.name}')"
    
    @property
    def coll_v(self): 
        if log>1: log(self)
        if self._coll_v is None: self.init_collection()
        return self._coll_v


    def init_graph(self):
        if self.db.has_graph(GRAPHNAME):
             self._graph = self.db.graph(GRAPHNAME)
        else:
            self._graph = self.db.create_graph(GRAPHNAME)


    def init_collection(self, drop=False):

        # vertex collection
        if not self.graph.has_vertex_collection(self.name_v):
            self._coll_v=self.graph.create_vertex_collection(self.name_v)
        
        self._coll_v = self.graph.vertex_collection(self.name_v)
        
        # edge collection
        if not self.graph.has_edge_definition(self.name):
            self._coll = self.graph.create_edge_definition(
                edge_collection=self.name,
                from_vertex_collections=[self.name_v],
                to_vertex_collections=[self.name_v],
            )
        else:
            self._coll = self.graph.edge_collection(self.name)


    def link(self,id1,id2,d1={},**d2):
        from dialectics.texts import Text
        log('linking texts')
        t1,t2=Text(id1),Text(id2)


        ## add vertices
        for t in [t1,t2]:
            td=t.ensure_id()
            del td['_id']
            try:
                self.coll_v.insert(td)
            except DocumentInsertError:
                self.coll_v.update(td)
                
            
        ## add edge
        key=f'{t1._key}__{t2._key}'
        _id=f'{self.name}/{key}'
        obj={
            '_id':_id,
            '_key':key,
            '_from':t1._id,
            '_to':t2._id,
            **safebool(safejson(merge_dict(d1,d2)))
        }

        del obj['_id']
        try:
            self.coll.insert(obj)
        except DocumentInsertError as e:
            self.coll.update(obj)






from .docspace import Docspace
def Relspace(force=False, **kwargs):
    return Docspace(RELSPACE_DEFAULT, _class=RelspaceModel, **kwargs)    
