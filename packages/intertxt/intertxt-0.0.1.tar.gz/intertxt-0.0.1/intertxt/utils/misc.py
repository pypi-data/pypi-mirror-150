#print(__file__,'imported')
from .utils import *


def gettimestamp():
    from datetime import datetime
    dt=datetime.now()
    return f'{dt.hour:02}:{dt.minute:02}:{dt.second:02}.{dt.microsecond//1000}'


def is_textish(obj):
    return is_text_obj(obj) or is_addr(obj)

def is_valid_text_obj(obj):
    return is_text_obj(obj) and obj.id_is_valid()

def is_text_obj(obj):
    from intertxt.text import BaseText
    if issubclass(type(obj), BaseText): return True
    return False

def is_corpus_obj(obj): 
    from intertxt.corpus import BaseCorpus
    return issubclass(type(obj), BaseCorpus)


def to_params_meta(_params_or_meta,prefix_params='_'):
    params={k:v for k,v in _params_or_meta.items() if k and k[0]==prefix_params}
    meta={k:v for k,v in _params_or_meta.items() if k and k[0]!=prefix_params}
    return (params,meta)


def to_addr(corp,text): 
    if is_corpus_obj(text): corp=corp.id
    if is_text_obj(text): text=text.id
    return f'_{corp}/{text}'

def is_addr(idx): return is_our_addr(idx) or is_db_addr(idx)

def is_our_addr(idx):
    return type(idx)==str and idx and idx.startswith(IDSEP_START) and IDSEP in idx
def is_db_addr(_id):
    return type(_id)==str and _id and not IDSEP in _id and IDSEP_DB in _id


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
    od={k:v for k,v in dict(d).items() if k and k[0]!='_'}
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
    from intertxt import log,PATH_HOME,PATH_DATA,PATH_CONFIG,PATH_CORPORA
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



def hashstr(x):
    import hashlib
    return hashlib.sha224(str(x).encode('utf-8')).hexdigest()


def in_jupyter(): return sys.argv[-1].endswith('json')

def get_tqdm(*args,desc='',**kwargs):
    if desc: desc=f'[{gettimestamp()}] {desc}'
    if in_jupyter():
        from tqdm.notebook import tqdm as tqdmx
    else:
        from tqdm import tqdm as tqdmx
    return tqdmx(*args,desc=desc,**kwargs)






def zeropunc(x,allowed={'_'}): return ''.join(y for y in x if y.isalpha() or y in allowed)


def addr_to_key(addr):
    # return zeropunc(addr.replace(IDSEP,IDSEP_DB),allowed='_')
    return hashstr(addr)[:13]