# -*- coding: utf-8 -*-
from ipylib.idebug import *
from ipylib.inumber import *
from ipylib.idatetime import *


__all__ = [
    'DtypeParser',
]

def DtypeParser(value, dtype, n_prec=4, p_prec=2):
    params = locals()
    v = value
    info1 = f'### params: {params}'
    info2 = f'### v: {v} {type(v)}'
    try:
        if v is None:
            return v
        else:
            if dtype is None:
                return v
            elif dtype in ['int','int_abs','float']:
                snp = StrNumberParser(v, n_prec)
                if snp.is_nan:
                    return None
                else:
                    if dtype == 'int': return snp.int
                    elif dtype == 'int_abs': return snp.int_abs
                    else: return snp.value
            elif dtype == 'pct':
                return Percent(v, p_prec).value
            elif dtype in ['date','time','datetime']:
                return DatetimeParser(v)
            elif dtype == 'str':
                return None if str(v) == 'nan' else str(v)
            elif dtype in ['boolean','bool']:
                return bool(v)
            elif dtype == 'list':
                if isinstance(v, list): return v
                else: raise
            elif dtype == 'dict':
                if isinstance(v, dict): return v
                else: raise
            else:
                msg = f"정의되지 않은 데이타-타입이다, 개발오류이므로 에러발생시키고 dtype을 수정해라."
                logger.error(f'{msg}-->\n{info1}\n{info2}')
                raise
    except Exception as e:
        msg = '파싱 에러가 발생하면, 개발오류이므로 에러발생시키고 dtype을 수정해라.'
        logger.error(f'{e} | {msg}-->\n{info1}\n{info2}')
        raise
