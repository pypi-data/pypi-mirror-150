#print(__file__,'imported')
from .imports import *


CORPUS_CACHE={}
def Corpus(id=TMP_CORPUS,_force=False,**kwargs):
    global CORPUS_CACHE
    if not id: return
    if _force or not id in CORPUS_CACHE:
        CORPUS_CACHE[id]=BaseCorpus(id,**kwargs)
    return CORPUS_CACHE[id]



class BaseCorpus(TextList):
    col_id='id'
    col_addr='_id'

    def __init__(self,id=TMP_CORPUS,name=None,**kwargs):
        self.id=zeropunc(id).lower()
        self.name=zeropunc((name if name else id).title())
        self._texts=[]
        self._textd={}
        self._meta=merge_dict(
            kwargs,
            get_corpora_meta().get(self.id,{})
        )

    def __repr__(self):
        return f"Corpus('{self.id}')"

    @property
    def paths(self):
        pathd={}
        pathd['root']=os.path.join(PATH_CORPORA,self.id)
        pathd['metadata']=os.path.join(pathd['root'],'metadata.csv')
        return pathd
        
    @property
    def urls(self):
        return {
            k[4:]:v
            for k,v in self._meta.items()
            if k.startswith('url_')
            and type(v)==str and v and v.startswith('http')
        }


    def text(self,id=None,meta={},_load=None,_i=None,_force=False,**meta2):
        d=merge_dict(meta,meta2)
        meta=just_meta(d)
        # get id
        if not id: id=d.get(self.col_id)
        if not id: id=get_idx(i=_i)        # already have it?
        if not _force and id in self._textd: return self._textd[id]#.init(**meta)
        # prob gonne have to make it
        if _load is None: _load = not d
        t=Text(
            id,             # text id within corpus
            self.id,        # id if corpus
            **meta,
            _load=_load
        )
        self._textd[t.id]=t
        return t

    @property
    def textd(self):
        if not self._textd: self.init()
        return self._textd

    def texts_iter(self):
        return iter(self.textd.values())
    def texts(self):
        return list(self.texts_iter())
    _texts=texts
    @property
    def tl(self): return self.texts()
    @property
    def t(self): return random.choice(self.tl)

    def init_iter(self):
        with Log('Initializing corpus') as log:
            i=0
            for d in self.init_from_db():
                i+=1
                yield self.text(_i=i, **d)
            
            if not i:
                for d in self.init_from_files():
                    i+=1
                    yield self.text(i=i+1, **d)
            log(f'Initialized {i} texts')
    
    def init(self):
        list(self.init_iter())
        return self



    def init_from_file(self,as_text=True):
        with Log('loading corpus from file') as log:
            if not os.path.exists(self.path_metadata):
                self.download_metadata()
            if not os.path.exists(self.path_metadata):
                log.error('No metadata file')
                return
            for d in readgen(self.path_metadata):
                if self.col_id in d and d[self.col_id]:
                    yield d



    @property
    def text_collection(self):
        if not self._text_collection: self._text_collection=get_text_collection()
        return self._text_collection

    def init_from_db(self,as_text=True,progress=True):
        total=self.text_collection.count()
        if total:
            with Log('loading corpus from database') as log:
                iterr=self.text_collection.find({'_corpus':self.id})
                if progress: iterr=get_tqdm(iterr,total=self.text_collection.count())
                for d in iterr:
                    if self.col_id in d and d[self.col_id]:
                            yield d
        

    def sync(self,batch_size=100,**kwargs):
        with Log(f'Syncing {self} into database') as log:
            batch=[]
            coll=self.text_collection
            for d in self.init_from_file():
                id=d.get(self.col_id)
                addr=to_addr(self.id,id)
                odx={
                    '_key':addr_to_key(addr),
                    '_addr':addr,
                    '_corpus':self.id,
                    **just_meta(d)
                }
                batch.append(odx)

                if len(batch)>=batch_size:
                    try:
                        coll.import_bulk(batch)
                    except Exception as e:
                        log.error(e)
                        bids=[x['_addr'] for x in batch]
                        from collections import Counter
                        print(Counter(bids).most_common(10))
                    
                    batch=[]
            if batch:
                try:
                    coll.import_bulk(batch)
                except Exception as e:
                    log.error(e)
                    bids=[x['_addr'] for x in batch]
                    from collections import Counter
                    print(Counter(bids).most_common(10))
        
                








CORPORA_META={}
def get_corpora_meta(force=False):
    global CORPORA_META
    if force or CORPORA_META is not None:
        path=os.path.join(PATH_CORPORA,'metadata.csv')
        df=pd.read_csv(path).fillna('')
        dd=dict((d['id'],d) for d in df.to_dict('records'))
        CORPORA_META=dd
        
    return CORPORA_META


