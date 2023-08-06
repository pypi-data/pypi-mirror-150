from .imports import *




### handy things

def sync(corpora=INIT_DB_WITH_CORPORA,reverse=False):
    corpora=sorted([c for c in corpora],reverse=reverse)
    for c in get_tqdm(corpora,desc='Syncing corpora'):
        Corpus(c).sync()





## convenient names/funcs
DB = tspace = TS = textspace = Textspace()
find_texts = find = tspace.find
search_texts = lookfor_texts = lookfor = look_for = look = tspace.look