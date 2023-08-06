# -*- coding: utf-8 -*-
import os
import re
import copy
import csv
import json


from ipylib.idebug import *
from ipylib.ipath import *
from ipylib.ipath import clean_path
from ipylib.idatetime import DatetimeParser
from ipylib.inumber import *


__all__ =[
    'get_filenames',
    'get_dirs',
    'get_filepaths',
    'open_file',
    'write_file',
    'FileReader',
    'FileWriter',
]



def get_filenames(path):
    fnames = []
    with os.scandir(clean_path(path)) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                fnames.append(entry.name)
    return sorted(fnames)

def get_dirs(path, alldepth=False):
    all_dirs = []
    for root, dirs, files in os.walk(top=clean_path(path), topdown=True):
        if alldepth:
            for dir in dirs:
                all_dirs.append(dir)
        else:
            if root == path:
                all_dirs = dirs
                break
    return sorted(all_dirs)

def get_filepaths(path, alldepth=True, topdown=True):
    filepaths = []
    for root, dirs, files in os.walk(top=clean_path(path), topdown=topdown):
        for file in files:
            if alldepth:
                filepaths.append(os.path.join(root, file))
            else:
                if root == path:
                    filepaths.append(os.path.join(root, file))
    filepaths = [e for e in filepaths if e not in ['.DS_Store']]
    return sorted(filepaths)

def open_file(filepath):
    dbg.printer(f"filepath : {filepath}")
    try:
        with open(file=filepath, mode='r') as f:
            text = f.read()
            f.close()
            return text
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.open_file")

def _makedirs(filepath):
    try:
        os.makedirs(os.path.dirname(filepath))
    except Exception as e:
        pass

def write_file(filepath, text):
    dbg.printer(f"filepath : {filepath}")
    _makedirs(filepath)
    with open(file=filepath, mode='w') as f:
        f.write(text)
        f.close()


def search_file(dir, filename):
    for root, dirs, files in os.walk(top=dir, topdown=True):
        for name in files:
            f, ext = os.path.splitext(name)
            if f == filename:
                filepath = os.path.join(root, name)
                return filepath

class FileReader:

    @classmethod
    def _clean(self, data):
        for d in data:
            for k,v in d.copy().items():
                if isinstance(v, str) and len(v.strip()) == 0: del d[k]
        return data
    @classmethod
    def read_text(self, file):
        try:
            f = open(file, mode='r', encoding='utf-8')
            text = f.read()
            f.close()
        except Exception as e:
            logger.error(f'{self} | {e} | TEXT파일이 존재하지 않는다. {file}')
        else:
            logger.info(f'{self} | FilePath--> {file}')
            return text.strip()
    @classmethod
    def read_csv(self, file):
        try:
            data = []
            with open(file, newline='\n', encoding='utf8') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader: data.append(row)
                f.close()
        except Exception as e:
            logger.error(f'{self} | {e} | CSV파일이 존재하지 않는다. {file}')
        else:
            logger.info(f'{self} | FilePath--> {file}')
            return self._clean(data)
    @classmethod
    def read_json(self, file):
        try:
            f = open(file, 'r', encoding='utf8')
            data = []
            for line in f:
                js = json.loads(line.strip())
                data.append(js)
        except Exception as e:
            logger.error(f'{self} | {e} | {file}')
            return []
        else:
            logger.info(f'{self} | FilePath--> {file}')
            return self._clean(data)


class FileWriter:

    @classmethod
    def write_csv(self, file, fields, data):
        self._makedir(file)
        try:
            with open(file, 'w', newline='\n', encoding='utf8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                for d in data: writer.writerow(d)
            self.State('파일쓰기완료. 파일경로-->', file)
        except Exception as e:
            logger.error(e)
            raise
    @classmethod
    def write_json(self, file, data, colseq=None):
        self._makedir(file)
        try:
            with open(file, 'w', encoding='utf8') as f:
                for d in data:
                    if colseq is None: pass
                    else: d = {c:d[c] for c in colseq if c in d}
                    js = json.dumps(d, ensure_ascii=False)
                    f.write(f'{js}\n')
                f.close()
            self.State('파일쓰기완료. 파일경로-->', file)
        except Exception as e:
            logger.error(e)
            raise
    @classmethod
    def _makedir(self, file):
        try: os.makedirs(os.path.dirname(file))
        except Exception as e: pass
    @classmethod
    @stateFunc
    def State(self, *args): pass


# ============================================================
"""파일/폴더명 중 일부 용어 변경."""
# ============================================================

rootdir = '/Users/sambong/Career/UPV/courses'

def convert_space_of_dir(rootdir, repl='-'):
    p_spc = re.compile('\s')
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for dir in dirs:
            if p_spc.search(dir) is not None:
                print(f"{'-'*60} {dir}")
                print(os.path.join(root, dir))
                newdir = dir.replace(' ',repl)
                print(os.path.join(root, newdir))
                os.rename(os.path.join(root, dir), os.path.join(root, newdir))

def convert_space_of_file(rootdir, repl='-'):
    p_spc = re.compile('\s')
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for file in files:
            m = p_spc.search(file)
            if m is not None:
                print(f"{'-'*60}\n{m}")
                print(os.path.join(root, file))
                newfile = file.replace(' ',repl)
                print(os.path.join(root, newfile))
                os.rename(os.path.join(root, file), os.path.join(root, newfile))

convert_space_of_file('/Users/sambong/pjts/iportfolio/home/static/home/images/responsive/thesis')

def convert_underbar_of_dir(rootdir, repl='__'):
    p_ubar = re.compile('[a-zA-Z0-9]_[a-zA-Z0-9]')
    p_excep = re.compile('^\.')
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for dir in dirs:
            if p_excep.search(dir) is not None:
                pass
            else:
                if p_ubar.search(dir) is not None:
                    print(f"{'-'*60} {dir}")
                    print(os.path.join(root, dir))
                    newdir = copy.copy(dir)
                    for m in p_ubar.finditer(newdir):
                        newsdirli = list(newdir)
                        newsdirli.insert(m.start()+2, '_')
                        newdir = "".join(newsdirli)
                    #newdir, num = p_ubar.subn(repl=repl, string=dir)
                    print(os.path.join(root, newdir))
                    #os.rename(os.path.join(root, dir), os.path.join(root, newdir))


def convert_words_of_dir(rootdir, words_map):
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for dir in dirs:
            for k,v in words_map.items():
                if re.search(k, dir) is not None:
                    print(f"{'-'*60} {dir}")
                    print(os.path.join(root, dir))
                    newdir, n = re.subn(pattern=k, repl=v, string=dir)
                    print(os.path.join(root, newdir))
                    os.rename(os.path.join(root, dir), os.path.join(root, newdir))
