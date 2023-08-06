#print(__file__,'imported')
from .misc import *
import zipfile,tempfile,shutil


def download(url, save_to, verbose = False, desc=None):
    
    opath=os.path.dirname(save_to) if not os.path.isdir(save_to) else save_to
    ensure_dir_exists(opath,fn=False)
    with tempfile.TemporaryDirectory() as dirname:    
        ofn = download_file_tqdm(url,dirname=dirname)
        if zipfile.is_zipfile(ofn):
            unzip(ofn,opath,overwrite=True)
        else:
            shutil.move(ofn,save_to)
        
        return save_to


#!/usr/bin/env python 
__author__  = "github.com/ruxi"
__license__ = "MIT"
def download_file_tqdm(url, filename=False, dirname = ".", verbose = False, desc=None):
    """
    Download file with progressbar
    """

    import requests 
    import os.path


    if not filename:
        local_filename = os.path.join(url.split('?')[0].split('/')[-1])
    else:
        local_filename = filename

    if dirname and not os.path.isabs(local_filename): local_filename=os.path.join(dirname,local_filename)
    
    r = requests.get(url, stream=True)
    file_size = r.headers.get('content-length')
    chunk = 1
    chunk_size=1024
    num_bars = int(file_size) // chunk_size if file_size else None
    if verbose>0:
        print(dict(file_size=file_size))
        print(dict(num_bars=num_bars))

    ensure_dir_exists(local_filename,fn=True)
    with open(local_filename, 'wb') as fp:
        iterr=get_tqdm(
            r.iter_content(chunk_size=chunk_size),
            total=num_bars,
            unit='KB',
            desc = f'Downloading {os.path.basename(local_filename)}' if not desc else desc,
            leave = True
        )
        for chunk in iterr:
            fp.write(chunk)
    return local_filename







def unzip(zipfn, dest='.', flatten=False, overwrite=False, replace_in_filenames={},desc='',progress=True):
    from zipfile import ZipFile
    from tqdm import tqdm

    # Open your .zip file
    if not desc: desc=f'Extracting {os.path.basename(zipfn)} to {dest}'
    with ZipFile(zipfn) as zip_file:
        namelist=zip_file.namelist()

        # Loop over each file
        iterr=get_tqdm(iterable=namelist, total=len(namelist),desc=desc) if progress else namelist
        for member in iterr:
            # Extract each file to another directory
            # If you want to extract to current working directory, don't specify path
            filename = os.path.basename(member)
            if not filename: continue
            target_fnfn = os.path.join(dest,member) if not flatten else os.path.join(dest,filename)
            for k,v in replace_in_filenames.items(): target_fnfn = target_fnfn.replace(k,v)
            if not overwrite and os.path.exists(target_fnfn): continue
            target_dir = os.path.dirname(target_fnfn)
            try:
                if not os.path.exists(target_dir): os.makedirs(target_dir)
            except FileExistsError:
                pass
            except FileNotFoundError:
                continue
            try:
                with zip_file.open(member) as source, open(target_fnfn,'wb') as target:
                    shutil.copyfileobj(source, target)
            except FileNotFoundError:
                print('!! File not found:',target_fnfn)



