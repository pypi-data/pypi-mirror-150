#print(__file__,'imported')
from .utils import *


def gettimestamp():
    from datetime import datetime
    dt=datetime.now()
    return f'{dt.hour:02}:{dt.minute:02}:{dt.second:02}.{dt.microsecond//1000}'



def is_valid_text_obj(obj):
    return is_text_obj(obj) and obj.id_is_valid()

def is_text_obj(obj):
    from dialectics.texts import BaseText
    if issubclass(type(obj), BaseText): return True
    return False

def is_corpus_obj(obj): 
    from dialectics.corpora import BaseCorpus
    return issubclass(type(obj), BaseCorpus)


def to_params_meta(_params_or_meta,prefix_params='_'):
    params={k:v for k,v in _params_or_meta.items() if k and k[0]==prefix_params}
    meta={k:v for k,v in _params_or_meta.items() if k and k[0]!=prefix_params}
    return (params,meta)


def to_addr(corp,text): 
    if is_corpus_obj(text): corp=corp.id
    if is_text_obj(text): text=text.id
    return f'{IDSEP_START}{corp}{IDSEP}{text}'

def is_addr(idx): return is_our_addr(idx)# or is_db_addr(idx)

def to_corpus_and_id(idx):
    if is_addr(idx):
        return tuple(idx[len(IDSEP_START):].split(IDSEP,1))
    return ('',idx)

def is_our_addr(idx):
    return type(idx)==str and idx and idx.startswith(IDSEP_START) and IDSEP in idx


def addr_to_corpus(addr):
    if addr.startswith(IDSEP_START) and IDSEP in addr:
        return addr[1:].split(IDSEP)[0].strip()
def addr_to_id(addr):
    if addr.startswith(IDSEP_START) and IDSEP in addr:
        return addr.split(IDSEP,1)[-1].strip()






def just_params(d):
    od={k:('' if not v else v) for k,v in dict(d).items() if k and k[0]=='_'}
    return od



def just_meta(d):
    od={k:v for k,v in dict(d).items() if k and (k in OK_META_KEYS or k[0]!='_')}
    return od

def just_meta_no_id(d):
    od={k:v for k,v in dict(d).items() if k and k not in OK_META_KEYS and k[0]!='_'}
    return od


#### ADDRESS MANAGEMENT

def merge_dict(*ld):
    odx={}
    for d in ld: odx={**odx,**safebool(d)}
    return odx



def getattribute(obj,name):
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        return None


def ensure_dir_exists(path,fn=None):
    import os
    if not path: return ''
    try:
        if fn is None and os.path.splitext(path)!=path: fn=True
        if fn: path=os.path.dirname(path)
        if not os.path.exists(path): os.makedirs(path)
    except AssertionError:
        pass


def get_backup_fn(fn,suffix='bak'):
    name,ext=os.path.splitext(fn)
    return f'{name}.bak{ext}'

def backup_fn(fn,suffix='bak',copy=True,move=True,**kwargs):
    """
    `move` is reset to False if copy == True
    """
    if copy: move=False
    if os.path.exists(fn):
        ofn=get_backup_fn(fn)
        if copy: shutil.copy(fn,ofn)
        if move: shutil.move(fn,ofn)



def rmfn(fn):
    if os.path.exists(fn):
        try:
            os.unlink(fn)
        except AssertionError as e:
            pass






import numpy as np
def safebool(x,bad_vals={np.nan}):
    if is_dictish(x):
        return {
            k:v
            for k,v in x.items()
            if safebool(k) and safebool(v)
        }

    import pandas as pd
    try:
        if is_hashable(x) and x in bad_vals: return False
    except AssertionError as e:
        log.error(e)
    
    try:
        if is_iterable(x): return bool(len(x))
    except AssertionError as e:
        log.error(e)
    
    try:
        if pd.isnull(x) is True: return False
    except AssertionError as e:
        log.error(e)

    try:
        return bool(x)
    except AssertionError as e:
        log.error(e)
        return None

def safeget(x,k):
    try:
        return x.get(k)
    except AssertionError:    
        try:
            return x[k]
        except AssertionError:
            pass
    

def safejson(obj):
    import orjson
    return orjson.loads(orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY))










def is_hashable_rly(v):
    """Determine whether `v` can be hashed."""
    try:
        hash(v)
        return True
    except Exception:
        return False

def is_hashable(v):
    from collections.abc import Hashable
    return isinstance(v,Hashable) and is_hashable_rly(v)

def is_dictish(v):
    from collections.abc import MutableMapping
    return isinstance(v, MutableMapping)

def is_iterable(v):
    from collections.abc import Iterable
    return isinstance(v,Iterable)

























def setup():
    from dialectics import log,PATH_HOME,PATH_DATA,PATH_CONFIG,PATH_CORPORA
    # create paths
    for path in [PATH_HOME,PATH_DATA,PATH_CONFIG,PATH_CORPORA]:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                log.error(e)

    log.info('ready')



def get_func_str_parts(xstr_or_l):
    if not xstr_or_l: return []
    if type(xstr_or_l)==str:
        l=xstr_or_l.split(',')
    elif is_iterable(xstr_or_l):
        l=xstr_or_l
    else:
        l=[]
    l=[x.strip() for x in l if x.strip()]
    return l 




import hashlib
from base64 import b64encode

def as_bytes(x): return x.encode() if type(x)!=bytes else x
def hash_md5(x): return b64encode(hashlib.md5(as_bytes(x)).digest()).decode()
def hash_sha256(x): return b64encode(hashlib.sha256(as_bytes(x)).digest()).decode()
def hash_sha224(x): return b64encode(hashlib.sha224(as_bytes(x)).digest()).decode()
def h6(w): return hash_md5(w)[:6]
def h10(w): return hash_sha256(w)[:6]
def h1(w): return hashlib.md5(as_bytes(w)).hexdigest()
def h4(w): return hash_md5(w)[:7]
def hashstr(x): return hashlib.sha224(str(x).encode('utf-8')).hexdigest()

## mine:
def h5(w): return hash_sha256(w)[:5]
def hashed(w): return h5(w)


def nhash(x,n=5,hasher=hash_md5,alnum=False):
    xhash = hasher(x)
    if alnum: xhash=''.join(y for y in xhash if y.isalnum())
    return xhash[:n]

def safehash(x,n=5): return nhash(x,n=n,hasher=hash_md5,alnum=True)

def in_jupyter(): return sys.argv[-1].endswith('json')

def get_tqdm(*args,desc='',**kwargs):
    if desc: desc=f'[{gettimestamp()}] {desc}'
    if in_jupyter():
        from tqdm.notebook import tqdm as tqdmx
    else:
        from tqdm import tqdm as tqdmx
    return tqdmx(*args,desc=desc,**kwargs)






def zeropunc(x,allow={'_'}):
    if not x: return ''
    return ''.join([y for y in x if y.isalnum() or y in allow])


def addr_to_dbkey(addr):
    return safehash(addr)
    # h=hashstr(addr)
    # # return h[:7]
    # # return h[:2]+'-'+h[2:4]+'-'+h[4:7]
    # return h[:3]+'-'+h[3:7]

# def addrs_to_edbkey(addr1,addr2): 
#     #addrs=tuple(list(sorted([addr1,addr2])))
#     h=hashstr((addr1,addr2))
#     return h[:3]+'-'+h[3:7]





def to_lastname(name):
    if not name: return ''
    name=name.strip()
    if not name: return 'Unknown'
    if ',' in name:
        namel=[x.strip() for x in name.split(',') if x.strip()]
        name=namel[0] if namel else name
    else:
        namel=[x.strip() for x in name.split() if x.strip()]
        name=namel[-1] if namel else name

    # random
    if 'Q' in name:
        ind=name.index('Q')
        try:
            ind2=name[ind+1]
            if ind2.isdigit():
                name=name[:ind]
        except IndexError:
            pass

    return name


def ensure_snake(xstr,lower=True,allow={'_'}):
    if lower: xstr=xstr.lower()
    xstr=xstr.strip().replace(' ','_')
    o='_'.join(
        zeropunc(x,allow=allow)
        for x in xstr.split('_')
    )
    return o



def to_shorttitle(title,
            puncs=':;.([,!?',
            ok={'Mrs','Mr','Dr'},
            title_end_phrases={
                'edited by','written by',
                'a novel','a tale','a romance','a history','a story',
                'a domestic tale',
                'by the author','by a lady','being some','by Miss','by Mr',
                'an historical','the autobiography',
                'being',
                ' by ',
                ' or'
            },
            replacements={
                ' s ':"'s ",
            },
            replacements_o={"'S ":"'s "}
            ):

        if not title: return ''
        ti=title
        ti=ti.strip().replace('—','--').replace('–','-')
        ti=ti.title()
        for x,y in replacements.items(): ti=ti.replace(x.title(),y)
        if any(x in ti for x in puncs):
            for x in puncs:
                o2=ti.split(x)[0].strip()
                if o2 in ok: continue
                ti=o2
        else:
            l=list(title_end_phrases)
            l.sort(key = lambda x: -len(x))
            for x in l:
                # log(x+' ?')
                ti=ti.split(x.title())[0].strip()
        o=ti.strip()
        for x,y in replacements_o.items(): o=o.replace(x,y)
        return o






















def get_addr_str(text=None,corpus=None,source=None,**kwargs):
    from dialectics.corpora import Corpus
    corpus=Corpus(corpus)

    # rescue via source?
    if text is None:
        if source is not None: return get_addr_str(source,corpus,None,**kwargs)
        return get_addr_str(
            get_idx(
                # i=corpus.num_texts+1 if corpus else None,
                **kwargs),
                corpus,
            **kwargs
        )
    
    # corpus set? if not, work to get it so
    if not corpus:
        if is_text_obj(text): return text.addr
        if type(text)==str:
            cx,ix = to_corpus_and_id(text)
            if cx and ix: return text
            if ix: return get_addr_str(ix,TMP_CORPUS_ID,**kwargs)
        return get_addr_str(text,TMP_CORPUS_ID,**kwargs)

    # now can assume we have both corpus and text
    corpus = corpus.id if is_corpus_obj(corpus) else str(corpus)
    idx=get_idx(text)
    cpref=IDSEP_START + corpus + IDSEP
    o=cpref + idx if not idx.startswith(cpref) else idx
    if log>3: log(f'-> {o}')
    return o


      
def dict_to_addr(d1={},**d2):
    d={**d1,**d2}
    addr,id,corp=d.get(COL_ADDR),d.get(COL_ID),d.get(COL_CORPUS)
    if addr: return addr
    if id and corp: return to_addr(id,corp)
    if id and is_addr(id): return id
    # if not id: id=d.get('_id')
    
    # if 'corpus' in d: d[]
    raise Exception(f"Where is the id? {d}")


def get_imsg(__id=None,__corpus=None,__source=None,**kwargs):
    o=[]
    _id,_corpus,_source = __id,__corpus,__source
    if _id: o.append(f'id = {_id}')
    if _corpus: o.append(f'corpus = {_corpus}')
    if _source: o.append(f'source = {_source}')
    if kwargs: o.append(f'kwargs = {str(kwargs)[:100]})')
    # if kwargs: o.append(f'kwargs = {list(kwargs.keys())}')
    return ', '.join(o) if o else ''




def is_textish(obj):
    return is_text_obj(obj) or is_addr(obj)




def TextKeys(id=None,_corpus=None,_load=True,_force=False,_id=None,_addr=None,**kwargs):
    if type(id)==dict:
        odx=merge_dict(id, kwargs, dict(_corpus=_corpus,_force=_force,_id=_id,_addr=_addr))
        return TextKeys(**odx)

    # in case we have addr
    for idx in [_addr,_id,id]:
        if is_textish(idx):
            idx=idx.addr if is_text_obj(idx) else idx
            return get_textkeys_addr(idx)# if not _corpus else get_textkeys_id_corpus(idx,_corpus,_source=idx)
    
    # contingencies...
    if _id and not id: id=_id
    

    # if not corpus...
    if not _corpus:
        # if id already text -- give it back immediately
        if is_text_obj(id): return id

        ## if no id at all -- give both defaults
        if not id:
            _corpus,id=TMP_CORPUS,get_idx()
        
        # if id...
        else:
            ## if id already an address -- parse it
            if is_addr(id):
                _corpus,id=to_corpus_and_id(id)
            # if not, then keep this id but use default corpus
            else:
                _corpus=TMP_CORPUS
    
    # if IS a corpus...
    else:
        # if no id
        if not id:
            id=get_idx()
        # if IS id
        else:
            # already a text? add as source?
            if is_textish(id):
                _source = id
            else:
                # normal situation! corpus and id
                pass

    assert id and _corpus
    return get_textkeys_id_corpus(id,_corpus)


def get_textkeys_addr(addr,_clean=True,**extra):
    assert is_addr(addr)

    # clean!  ## all comes through here?
    if _clean: addr = get_idx(addr)
    ####

    _corpus,id = to_corpus_and_id(addr)
    key = addr_to_dbkey(addr)
    dbid = f'{TEXT_COLLECTION_NAME}/{key}'
    return dict(
        _id=dbid,
        _key=key,
        _addr=addr,
        _corpus=_corpus,
        id=id,
        **extra
    )
def get_textkeys_id_corpus(id,_corpus,**kwargs):
    addr = to_addr(_corpus,id)
    return get_textkeys_addr(addr,**kwargs)














### Funcs



META_KEYS_USED_IN_AUTO_IDX = {
    'author',
    'title',
    'edition',
    'year',
    'publisher',
    'vol',
}

# def get_idx_from_meta(meta,sep_kv='=',sep='/',hidden='_'):
#     o=[]
#     for k,v in sorted(meta.items()):
#         if k and k[0]!=hidden:
#             o.append(f'{k}{sep_kv}{v}')
#     ostr=sep.join(o)
#     return get_idx(ostr)

def get_idx_from_meta(
        meta,
        keys=META_KEYS_USED_IN_AUTO_IDX,
        sep_kv='=',
        sep='/',
        hidden='_'):
    o=[]
    for k in keys:
        v = get_prop_ish(meta,k)
        if v is not None:
            o.append(f'{k}{sep_kv}{v}')
    o.sort()
    ostr=sep.join(o)
    return get_idx(ostr) if o else None

def get_idx_from_int(i=None,numzero=5,prefstr='T'):
    if not i:
        numposs=int(f'1{"0"*5}')
        i=random.randint(1,numposs-1)
    return f'{prefstr}{i:0{numzero}}'


def get_idx(
        id=None,
        i=None,
        allow='_/.-:,=',
        prefstr='T',
        numzero=5,
        use_meta=True,
        force_meta=True,
        **meta):
    
    from dialectics import log
    if is_text_obj(id): return id.id
    id1=id
    if log>1: log(f'<- id = {id}, i = {i}')
    # already given?
    if safebool(id):
        if type(id)==str:
            id = ensure_snake(
                str(id),
                allow=allow,
                lower=False
            )
            if log>2:
                if log: log(f'id set via `id` str: {id1} -> {id}')
        
        elif type(id) in {int,float}:
            id = get_idx_from_int(int(id))
            if log>1: log(f'id set via `id` int: {id1} -> {id}')
        
        else:
            raise Exception(f'What kind of ID is this? {type(id1)}')

    else:
        if meta and (force_meta or (use_meta and not i)):
            id = get_idx_from_meta(meta)
            if log>1: log(f'id set via `meta`: {id1} -> {id}')
        elif i:
            id = get_idx_from_int(i,numzero=numzero,prefstr=prefstr)
            if log>1: log(f'id set via `i` int: {id1} -> {id}')

    
    if not id:
        id = get_idx_from_int(numzero=numzero,prefstr=prefstr) # last resort
        if log>1: log(f'id set via random int: {id1} -> {id}')
    
    if not id: raise Exception('what happened?')
        
    if log>1: log(f'-> {id}')
    return id






from collections import MutableMapping,defaultdict
class OrderedSetDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
    function before accessing the keys"""

    def __init__(self, *args, flatten=False, **kwargs):
        self.store = defaultdict(list)
        self.store_set = defaultdict(set)
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        self.flatten = flatten

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        vals = [v for v in value] if type(value) in {list,set} else [value]
        for v in vals:
            if is_hashable(v):
                if not v in self.store_set[key]:
                    self.store_set[key]|={v}
                    self.store[key]+=[v]
            elif type(v)==dict:
                if self.flatten:
                    for vk,vv in v.items():
                        key2 = f'{key}_{vk}'
                        print([key2,vv])
                        if is_hashable(vv):
                            if vv not in self.store_set[key2]:
                                self.store[key2]+=[vv]
                                self.store_set[key2]|={vv}
                        else:
                            self.store[key2]+=[vv]
                else:
                    self.store[key]+=[v]
            else:
                self.store[key]+=[v]


    def __delitem__(self, key):
        del self.store[key]
        del self.store_set[key]

    def __iter__(self):
        return iter(self.store)
    
    def __len__(self):
        return len(self.store)

    def to_dict(self):
        return {
            k:(val[0] if len(val)==1 else val)
            for k,val in self.store.items()
        }






def readtxt(path):
    with open(path,errors='ignore',encoding='utf-8') as f: return f.read()







def tokenize_agnostic(txt):
    return re.findall(r"[\w']+|[.,!?; -—–\n]", txt)
    
def tokenize_fast(line,lower=False):
    line = line.lower() if lower else line
    import re
    # tokenize using reg ex (fast)
    tokens = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",line)
    # remove punctuation on either end
    from string import punctuation
    tokens = [tok.strip(punctuation) for tok in tokens]
    # make sure each thing in list isn't empty
    tokens = [tok for tok in tokens if tok]
    return tokens

# tokenize
def tokenize_nltk(txt,lower=False):
    # lowercase
    txt_l = txt.lower() if lower else txt
    # use nltk
    tokens = nltk.word_tokenize(txt_l)
    # weed out punctuation
    tokens = [
        tok
        for tok in tokens
        if tok[0].isalpha()
    ]
    # return
    return tokens

def tokenize(txt,*x,**y):
    return tokenize_fast(txt,*x,**y)




def slices(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


