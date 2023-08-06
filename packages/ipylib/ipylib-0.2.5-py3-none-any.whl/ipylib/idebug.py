# -*- coding: utf-8 -*-
import logging
from datetime import datetime
import os
import re
from copy import copy
import os, sys, platform
import pprint
pp = pprint.PrettyPrinter(indent=2)


__all__ = [
    'pp',

    'logger',
    'funcIdentity',
    'stateFunc',
    'ftracer',
    'ctracer',
    'ModuleGubun',
    'PartGubun',
    'SectionGubun',
    'utest',
    'loop',
    'view_dir',
    'view_dict',
    'dictValue',
    'pretty_title',
    'dbg',
    'inspect_mod',
    'inspect_cls',
    'platformInfo',
]


LogLevelDict = {
    10:'DEBUG',
    20:'INFO',
    30:'WARNING',
    40:'ERROR',
    50:'CRITICAL'
}
rLogLevelDict = {v:k for k,v in LogLevelDict.items()}



DESCRIPTION = f"""
############################################################
                    idebug 셋업상태 [{__file__}]
############################################################

사용자가 로그 레벨을 설정하지 않는다면 기본값은 'DEBUG' 이다.

원하는 로그 레벨을 설정하고 싶다면,
1. 코드상에서
os.environ['LOG_LEVEL'] = '[10/20/.../50/DEBUG/INFO/.../CRITICAL]'
2. MaxOS 터미널에서
export LOG_LEVEL=[10/20...50/DEBUG/INFO/.../CRITICAL]
3. MaxOS 터미널에서
???????????????????????????????????????????????????????

상세한 내용은 다음 내용 참조하라.
https://docs.python.org/3/library/logging.html#logging-levels
"""

try:
    LogLevel = os.environ['LOG_LEVEL']
except Exception as e:
    LogLevel = logging.DEBUG
else:
    # print(f'사용자 입력 로그 레벨: {LogLevel}')
    try:
        # 사용자 입력갑 청소
        if LogLevel.isnumeric():
            LogLevel = int(LogLevel)
        elif LogLevel.isalpha():
            LogLevel = LogLevel.upper()
            LogLevel = rLogLevelDict[LogLevel]
    except Exception as e:
        print("잘못된 로그 레벨값을 입력했다. 기본값 'DEBUG'로 자동셋업된다.", 'Exception:', e)
        LogLevel = logging.DEBUG
finally:
    print('LogLevel:', LogLevel, f'({LogLevelDict[LogLevel]})', __file__)


DefaultFormat = "%(asctime)s | %(levelname)s | [%(process)s/%(processName)s][%(thread)s/%(threadName)s]"
MainFormat = f'{DefaultFormat} | %(module)s.%(funcName)s[%(lineno)s] | %(message)s'
DecoFormat = f'{DefaultFormat} | %(message)s'
# logging.basicConfig(format=MainFormat, level=logging.DEBUG)


"""베이스 로거"""
logger = logging.getLogger('Basic')
logger.setLevel(LogLevel)
# pp.pprint(logger.__dict__)

"""스트림핸들러(터미널에 찍기) 추가"""
sh = logging.StreamHandler()
sh.setLevel(LogLevel)
formatter = logging.Formatter(MainFormat)
sh.setFormatter(formatter)
logger.addHandler(sh)

"""데코레이터 전용 로거"""
DecoLogger = logging.getLogger('Decorator')
DecoLogger.setLevel(LogLevel)
_sh = logging.StreamHandler()
_sh.setLevel(LogLevel)
_formatter = logging.Formatter(DecoFormat)
_sh.setFormatter(_formatter)
DecoLogger.addHandler(_sh)


class GubunHandler:
    def __init__(self, **kw):
        for k,v in kw.items(): setattr(self, k, v)
    def set_len(self, n):
        self.len = int(n)
    def set_simbol(self, s):
        self.simbol = str(s)
    def set_n_newline(self, n):
        self.n_newline = int(n)

class Debugger(object):

    def __init__(self):
        self.ModuleGubun = GubunHandler(name='ModuleGubun', simbol='@', n_newline=2)
        self.PartGubun = GubunHandler(name='PartGubun', simbol='=', n_newline=1)
        self.SectionGubun = GubunHandler(name='SectionGubun', simbol='-', n_newline=0)
        self.set_gubun_len(100)
        self.set_viewEnvType('print')

    @property
    def LogLevel(self): return LogLevel
    @property
    def GubunLineLen(self): return self.PartGubun.len
    @property
    def ViewEnvType(self): return self._view_env_type
    def report(self):
        print(DESCRIPTION)

        pretty_title('Debugger 클래스 셋업상태', width=60)
        txt = f"""
        LogLevel: {LogLevelDict[self.LogLevel]}({self.LogLevel})
        ViewEnvType: {self.ViewEnvType} (1: print | 2: logger | 3: jupyter)
        GubunLineLen: {self.GubunLineLen}
        """
        for line in txt.splitlines():
            if len(line.strip()) > 0: print(line.strip())

    def set_gubun_len(self, n):
        for type in ['ModuleGubun','PartGubun','SectionGubun']:
            getattr(self, type).set_len(n)
    def set_viewEnvType(self, s):
        if s == 'print': self._view_env_type = 1
        elif s == 'logger': self._view_env_type = 2
        elif s == 'jupyter': self._view_env_type = 3
        else: raise
        logger.info(f'{self} | {self._view_env_type} (1: print | 2: logger | 3: jupyter)')
    def autoset_viewEnvType(self):
        # 실행환경에 따라 자동으로 셋업한다
        pass

    def pretty_title(self, s, simbol='*', width=None):
        width = self.GubunLineLen if width is None else int(width)
        space = " " * int((width - len(s)) / 2)
        line = simbol * width
        print(f"\n{line}\n{space}{s}{space}\n{line}")

    def dict(self, obj):
        print(f"\n\n{obj.__repr__()}.__dict__")
        pp.pprint(obj.__dict__)
        # title = f"{obj.__repr__()}.__dict__"
        # contents = obj.__dict__
        # logger.debug(f'\n\n\n{title}\n{contents}')

    def dir(self, obj):
        print(f"\n\ndir({obj.__repr__()})")
        pp.pprint(dir(obj))

    def dictValue(self, loc, msg, dic):
        logger.debug(f"{loc} | {msg}")
        pp.pprint(dic)

    def attrs(self, obj):
        self.pretty_title(f'Detail Attrs Info of {obj.__repr__()}')
        for a in dir(obj):
            print(f"{'-'*self.GubunLineLen} {a}")
            v = getattr(obj, a)
            print('type:', type(v))
            print('callable:', callable(v))
            if callable(v):
                try:
                    rv = v()
                except Exception as e:
                    print("Error ->", e)
                else:
                    print('rv ->', rv, type(rv))


dbg = Debugger()


def funcIdentity(f):
    def __func(*args, **kwargs):
        msg = f"{f.__module__}.{f.__qualname__}"
        # self 제외
        _args = copy(args)[1:]
        _kwargs = kwargs.copy()
        _args = _args if len(_args) > 0 else ''
        _kwargs = _kwargs if len(_kwargs) > 0 else ''
        msg = f'{msg} | {_args}' if len(_args) > 0 else msg
        msg = f'{msg} | {_kwargs}' if len(_kwargs) > 0 else msg
        DecoLogger.debug(msg)

        return f(*args, **kwargs)
    return __func

def stateFunc(f):
    def __func(*args, **kwargs):
        msg = f"{f.__module__}.{f.__qualname__}"
        # self 제외
        _args = copy(args)[1:]
        _kwargs = kwargs.copy()
        _args = _args if len(_args) > 0 else ''
        _kwargs = _kwargs if len(_kwargs) > 0 else ''
        msg = f'{msg} | {_args}' if len(_args) > 0 else msg
        msg = f'{msg} | {_kwargs}' if len(_kwargs) > 0 else msg

        DecoLogger.info(msg)

        return f(*args, **kwargs)
    return __func


def __tracer__(type, f, *args, **kwargs):
    if type == 'func':
        _args = copy(args)
    elif type == 'class':
        # self 제외
        _args = copy(args[1:])
    _kwargs = kwargs.copy()
    _args = _args if len(_args) > 0 else ''
    _kwargs = _kwargs if len(_kwargs) > 0 else ''

    msg = f"{f.__module__}.{f.__qualname__}"
    msg = f'{msg} | {_args}' if len(_args) > 0 else msg
    msg = f'{msg} | {_kwargs}' if len(_kwargs) > 0 else msg
    return msg

"""함수 트레이서"""
def ftracer(f):
    def __ftracer__(*args, **kwargs):
        msg = __tracer__('func', f, *args, **kwargs)
        DecoLogger.info(msg)
        return f(*args, **kwargs)
    return __ftracer__

"""클래스 트레이서"""
def ctracer(f):
    def __ctracer__(*args, **kwargs):
        msg = __tracer__('class', f, *args, **kwargs)
        DecoLogger.info(msg)
        return f(*args, **kwargs)
    return __ctracer__

def GubunBase(type, msg, n_newline, simbol):
    Gubun = getattr(dbg, type)
    msg = Gubun.name if msg is None else msg
    n_newline = Gubun.n_newline if n_newline is None else n_newline
    simbol = Gubun.simbol if simbol is None else simbol

    gubunline = simbol * Gubun.len
    newlines = '\n' * n_newline
    format = f"\n{gubunline} {msg}{newlines}"
    return format

def ModuleGubun(_file_, n_newline=None, simbol=None):
    format = GubunBase('ModuleGubun', _file_, n_newline, simbol)
    if dbg.ViewEnvType == 1: print(format)
    elif dbg.ViewEnvType == 2: logger.debug(format)
    else: raise
def PartGubun(msg=None, n_newline=None, simbol=None):
    format = GubunBase('PartGubun', msg, n_newline, simbol)
    if dbg.ViewEnvType == 1: print(format)
    elif dbg.ViewEnvType == 2: logger.debug(format)
    else: raise
def SectionGubun(msg=None, n_newline=None, simbol=None):
    format = GubunBase('SectionGubun', msg, n_newline, simbol)
    if dbg.ViewEnvType == 1: print(format)
    elif dbg.ViewEnvType == 2: logger.debug(format)
    else: raise


def _convert_timeunit(seconds):
    sec = 1
    msec = sec / 1000
    min = sec * 60
    hour = min * 60

    t = seconds
    if t < sec:
        unit = 'msec'
        t = t / msec
    elif sec <= t <= min:
        unit = 'secs'
    elif min < t <= hour:
        unit = 'mins'
        t = t / min
    else:
        unit = 'hrs'
        t = t / hour

    return round(t, 1), unit


"""Python decorator 에 대한 공부가 우선이다"""
def utest(f, title=None):
    def _utest(*args, **kwargs):
        print('뭐지?')
        loc = f"{f.__module__}.{f.__qualname__}"
        if len(args) > 1: loc = f"{loc} | {list(args)[1:]}"
        if len(kwargs) > 1: loc = f"{loc} | {kwargs}"
        DecoLogger.debug(msg=loc)

        start_dt = datetime.now()
        # 데코레이터에 주어진 함수 실행
        rv = f(*args, **kwargs)
        # 함수 실행시간 측정
        secs = (datetime.now() - start_dt).total_seconds()
        timeExp, unit = _convert_timeunit(secs)

        DecoLogger.debug(msg=f"{loc} | Runtime: {timeExp} ({unit})")

        return rv
    return _utest


def loop(loc, i, _len, msg=None):
    _msg = f"{loc} {'-'*50} {i}/{_len}"
    msg = _msg if msg is None else f"{_msg} | {msg}"
    logger.debug(msg)


def view_dict(obj, loc=None):
    try:

        loc = '-'*50 if loc is None else loc
        logger.debug(f"{loc} | {obj}.__dict__:")
        pp.pprint(obj.__dict__)
    except Exception as e:
        logger.exception(e)


def view_dir(obj):
    try:
        print(f"\n\n{'-'*50} dir({obj}):")
        pp.pprint(dir(obj))
    except Exception as e:
        logger.exception(e)


def dictValue(loc, msg, dic):
    logger.debug(f"{loc} | {msg}")
    pp.pprint(dic)


def pretty_title(s, rv=False, simbol='#', width=100):

    space = " " * int((width - len(s)) / 2)
    line = simbol * width
    text = f"\n{line}\n{space}{s}{space}\n{line}"
    if rv: return text
    else: print(text)


def _inspect_obj(o, target, linelen, detail=False):
    print(f"type(object): {type(o)}")
    line = '-' * linelen
    p = re.compile('^_')
    elems = dir(o)
    if detail is False:
        elems = [e for e in elems if p.match(e) is None]

    for e in elems:
        a = getattr(o, e)
        _type = type(a)
        _callable = callable(a)
        if _callable:
            try:
                a()
            except Exception as err:
                # v = f"!!!Exception!!! {err}"
                if target == 'func_param':
                    print(line, e)
                    print('type:', _type)
                    print('callable:', _callable)
                    print('Exception -->', err)
            else:
                if target == 'func':
                    rv = a()
                    print(line, e)
                    print('type:', _type)
                    print('callable:', _callable)
                    print('rv -->', rv, type(rv))
        else:
            if target == 'var':
                print(line, e)
                print('type:', _type)
                print('callable:', _callable)
                print(f'{e} -->', a)


def inspect_mod(m, title=None, target='var', linelen=100):
    s = repr(m) if title is None else title
    dbg.pretty_title(s)
    _inspect_obj(m, target, linelen)


def inspect_cls(cls, title=None, target='func', linelen=100):
    s = repr(cls) if title is None else title
    dbg.pretty_title(s)
    _inspect_obj(cls, target, linelen)


class ObjectInspector(object):
    def __init__(self, target='method', linelen=100):
        d = locals()
        del d['self']
        for k,v in d.items():
            setattr(self, k, v)

    def view(self, obj):
        _inspect_obj(obj)


def platformInfo():
    pretty_title('플랫폼정보', width=60)
    li = ['_node', 'machine', 'node', 'platform', 'processor', 'python_branch', 'python_compiler', 'python_implementation', 'python_revision', 'python_version', 'release', 'system', 'version', 'win32_edition']
    for a in li:
        try: print({f'platform.{a}': getattr(platform, a)()})
        except Exception as e: print([__file__, a, e])

    li = ['__name__', '__package__', '_base_executable', '_framework', 'base_exec_prefix', 'base_prefix', 'byteorder', 'copyright', 'exec_prefix', 'executable', 'float_repr_style', 'platform', 'platlibdir', 'prefix', 'version', 'winver']
    for a in li:
        try: print({f'sys.{a}': getattr(sys, a)})
        except Exception as e: print([__file__, a, e])
