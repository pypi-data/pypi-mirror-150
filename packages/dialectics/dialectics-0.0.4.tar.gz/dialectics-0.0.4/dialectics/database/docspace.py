#print(__file__,'imported')
from dialectics.imports import *
from .baseobj import BaseObject
log = Log()


class DocspaceModel(BaseObject):
    def __init__(self,
            name=TEXT_COLLECTION_NAME,
            dbname=DATABASE+'_'+VNUM,
            _client=None,
            _db=None,
            _coll=None,
            ):
        self.name=name
        self.dbname=dbname
        self._client=None
        self._db=None
        self._coll=None
    
    @property
    def client(self):
        if log>1: log(self)
        if self._client is None: self.init_database()
        return self._client
    @property
    def db(self):
        if log>1: log(self)
        if self._db is None: self.init_database()
        if log>1: log(self._db)
        return self._db
    @property
    def coll(self): 
        if log>1: log(self)
        if self._coll is None: self.init_collection()
        return self._coll
    
    def __str__(self):
        return f"Dospace('{self.name}','{self.dbname}')"

    def init_database(self,force=False):
        if log>1: log(self)
        if force or self._db is None:
            from arango import ArangoClient
            self._client = ArangoClient(hosts=','.join(SERVERS))
            self._sysdb  = self._client.db('_system', username='root', password='passwd')
            if not self._sysdb.has_database(self.dbname): self._sysdb.create_database(self.dbname)
            self._db = self._client.db(self.dbname, username='root', password='passwd')
        return self.db

    def init_collection(self,drop=False):
        if log>1: log(self)
        if self.db.has_collection(self.name) and drop: self.db.delete_collection(self.name)
        if not self.db.has_collection(self.name):
            self.db.create_collection(self.name)
            coll = self._coll=self.db.collection(self.name)
            coll.add_persistent_index(fields=['_addr'],unique=True)
            coll.add_persistent_index(fields=['_corpus'])
            coll.add_persistent_index(fields=['id'])
            coll.add_persistent_index(fields=['au'])
            coll.add_persistent_index(fields=['ti'])
            coll.add_persistent_index(fields=['yr'])
            coll.add_fulltext_index(fields=['author'])
            coll.add_fulltext_index(fields=['title'])
        else: 
            self._coll=self.db.collection(self.name)
        return self._coll
        

            
    ### TREATS FULL TEXT OPERATOR FOR MULTIPLE ARGUMENTS AS 'OR' so far
    def find(self,*args,**kwargs):
        if log>1: log(self)
        from dialectics.texts.textlist import TextList
        return TextList(self.look(*args,**kwargs))


    def get(self,id,default=None):
        from dialectics.texts import Text
        from .relspace import Relspace

        if id in TEXT_CACHE: return TEXT_CACHE[id]
        if id in CORPUS_CACHE: return CORPUS_CACHE[id]
        if self.coll.has(id): return Text(**self.coll.get(id))
        
        if Relspace().coll.has(id): return Text(**Relspace().coll.get(id))

        return default

        
    def look(self, id_key=COL_ADDR, **query_meta):
        if log>1: log(self)
        from dialectics import Text,Log
            
        # prime
        if not self.coll: return

        fulltextmeta={k:v for k,v in query_meta.items() if k in FULL_TEXT_KEYS}
        exactmeta={k:v for k,v in query_meta.items() if k not in FULL_TEXT_KEYS}
        if log>1: log(fulltextmeta)
        if log>1: log(exactmeta)
        ids_given=set()

        if exactmeta:
            with Log(f'Querying exact metadata: {exactmeta}'):
                res_exact = self.coll.find(exactmeta)
                for d in res_exact:
                    id=d.get(id_key)
                    if id not in ids_given:
                        yield Text(**d)
                        ids_given|={id}
        
        if fulltextmeta:
            with Log(f'Querying full text metadata: {fulltextmeta}'):
                for qk,qv in fulltextmeta.items():
                    res = self.coll.find_by_text(qk,qv)
                    for d in res:
                        id=d.get(id_key)
                        if id not in ids_given:
                            yield Text(**d)
                            ids_given|={id}



class TextspaceModel(DocspaceModel): pass


DOCSPACES={}
def Docspace(name, dbname=f"{DATABASE}_{VNUM}", force=False, _class=DocspaceModel,**kwargs):
    key=(name,dbname,_class.__name__)
    if not force and key in DOCSPACES: return DOCSPACES[key]
    obj = _class(name=name,dbname=dbname)
    DOCSPACES[key] = obj
    return obj

def Textspace(force=False, **kwargs):
    return Docspace(TEXT_COLLECTION_NAME, **kwargs)

