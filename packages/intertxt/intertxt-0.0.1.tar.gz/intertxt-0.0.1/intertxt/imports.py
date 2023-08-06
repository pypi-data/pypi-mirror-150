#print(__file__,'imported')
import os,sys
from pathlib import Path
PATH_USER_HOME = str(Path.home())
PATH_HOME = os.path.join(PATH_USER_HOME,'intertxt')
PATH_DATA = os.path.join(PATH_HOME,'data')
PATH_CONFIG = os.path.join(PATH_HOME,'config')
PATH_CORPORA = os.path.join(PATH_HOME,'corpora')
TO_SCREEN = True
TO_FILE = True

SERVERS=[
    'http://128.232.229.63:8529'
]
COL_ID='id'
COL_ADDR='_id'
COL_CORPUS='_corpus'
IDSEP_START='_'
IDSEP='/'
IDSEP_DB='__'

INIT_DB_WITH_CORPORA = {
	# 'bpo',
	'chadwyck',
	'chicago',
	'markmark',
	'txtlab',
	'tedjdh',
	'gildedage',
	# 'canon_fiction',
	'clmet',
	'dta',
	'dialnarr',
	'estc',
	'eebo_tcp',
	'ecco_tcp',
	'ecco',
	'evans_tcp',
	'litlab',
	# 'ravengarside',
	'semantic_cohort',
	'spectator'
}




### stdlib
import tempfile
from zipfile import BadZipFile
import shutil
import tempfile,sys,shutil,os,random


## external
import pandas as pd
import numpy as np
import humanize



## me
from .logs import *
with Log('booting'):
	from .utils import *
	from .models import *
	from .database import *
	from .text import *
	from .textlist import *
	from .corpus import *
	from .rels import *
	from .database import _ADB_ as db,_ADB_CLIENT as client,_ADB_SYSDB as sysdb
