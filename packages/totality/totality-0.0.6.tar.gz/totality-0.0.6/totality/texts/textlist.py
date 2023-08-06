from totality.imports import *
from collections import UserList
from .text import Text

class TextList(BaseObject, UserList):
    def __init__(self, l=[],unique=True):
        self.unique = unique
        self.data_all = list(map(Text,l))
        self._g=None
        self.sort()

    def sort(self):
        self.data_all.sort(key=lambda t: t.yr)
        return self

    @property
    def data(self):
        o=None
        if self.unique and self._data_uniq: o=self._data_uniq
        if not o: o=self.data_all
        if not o: o=[]
        return sorted(o,key=lambda t: t.yr)
    
    @property
    def data_uniq(self):
        if not self._data_uniq: self.filter()
        return self._data_uniq
    uniq=data_uniq

    def __iter__(self): yield from self.data
    def __len__(self): return len(self.data_all)

    def __repr__(self,maxnum=25):
        pref='TextList('
        iterr = self.data
        o=[]
        for i,t in enumerate(sorted(iterr,key=lambda t: t.yr)):
            if i:
                prefx=' '*(len(pref)+1)
            else:
                prefx='['
            o+=[prefx + repr(t)]
        o='\n'.join(o)
        if o: return pref + o + '])'
        return f'[TextList]({len(self.data_all)} texts)'
    
    @property
    def addrs(self): return [t.addr for t in self.data_all]
    
    

    def filter(self,text_iter=None,**kwargs):
        if text_iter is None: text_iter = self.data_all
        self._data_uniq = sorted(
            list(self.iter_texts_uniq(self.data_all,**kwargs)),
            key=lambda t: t.year
        )
        if log:
            log(f'data_all={len(self.data_all)}, _data_uniq={len(self._data_uniq)}')
        return self._data_uniq
    filtered=filter
    
    def iter_texts(self,text_iter=None,_unique=True,**kwargs):
        if _unique and self._data_uniq:
            yield from self._data_uniq
        else:
            yield from self.data_all


    def iter_texts_uniq(
            self,
            progress=False,
            force=True,
            force_inner=True,
            desc='[LLTK] iterating distinct texts',
            leave=True,
            **kwargs):

        if False: #not force and self._data_uniq:
            yield from self._data_uniq
        else:
            self._g = g = self.get_matchgraph() if (True or not self._g) else self._g
            if log: log(f'<- matchgraph! = {g}')
            if g and isinstance(g,nx.Graph):
                cmps=list(nx.connected_components(g))
                if 0: cmps=get_tqdm(cmps,desc=desc,leave=leave)
                for i,nodeset in enumerate(cmps):
                    nset=list(nodeset)
                    nset.sort(key=lambda x: CORPUS_SOURCE_RANKS.get(to_corpus_and_id(x)[0],1000))
                    t=Text(nset[0])
                    if log: log(f'{i} {t}')
                    if 0: cmps.set_description(f'{desc}: {t}')
                    yield t


    def quiet(self): self.progress=False
    def verbose(self): self.progress=True

        
        

    @property
    def t(self): return random.choice(self.data)

    def sample(self,n): 
        if n < len(self.data): return random.sample(self.data,n)
        o = [x for x in self.data]
        random.shuffle(o)
        return TextList(o)


    def run(self,func,text_iter=None,*args,**kwargs):
        return llmap(
            self.addrs,
            func,
            *args,
            **kwargs
        )
    map = run
                
    def graph_ties(self,node_name='addr'):
        import networkx as nx
        g = nx.Graph()
        for t in get_tqdm(self.data_all):
            tg=t.graph_ties()
            g = nx.compose(g,tg)

        for node in list(g.nodes()):
            if IDSEP_START+TMP_CORPUS_ID+IDSEP in node:
                g.remove_node(node)

        if node_name!='addr':
            labeld=dict((addr,Text(addr).node) for addr in g.nodes())
            nx.relabel_nodes(g,labeld,copy=False)
        return g
        

    def matchgraph(self,draw=True,node_name='node',**kwargs):
        from lltk.model.networks import draw_nx
        g=self.get_matchgraph(node_name=node_name)
        return g if g is None or not draw else draw_nx(g)



    def init(self,progress=True,**kwargs):
        for t in self.data_all: t.init()
        return self

    def queue_remote_sources(self):
        for t in self: t.queue_remote_sources()


    def get_titlematch_input_df(self):
        df = pd.DataFrame(
            dict(id=t.addr, author=t.au, title=t.ti)
            for t in self
            if t.au and t.ti
        ).set_index('id')
        return df

    def match(self,rel=MATCHRELNAME,_progress=True,**kwargs):
        from totality.models.matching import match_by_title

        inpdf = self.get_titlematch_input_df()
        if not safebool(inpdf): return pd.DataFrame()
        matchdf = match_by_title(inpdf)
        if not safebool(matchdf): return pd.DataFrame()

        iterr=zip(matchdf.id_1,matchdf.id_2)
        if _progress: iterr=get_tqdm(list(iterr))
        for id1,id2 in iterr:
            Text(id1).relate(Text(id2), rel=rel, **kwargs)
        
        return matchdf





    def batches(self,data=None,n=5):
        if not data: data=self.data
        return slices(data,n=n)

    def into_lsh(self,progress=True,batch_n=10):
        from totality.models.matching import get_lsh,get_all_lsh_keys
        lsh = get_lsh()
        lshkeys = get_all_lsh_keys(lsh)
        texts = [t for t in self if t.addr not in lshkeys]
        iterr=self.batches(texts,batch_n)
        if progress: iterr=get_tqdm(list(iterr), desc='LSH batch inserting')
        for batch in iterr:
            with lsh.insertion_session() as session:
                for t in batch:
                    minh = t.minhash()
                    if minh is not None:
                        session.insert(t.addr, minh)
        return lsh

        
    
    def match_by_hash(self,progress=True):
        from totality.models.matching import get_lsh
        lsh = get_lsh()
        iterr=self
        if progress: iterr=get_tqdm(iterr,desc='Finding matches')
        for t in iterr:
            mh=t.minhash()
            if mh:
                for t2addr in lsh.query(mh):
                    if t2addr != t.addr:
                        t2=Text(t2addr)
                        t.relate(t2,rel_type='match_hash')
                        if progress:
                            iterr.set_description(f'Found: {t} --> {t2}')
                        

