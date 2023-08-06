from .imports import *




### handy things

def sync(corpora=INIT_DB_WITH_CORPORA,reverse=False):
    corpora=sorted([c for c in corpora],reverse=reverse)
    for c in get_tqdm(corpora,desc='Syncing corpora'):
        Corpus(c).sync()





## convenient names/funcs
BaseText.textspace = BaseText.db = BaseText.tspace = BaseText.tdb = tspace = TS = textspace = Textspace()
BaseText.relspace = BaseText.rdb = rspace = RS = relspace = Relspace()
Text.find = BaseText.find = find_texts = find = tspace.find
BaseText.lookfor = BaseText.search = search_texts = lookfor_texts = lookfor = look_for = look = tspace.look