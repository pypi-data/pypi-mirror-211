# -*- coding: utf-8 -*-
import math

from ipylib.idebug import *

from ipylib.inumber import Percent





"""나누기"""
def fraction(ja, mo):
    # ja: numerator
    # mo: denominator
    try:
        if math.isnan(ja) or math.isnan(mo): return math.nan
        else:
            ja = float(ja)
            mo = float(mo)
            if mo == float(0):
                if ja == float(0): return math.nan
                else: return math.inf if ja > 0 else -math.inf
            else:
                return ja/mo
    except Exception as e:
        logger.error([e, locals()])

"""x1 -> x2 로 변할 때의 변화율"""
def relchg(x1, x2, prec=4):
    """
    https://en.wikipedia.org/wiki/Relative_change_and_difference
    x2 - x1
    _______
      x1
    """
    c1 = isinstance(x1, int) or isinstance(x1, float)
    c2 = isinstance(x2, int) or isinstance(x2, float)
    if c1 and c2:
        r = fraction(x2-x1, abs(x1))
        return round(r, prec)
    else:
        return math.nan

def rate(x1, x2):
    """
    rate (Rate of change) |
    https://en.wikipedia.org/wiki/Rate_(mathematics)
    f(a+h) - f(a)
    _____________
           h
    h는 주로 time 인 경우가 많다.
    An instantaneous rate of change is equivalent to a derivative.
    """
    return

def dist_ratio(xlist):
    """
    구성비『統計』 the component[distribution] ratio.
    """
    try:
        print(xlist)
        xs = 0
        for x in xlist:
            xs += x

        rpt_list= []
        for x in xlist:
            rv = fraction(x, xs)
            rpt_list.append(round(rv, 2))
        return rpt_list
    except Exception as e:
        logger.exception(f"{e} | locals(): {locals()}")

def approximate(v, bin=10):
    f, i = math.modf(v / bin)
    return int(i * bin)
