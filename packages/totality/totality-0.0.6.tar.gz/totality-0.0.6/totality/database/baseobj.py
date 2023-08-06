#print(__file__,'imported')
from totality.imports import *

class BaseObject(object):
    __COLLECTION__='obj'

    def __getattr__(self,key):
        x=getattribute(self,key)
        if x: return x

        if key.startswith('path_'):
            pkey=key[5:]
            if pkey:
                x=self.paths.get(pkey)
                if x: return x

        if key.startswith('url_'):
            pkey=key[4:]
            if pkey:
                x=self.urls.get(pkey)
                if x: return x
        return None
    
    @property
    def paths(self): return {}
    @property
    def path(self): return self.paths.get('root')









    ### downloading
    def download(self,parts='metadata',**kwargs):
        for part in get_func_str_parts(parts):
            func=getattr(self,f'download_{part}')
            if func is not None:
                func(**kwargs)

    
    def download_metadata(self,force=False):
        url,opath=self.url_metadata,self.path_metadata
        if url and opath:
            if force or not os.path.exists(opath):
                download(url,opath)
    
    def download_txt(self,force=False):
        url,opath=self.url_txt,self.path
        if url and opath: download(url,opath)
    
