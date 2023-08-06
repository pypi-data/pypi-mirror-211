# -*- coding: utf-8 -*-
from ipylib.idebug import *



__all__ = ['BaseDataClass']


class BaseDataClass:
    # 데이타-타입 파싱은 직접한 후에, 데이타-클래스로 만들어라. 여기서 파싱 안한다.
    # @funcIdentity
    def __init__(self, datanm=None, **doc):
        self._set_name(datanm)
        self.setup(**doc)

    @property
    def dataname(self): return self.__dataclsname__
    @property
    def dict(self):
        d = self.__dict__.copy()
        del d['__dataclsname__']
        return d
    @property
    def keys(self): return list(self.dict)
    @property
    def len(self): return len(self.dict)

    def _set_name(self, datanm):
        self.__dataclsname__ = self if datanm is None else f"{self} of {datanm}"
    def build(self, **doc):
        for k,v in doc.items(): setattr(self, k, v)
    # @funcIdentity
    def setup(self, **doc):
        for k,v in doc.items(): setattr(self, k, v)
    def set(self, k, v): setattr(self, k, v)
    def unset(self, k):
        try: delattr(self, k)
        except Exception as e: logger.warning(e)
    def get(self, k):
        try: return getattr(self, k)
        except Exception as e: pass
    def get_doc(self):
        return self.dict
    def repr(self):
        print(f"\n{self.dataname}")
        pp.pprint(self.dict)
    # @funcIdentity
    def items(self): return [(k,v) for k,v in self.dict.items()]
    # @funcIdentity
    def isin(self, k): return True if k in self.dict else False

class BaseDataClassV1:
    # 데이타-타입 파싱은 직접한 후에, 데이타-클래스로 만들어라. 여기서 파싱 안한다.
    # @funcIdentity
    def __init__(self, datanm=None, **doc):
        self._set_name(datanm)
        self.setall(**doc)
    def _set_name(self, datanm):
        self.__dataclsName__ = self if datanm is None else f"{self} of {datanm}"
    @property
    def dataclsName(self): return self.__dataclsName__
    def setall(self, **doc):
        for k,v in doc.items(): setattr(self, k, v)
    def set(self, k, v): setattr(self, k, v)
    def get(self, k): return getattr(self, k)
    @property
    def keys(self): return list(self.doc)
    @property
    def dict(self):
        d = self.__dict__.copy()
        del d['__dataclsName__']
        return d
    def repr(self):
        print(f"\n{self.dataclsName}")
        pp.pprint(self.doc)
    def items(self): return [(k,v) for k,v in self.dict]
