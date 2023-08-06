#print(__file__,'imported')
from totality.imports import *
log = Log()




def Text(id=None, _corpus=None, _force=False, **kwargs):
    global TEXT_CACHE
    from totality.corpora import Corpus

    if not _corpus and is_text_obj(id): return id
    
    keys = TextKeys(id=id, _corpus=_corpus, **kwargs)
    addr = keys.get(COL_ADDR)
    if not _force and addr in TEXT_CACHE:
        t = TEXT_CACHE[addr]
    else:
        corp,id=keys.get(COL_CORPUS),keys.get(COL_ID)
        t = TEXT_CACHE[addr] = Corpus(corp).text(id,**kwargs)
    
    return t


class BaseText(BaseObject):
    __COLLECTION__=TEXT_COLLECTION_NAME

    def __init__(self,id=None,_corpus=None,_source=None,**kwargs):
        self._keys=TextKeys(id=id,_corpus=_corpus,_source=_source,**kwargs)
        self._data=kwargs
        self._node=None

    @property
    def paths(self):
        pathd={}
        pathd['corpus']=os.path.join(PATH_CORPORA,self._corpus)
        pathd['root']=os.path.join(pathd['corpus'],'texts',self.id)
        pathd['txt']=os.path.join(pathd['root'],'text.txt')
        pathd['txt_']=os.path.join(pathd['corpus'],'txt',self.id+'.txt')
        return pathd


    # def __str__(self):
        # return f"Text('{self._addr}')"

    def __repr__(self):
        return self.nice
    
    def is_valid(self):
        return self.addr and is_addr(self.addr)

    @property
    def nice(self,force=True):
        if not self.is_valid(): return ''
        yr,au,ti,addr = self.yr, self.au, self.ti, self.addr
        austr=f"{au}, " if au else ""
        tistr=f"{ti.upper()[:50].strip()} " if ti else ""
        yrstr=f"({int(yr)}) " if safebool(yr) else ""
        addrstr=f"[{addr}] <{self._key}>"
        return ''.join([austr,tistr,yrstr,addrstr])

    def __getattr__(self,key):
        res = super().__getattr__(key)
        if res is not None: return res

        dicts = [(self,'_keys'), (self,'_data')]
        for obj,attrname in dicts:
            if hasattr(obj,attrname):
                attr=getattr(obj,attrname)
                if is_dictish(attr) and key in attr:
                    res = attr.get(key)
                    if res is not None:
                        return res

        if hasattr(self,'_data') and is_dictish(self._data) and key in self._data:
            res = self._data.get(key)
            if res is not None: return res
        
        return None


    @property
    def au(self):
        return zeropunc(to_lastname(self.author))
    @property
    def ti(self): return to_shorttitle(self.title)
    @property
    def yr(self): return pd.to_numeric(self.year,errors='coerce')
    

    @property
    def _meta(self):
        return self.ensure_id(just_meta(self._data))
    meta=_meta
    data=_meta
    @property
    def _params(self): return self.ensure_id(just_params(self._data))
    @property
    def addr(self): return to_addr(self._corpus, self.id)
    _addr=addr
    @property
    def corpus(self):
        if not self._corpusobj:
            from totality.corpora import Corpus
            self._corpusobj=Corpus(self._corpus) 
        return self._corpusobj
    
    
    @property
    def _qmeta(self):
        return {
            'au':self.au,
            'ti':self.ti,
            'yr':self.yr,
        }

    def ensure_id(self,d={},idkey='_id',**kwargs):
        newmeta=just_meta(merge_dict(self._data, d, kwargs))
        return merge_dict(
            self._keys,
            self._qmeta,
            newmeta,
        )





    @property
    def coll(self): return Textspace().coll
    collection=coll
    
    ## database funcs
    def load(self,force=False):
        if force or not self._loadd:
            data = self.coll.get(self._key)
            if data: self._data={**self._data,**just_meta(data)}
            self._loadd=True

    def update(self,**meta):
        #meta1=self._meta
        for k,v in meta.items(): self._data[k]=v
        #meta2=self._meta
        # if meta1!=meta2:
            # if log: log(f'updating db record for {self}')
            # self.save()
        
    def init(self,force=False,**kwargs):
        self.load(force=force)
        self.update(**kwargs)
        return self
    
    def exists(self):
        return self._key in self.collection
    
    def upsert(self,d={},tryagain=True):
        to_insert = safebool(safejson(self.ensure_id(d)))
        saved_meta={}
        try:
            saved_meta = self.coll.update(to_insert)
        except Exception as e:
            if log>2: log.error(e)
            try:
                saved_meta = self.coll.insert(to_insert)
            except Exception as e:
                if log: log.error(f'{e}. d = {to_insert}')
        if log>1: log(saved_meta)
        return {**to_insert, **saved_meta}
        
    
    def save(self):
        # with Log(f'Saving {self} in database')
        saved_meta=self.upsert()
        if not saved_meta: return
        assert saved_meta['_key'] == self._key
        self._data = {**self._data, **just_meta(saved_meta)}
        return saved_meta

    





    ### RELATIONS


    def relate(self,other,rel=MATCHRELNAME,rel_type='',yn='',**kwargs):
        from totality.database import Relspace
        other = Text(other)
        return Relspace().link(self,other,rel=rel,rel_type=rel_type,yn=yn,**just_meta_no_id(kwargs))
    
    def strong_ties(self, relspace='is_also', data=False, direction=None):
        from .textlist import TextList

        rs = Relspace(relspace)
        res=rs.graph.edges(rs.name, self._id, direction=direction)
        if type(res)!=dict or not res: return []
        res = res.get('edges')
        if type(res)!=list: return []
        
        ## otherwise
        me_id = self._id
        o=[]
        for d in res:
            you_id = d.get('_from') if d.get('_from')!=me_id else d.get('_to')
            u=self
            v=Textspace().get(you_id)
            o.append((v,d) if data else v)
        return o if not data else o
    neighbors=strong_ties
        
    def traverse_ties(self,
            direction="any",
            strategy="depthfirst",
            max_depth=2,
            **kwargs):
        from .textlist import TextList
        
        return Relspace().graph.traverse(
            start_vertex=self._id,
            direction=direction,
            max_depth=max_depth,
            strategy=strategy,
            **kwargs
        )

    def weak_ties(self,data=False,**kwargs):
        from .textlist import TextList
        all_ties = {Text(d) for d in self.traverse_ties(**kwargs)}
        strong_ties = set(self.strong_ties())
        weak_ties = all_ties - strong_ties - {self}
        return weak_ties if not data else [(t,{}) for t in weak_ties]

    def graph_ties(self,**kwargs):
        import networkx as nx
        g=nx.DiGraph()
        traversal_data = self.traverse_ties(**kwargs)
        for pathd in traversal_data.get('paths',[]):
            for edged in pathd.get('edges'):
                t1=Textspace().get(edged.get('_from'))
                t2=Textspace().get(edged.get('_to'))
                g.add_edge(t1.nice, t2.nice, **edged)
        return g

    def draw_ties(self,g=None,**kwargs):
        from totality.models.networks import draw_nx
        if g is None: g=self.graph_ties(**kwargs)
        return draw_nx(g)
        





    def get_txt(self,sources=False):
        if self._txt: return self._txt
        for pathtype,path in self.paths.items():
            if pathtype.startswith('txt') and os.path.exists(path):
                txt=readtxt(path)
                if txt: 
                    return txt
        
        if sources:
            for src in self.strong_ties():
                txt=src.get_txt(sources=False)
                if txt: return txt
        
        return ''

    @property
    def txt(self): return self.get_txt()

    def tokens(self,tokenizer=tokenize_fast,lower=True):
        return tokenizer(
            self.txt.lower() if lower else self.txt
        )

    def counts(self,tokens=None,**kwargs):
        if not tokens: tokens=self.tokens(**kwargs)
        return Counter(tokens)



    def minhash(self,cache=True,force=False):
        if not self._minhash:
            words = self.tokens()
            if not words: return None
            
            from datasketch import MinHash
            self._minhash = m = MinHash(num_perm=HASH_NUMPERM)
            for word in self.tokens(): m.update(word.encode('utf-8'))
        return self._minhash

    def hashdist(self,text,cache=True):
        m1=self.minhash(cache=cache)
        m2=text.minhash(cache=cache)
        return 1 - m1.jaccard(m2)


