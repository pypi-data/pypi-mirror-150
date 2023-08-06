#print(__file__,'imported')
from .utils import *
from .logs import Log
from .misc import get_tqdm

def writegen_jsonl(fnfn,generator,args=[],kwargs={}):
    import jsonlines
    with jsonlines.open(fnfn,'w') as writer:
        for i,dx in enumerate(generator(*args,**kwargs)):
            writer.write(dx)
    print('>> saved:',fnfn)

def readgen_jsonl(fnfn):
    import jsonlines
    with jsonlines.open(fnfn) as reader:
        for dx in reader:
            yield dx


def printm(x):
    from IPython.display import display,Markdown
    display(Markdown(x))


def writegen(fnfn,generator,header=None,args=[],kwargs={},find_all_keys=False,total=None,progress=False,delimiter=','):
    from tqdm import tqdm
    import csv,gzip

    if not header:
        iterator=generator(*args,**kwargs)
        if not find_all_keys:
            first=next(iterator)
            header=sorted(first.keys())
        else:
            print('>> finding keys:')
            keys=set()
            for dx in iterator:
                keys|=set(dx.keys())
            header=sorted(list(keys))
            print('>> found:',len(header),'keys')

    iterator=generator(*args,**kwargs)
    if progress or total: iterator=get_tqdm(iterator,total=total)

    with (open(fnfn, 'w') if not fnfn.endswith('.gz') else gzip.open(fnfn,'wt')) as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=header,extrasaction='ignore',delimiter=delimiter)
        writer.writeheader()
        for i,dx in enumerate(iterator):
            #for k,v in dx.items():
            #	dx[k] = str(v).replace('\r\n',' ').replace('\r',' ').replace('\n',' ').replace('\t',' ')
            writer.writerow(dx)
    print('>> saved:',fnfn)
    

# def writegen(fnfn,generator,header=None,args=[],kwargs={},find_all_keys=False,total=None):
# 	from tqdm import tqdm
# 	import codecs,csv
# 	if 'jsonl' in fnfn.split('.'): return writegen_jsonl(fnfn,generator,args=args,kwargs=kwargs)

# 	iterator=generator(*args,**kwargs)
# 	if total: iterator=get_tqdm(iterator,total=total)
# 	if not header:
# 		if not find_all_keys:
# 			first=next(iterator)
# 			header=sorted(first.keys())
# 		else:
# 			print('>> finding keys:')
# 			keys=set()
# 			for dx in iterator:
# 				keys|=set(dx.keys())
# 			header=sorted(list(keys))
# 			print('>> found:',len(header),'keys')

# 	iterator=generator(*args,**kwargs)
# 	with open(fnfn, 'w') as csvfile:
# 		writer = csv.DictWriter(csvfile,fieldnames=header,extrasaction='ignore',delimiter='\t')
# 		writer.writeheader()
# 		for i,dx in enumerate(iterator):
# 			for k,v in dx.items():
# 				#if type(v) in [str]:
# 				#	dx[k]=v.encode('utf-8')
# 				dx[k] = str(v).replace('\r\n',' ').replace('\r',' ').replace('\n',' ').replace('\t',' ')
# 			writer.writerow(dx)
# 	print('>> saved:',fnfn)

def writegen_orig(fnfn,generator,header=None,args=[],kwargs={}):
    if 'jsonl' in fnfn.split('.'): return writegen_jsonl(fnfn,generator,args=args,kwargs=kwargs)
    with codecs.open(fnfn,'w',encoding='utf-8') as of:
        for i,dx in enumerate(generator()):
            if not header: header=sorted(dx.keys())
            if not i: of.write('\t'.join(header) + '\n')
            of.write('\t'.join([str(dx.get(h,'')) for h in header]) + '\n')
    print('>> saved:',fnfn)

def writegengen(fnfn,generator,header=None,save=True):
    if save: of = codecs.open(fnfn,'w',encoding='utf-8')
    for dx in generator():
        if not header:
            header=sorted(dx.keys())
            if save: of.write('\t'.join(header) + '\n')
        if save: of.write('\t'.join([str(dx.get(h,'')) for h in header]) + '\n')
        yield dx


def nicedirname(dirname):
    home=os.path.expanduser('~')
    if not home.endswith(os.path.sep): home+=os.path.sep
    absp=os.path.abspath(dirname)
    return absp.replace(home,'~/')

def getheader(fn,sep=','):
    if not os.path.exists(fn): return []
    with open(fn) as f: line=next(f)
    return [x.strip() for x in ln.strip().split(sep) if x.strip()]

def getheader_and_numlines(fn,sep=','):
    if not os.path.exists(fn): return []
    line1=''
    numlines=0
    with open(fn) as f:
        for line in f:
            line=line.strip()
            if line:
                numlines+=1
                if numlines==1: line1=line
    if not line1: return
    header=[x.strip() for x in line1.strip().split(sep) if x.strip()]
    numlines=i+1
    return (header,numlines)

def parse_csv_line(linestr):
    import csvloader
    if type(linestr)!=str or not linestr: return []
    res=csvloader.loads(linestr.strip())
    return [(x if x else '') for x in res]


def readgen_csv(fn,sep=None,encoding='utf-8',errors='ignore',header=[],progress=True,num_lines=0,desc='Iterating CSV'):
    header=[x for x in header]
    if os.path.exists(fn):    
        if progress and not num_lines:
            with open(fn,encoding=encoding,errors=errors) as f:
                for _ in f: num_lines+=1
        with open(fn,encoding=encoding,errors=errors) as f:
            if progress:
                desc+=f' [{fn}]'
                iterr=get_tqdm(f,total=num_lines,desc=desc)
            else:
                iterr=f
            for i,ln in enumerate(iterr):
                lndatl=parse_csv_line(ln.strip())
                if len(lndatl)==0:
                    Log().error(f'No data parsed from line: {ln}')
                else:
                    if len(lndatl)>1:
                        Log().warning(f'More than one csv line in a file line? {ln}')
                    # get first ln
                    lndat=lndatl[0]
                    if lndat:
                        # header?
                        if not header:
                            header=lndat
                        else:
                            odx=dict(zip(header,lndat))
                            yield odx


def readgen_csv_orig(fnfn,sep=None,encoding='utf-8',errors='ignore',header=[],progress=True,num_lines=0,desc='Reading CSV file'):
    from smart_open import open
    from csv import reader
    if not sep: sep=',' if fnfn.endswith('csv') or fnfn.endswith('.csv.gz') else '\t'
    if progress and not num_lines:
        with open(fnfn,encoding=encoding,errors=errors) as f:
            for _ in f: num_lines+=1
    
    with open(fnfn,encoding=encoding,errors=errors) as f:
        header_line=next(f)
        if header_line==None: return
        header=list(reader([header_line.strip()]))[0]
        if header!=None:
            iterr=f if not progress else get_tqdm(f,total=num_lines,desc=desc)
            for row in iterr:
                try:
                    data = list(reader([row.strip()]))[0]
                    yield dict(zip(header,data))
                except Exception as e:
                    log.error(e)
                    print(e)
                    stop
                    pass
                

def readgen(fnfn,**y):
    if issubclass(fnfn.__class__,pd.DataFrame): yield from fnfn.reset_index().to_dict('records')
    if type(fnfn)==str and os.path.exists(fnfn):
        ext=os.path.splitext(fnfn)[-1]
        if ext=='.jsonl':
            yield from readgen_jsonl(fnfn,**y)
        elif ext=='.csv':
            yield from readgen_csv(fnfn,**y)
        elif ext=='.txt':
            yield from readgen_csv(fnfn,sep='\t',**y)
        else:
            # print(f'[readgen()] Resorting to non-generator load for {fnfn}')
            df=read_df(fnfn)
            yield from resetindex(df).to_dict('records')

def header(fnfn,tsep='\t',encoding='utf-8'):
    header=[]

    if fnfn.endswith('.gz'):
        import gzip
        of=gzip.open(fnfn)
    #of = codecs.open(fnfn,encoding=encoding)
    else:
        of=open(fnfn)

    for line in of:
        line = line[:-1]  # remove line end character
        line=line.decode(encoding=encoding)
        header=line.split(tsep)
        break
    of.close()
    return header
