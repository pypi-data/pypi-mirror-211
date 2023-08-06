# -*- coding: utf-8 -*-
from test._testenv import *

import math

from ipylib import inumber
from ipylib import iparser
from ipylib import idatetime
from ipylib import ipath
from ipylib import ifile
from ipylib import imath


@unittest.skip("class")
class ipylib_inumber(unittest.TestCase):

    def show_property(self, o):
        SectionGubun('프로퍼티')
        print('value:', o.value)
        print('str:', o.str)
        dbg.dict(o)
        try:
            print('int:', o.int)
            print('int_abs:', o.int_abs)
        except Exception as e:
            pass

    """파싱하지 않는 입력값"""
    def test00(self):
        PartGubun('파싱하지 않는 입력값')

        snp = inumber.StrNumberParser(1000)
        self.assertTrue(snp.value == 1000)
        # self.assertEqual(snp.str, '1,000')

        snp = inumber.StrNumberParser(0.23)
        self.assertTrue(snp.value == 0.23)

        snp = inumber.StrNumberParser('')
        self.show_property(snp)
        self.assertTrue(snp.is_nan)
        self.assertEqual(snp.str, 'nan')

        snp = inumber.StrNumberParser(None)
        self.show_property(snp)
        self.assertTrue(snp.is_nan)
        self.assertEqual(snp.str, 'nan')

        snp = inumber.StrNumberParser(math.nan)
        self.show_property(snp)
        self.assertTrue(snp.is_nan)
        self.assertEqual(snp.str, 'nan')

    """파싱 대상 입력값: 양수/음수 처리"""
    def test01(self):
        PartGubun('양수/음수 처리')

        snp = inumber.StrNumberParser('--1000')
        self.assertEqual(snp.value, -1000)

        snp = inumber.StrNumberParser('++1000')
        self.assertEqual(snp.value, 1000)

        snp = inumber.StrNumberParser('1,234,567.012')
        self.assertTrue(snp.value == 1234567.012)

        snp = inumber.StrNumberParser('+1,234,567.012')
        self.assertTrue(snp.value == 1234567.012)

        snp = inumber.StrNumberParser('-1,234,567.012')
        self.assertTrue(snp.value == -1234567.012)

    """파싱 대상 입력값: Integer"""
    def test02(self):
        PartGubun('Integer')

        snp = inumber.StrNumberParser('1000000')
        self.assertTrue(snp.value == 1000000)

        # 천단위 구분법 문자형숫자 (국제표준)
        snp = inumber.StrNumberParser('1,000,000')
        self.assertTrue(snp.value == 1000000)

        # 천단위 구분법 문자형숫자 (스페인식)
        snp = inumber.StrNumberParser('1.000.000', prec=4, sosujeom=',')
        self.assertTrue(snp.value == 1000000)

    """파싱 대상 입력값: Float"""
    def test03(self):
        PartGubun('Float')

        snp = inumber.StrNumberParser('1000000.12')
        self.assertTrue(snp.value == 1000000.12)

        snp = inumber.StrNumberParser('10012.3400')
        self.assertTrue(snp.value == 10012.34)

        # 천단위 구분법 문자형숫자 (국제표준)
        snp = inumber.StrNumberParser('1,000,000.12')
        self.assertTrue(snp.value == 1000000.12)

        # 천단위 구분법 문자형숫자 (스페인식)
        snp = inumber.StrNumberParser('1.000.000,12', prec=4, sosujeom=',')
        self.assertTrue(snp.value == 1000000.12)

    """파싱 대상 입력값: 소수"""
    def test04(self):
        PartGubun('소수점이하 수')

        # 표준 소수점 표기법
        snp = inumber.StrNumberParser('0.23')
        self.assertTrue(snp.value == 0.23)

        # 스페인식 소수점 표기법
        snp = inumber.StrNumberParser('0,23', prec=4, sosujeom=',')
        self.assertTrue(snp.value == 0.23)

        # 양/음수 표기법
        snp = inumber.StrNumberParser('-0.23')
        self.assertTrue(snp.value == -0.23)

        # 앞에 '0' 없이 입력
        snp = inumber.StrNumberParser('.23')
        self.assertTrue(snp.value == 0.23)

    """파싱 대상 입력값: 퍼센트 기호 처리"""
    def test05(self):
        PartGubun('퍼센트 기호')

        snp = inumber.StrNumberParser('0.23')
        self.assertTrue(snp.value == 0.23)

        snp = inumber.StrNumberParser('0.23%')
        self.assertEqual(snp.value, 0.0023)
        self.assertTrue(snp._is_pct)

    def _dbg(self, p):
        SectionGubun('디버그')
        print('p:', p, type(p))
        dbg.dict(p)
        dbg.dict(p.parser)

        SectionGubun('프로퍼티')
        print('input:', p.input)
        print('value:', p.value)
        print('to_float:', p.to_float)
        print('to_str:', p.to_str)
    """잘못된 입력값: None"""
    # @unittest.expectedFailure
    def test10(self):
        p = inumber.Percent(None)
        self._dbg(p)
    """입력값: 문자열"""
    def test11(self):
        p = inumber.Percent('0.23%')
        self.assertEqual(p.value, 0.23)
        self._dbg(p)

        p = inumber.Percent('0.23')
        self.assertEqual(p.value, 0.23)
        self._dbg(p)
    """입력값: 숫자"""
    def test12(self):
        p = inumber.Percent(0.23)
        self.assertEqual(p.value, 0.23)
        self._dbg(p)
        self.assertEqual(p.to_str, '0.23%')
        self.assertEqual(p.to_float, 0.0023)

        p = inumber.Percent(30)
        self.assertEqual(p.value, 30.0)
        self._dbg(p)
        self.assertEqual(p.to_str, '30.00%')
        self.assertEqual(p.to_float, 0.3)


@unittest.skip("class")
class ipylib_iparser(unittest.TestCase):

    def test00(self):
        PartGubun('int')
        rv = iparser.DtypeParser('100,000', 'int')
        self.assertTrue(rv == 100000)
        self.assertTrue(isinstance(rv, int))

    def test01(self):
        PartGubun('int_abs')
        rv = iparser.DtypeParser('-100,000', 'int_abs')
        self.assertTrue(rv == 100000)
        self.assertTrue(rv > 0)
        self.assertTrue(isinstance(rv, int))

    def test02(self):
        PartGubun('float')
        rv = iparser.DtypeParser('3.14', 'float')
        self.assertTrue(rv == 3.14)
        self.assertTrue(isinstance(rv, float))

    def test03_1(self):
        PartGubun('pct')
        rv = iparser.DtypeParser('0.26%', 'pct')
        print('rv:', rv, type(rv))
        self.assertTrue(rv == 0.26)
        self.assertTrue(isinstance(rv, float))

    def test03_2(self):
        PartGubun('pct')
        rv = iparser.DtypeParser(0.0026, 'pct', p_prec=4)
        print('rv:', rv, type(rv))
        self.assertTrue(rv == 0.0026)
        self.assertTrue(isinstance(rv, float))

    def test04(self):
        PartGubun('time|date|dt|datetime')
        rv = iparser.DtypeParser('19560303', 'date')
        print('rv:', rv, type(rv), rv.tzname())
        self.assertTrue(rv.year == 1956)
        self.assertTrue(rv.month == 3)
        self.assertTrue(rv.day == 3)
        self.assertTrue(rv.tzname() == '대한민국 표준시' or rv.tzname() == 'KST')
        self.assertTrue(isinstance(rv, datetime))
        for a in ['hour','minute','second','microsecond']:
            self.assertTrue(getattr(rv, a) == 0)

    def test05(self):
        PartGubun('str')
        rv = iparser.DtypeParser('19560303', 'str')
        print('rv:', rv, type(rv))
        self.assertTrue(isinstance(rv, str))

    @unittest.expectedFailure
    def test06(self):
        PartGubun('정의되지 않은 데이타-타입')
        rv = iparser.DtypeParser(None, 'NoneType')
    @unittest.expectedFailure
    def test07(self):
        PartGubun('파싱 실패')
        rv = iparser.DtypeParser('종목명', 'float')


@unittest.skip("class")
class ipylib_idatetime(unittest.TestCase):

    def test00(self):
        PartGubun('')
        fmt = idatetime.DatetimeFormatter()
        pp.pprint(fmt)

    def test10(self):
        PartGubun('1970년부터 시작하는 날짜')
        dts = ['19700101','1970-01-01','1970/1/1']
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print(dt, type(dt), dt.timetz())
            self.assertTrue(dt.tzname() == '대한민국 표준시')
            self.assertTrue(dt.year == 1970)
            self.assertTrue(dt.month == 1)
            self.assertTrue(dt.day == 1)

    def test11(self):
        PartGubun('1970년 이전 날짜')
        dts = ['19560303','1956-03-03','1956/3/3']
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print(dt, type(dt), dt.timetz())
            self.assertTrue(dt.tzname() == '대한민국 표준시')
            self.assertTrue(dt.year == 1956)
            self.assertTrue(dt.month == 3)
            self.assertTrue(dt.day == 3)

    def test12(self):
        PartGubun('예외처리해야할 케이스')
        dts = ['00000000','0']
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print('dt:', dt, type(dt))
            self.assertTrue(dt is None)

    def test13(self):
        PartGubun('예외처리조차 벗어난 예측불가 케이스')
        dts = ['00000000T00:00:00']
        for dt in dts:
            SectionGubun(dt)
            print('dt:', dt, type(dt))
            dt = idatetime.DatetimeParser(dt)
            self.assertTrue(isinstance(dt, str))

    def test14(self):
        PartGubun('에러발생시키는 케이스: 입력값 오류')
        dts = [0000]
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print('dt:', dt, type(dt))
            self.assertTrue(isinstance(dt, int))

    def test15(self):
        PartGubun('datetime값을 입력할 경우')
        dts = [datetime(2021,8,27)]
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print('dt:', dt, type(dt))
            self.assertTrue(dt.tzname() == '대한민국 표준시')
            self.assertTrue(dt.day == 27)

    def test16(self):
        PartGubun('일시 포멧 파싱')
        dts = ['20210507153000','20210507 153000','20210507T153000']
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print(dt, type(dt), dt.timetz())
            self.assertTrue(dt.tzname() == '대한민국 표준시')
            self.assertTrue(dt.year == 2021)
            self.assertTrue(dt.month == 5)
            self.assertTrue(dt.day == 7)
            self.assertTrue(dt.hour == 15)
            self.assertTrue(dt.minute == 30)
            self.assertTrue(dt.second == 0)
            self.assertTrue(dt.microsecond == 0)

    def test20(self):
        PartGubun('시간 포멧 파싱')
        dts = ['153000','15:30:00','15:30']
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print(dt, type(dt), dt.timetz())
            self.assertTrue(dt.tzname() == '대한민국 표준시')
            self.assertTrue(dt.hour == 15)
            self.assertTrue(dt.minute == 30)
            self.assertTrue(dt.second == 0)
            self.assertTrue(dt.microsecond == 0)

    def test21(self):
        PartGubun('시간 포멧 파싱')
        dts = ['000000','00:00:00','00:00']
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print(dt)
            self.assertTrue(dt.tzname() == '대한민국 표준시')
            self.assertTrue(dt.hour == 0)
            self.assertTrue(dt.minute == 0)
            self.assertTrue(dt.second == 0)

    def test30(self):
        PartGubun('datetime을 입력할 경우')
        dt = datetime(2021,5,7,15,30)
        dts = [dt, dt.astimezone()]
        for dt in dts:
            SectionGubun(dt)
            dt = idatetime.DatetimeParser(dt)
            print(dt, type(dt), dt.timetz())
            self.assertTrue(dt.tzname() == '대한민국 표준시')
            self.assertTrue(dt.year == 2021)
            self.assertTrue(dt.month == 5)
            self.assertTrue(dt.day == 7)
            self.assertTrue(dt.hour == 15)
            self.assertTrue(dt.minute == 30)
            self.assertTrue(dt.second == 0)
            self.assertTrue(dt.microsecond == 0)

    def test31(self):
        PartGubun('datetime을 입력할 경우: today()')
        dt0 = datetime.today().astimezone()
        print(dt0, type(dt0), dt0.timetz())
        dt = idatetime.DatetimeParser(dt0)
        print(dt, type(dt), dt.timetz())
        self.assertTrue(dt.tzname() == '대한민국 표준시')
        self.assertEqual(dt0, dt)

    def test32(self):
        PartGubun('datetime을 입력할 경우: 몽고DB 에 저장된 UTC시간대')
        dt0 = datetime(1969,12,31,15,30, tzinfo=timezone.utc)
        # dt0 = datetime(1970,1,1,15,30, tzinfo=timezone.utc)
        print(dt0, type(dt0), dt0.timetz())
        dt = idatetime.DatetimeParser(dt0)
        print(dt, type(dt), dt.timetz())
        self.assertTrue(dt.tzname() == '대한민국 표준시')
        self.assertEqual(dt0, dt)


@unittest.skip("class")
class ipylib_ipath(unittest.TestCase):

    def test00(self):
        PartGubun('')
        p = ipath.clean_path('C:/pjts/ipylib')
        print('p:', p)
        self.assertTrue(p == 'C:\pjts\ipylib')


@unittest.skip("class")
class ipylib_ifile(unittest.TestCase):

    def test00(self):
        fnames = get_filenames('/Users/sambong/Downloads')
        pp.pprint(fnames)

    # def test01(self):
    #     rv = get_dirs('/Users/sambong/Interests/간재미지네')
    #     dbg.printer(rv)
    #     # rv = get_dirs('/Users/sambong/Interests/간재미지네', True)
    #     # dbg.printer(rv)
    #     # pp.pprint(rv)
    #
    # def test02(self):
    #     path = '/Users/sambong/Interests/간재미지네'
    #     rv = get_filepaths(path)
    #     dbg.printer(rv)
    #     pp.pprint(rv)
    #
    # def test03(self):
    #     path = '/Users/sambong/Downloads/ipylib-utest/test-case/fn.log'
    #     # os.makedirs(path)
    #     # os.makedirs(path)
    #     #
    #     # os.removedirs(path)
    #
    # def test04__write_file(self):
    #     path = '/Users/sambong/Downloads/ipylib-utest/test-case/fn.log'
    #     text = "Fuck off!"
    #     write_file(path, text)
    #     rv = open_file(path)
    #     dbg.printer(rv)


# @unittest.skip("class")
class ipylib_imath(unittest.TestCase):

    def setUp(self): print('\n\n')

    # @unittest.skip('특이케이스')
    def test01_1(self):
        """0 나누기 0"""
        v = imath.fraction(0, 0)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        """0 으로 나누기"""
        v = imath.fraction(1, 0)
        print(v, type(v))
        self.assertTrue(v == math.inf)

        v = imath.fraction(-1, 0)
        print(v, type(v))
        self.assertTrue(v == -math.inf)

        v = imath.fraction(math.nan, 0)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        v = imath.fraction(0, math.nan)
        print(v, type(v))
        self.assertTrue(math.isnan(v))
    # @unittest.skip('정상케이스')
    def test01_2(self):
        v = imath.fraction(1, 2)
        print(v, type(v))
        self.assertTrue(v == 0.5)

        v = imath.fraction(0, 3)
        print(v, type(v))
        self.assertTrue(v == 0)
    # @unittest.skip('특이케이스')
    def test02_1(self):
        v = imath.relchg(0, 0)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        v = imath.relchg(0, 1)
        print(v, type(v))
        self.assertTrue(v == math.inf)

        v = imath.relchg(0, -1)
        print(v, type(v))
        self.assertTrue(v == -math.inf)

        v = imath.relchg(None, -1)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        v = imath.relchg(1, None)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        v = imath.relchg(None, None)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        v = imath.relchg(math.nan, -1)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        v = imath.relchg(1, math.nan)
        print(v, type(v))
        self.assertTrue(math.isnan(v))

        v = imath.relchg(math.nan, math.nan)
        print(v, type(v))
        self.assertTrue(math.isnan(v))
    # @unittest.skip('정상케이스')
    def test02_2(self):
        """증가::양수 -> 양수"""
        r = imath.relchg(0.23, 0.34)
        print(r)
        self.assertTrue(r > 0)
        """증가::음수 -> 양수"""
        r = imath.relchg(-0.69, 0.81)
        print(r)
        self.assertTrue(r > 0)
        """증가::음수 -> 음수"""
        r = imath.relchg(-0.56, -0.23)
        print(r)
        self.assertTrue(r > 0)

        """감소::양수 -> 양수"""
        r = imath.relchg(0.81, 0.23)
        print(r)
        self.assertTrue(r < 0)
        """감소::양수 -> 음수"""
        r = imath.relchg(2.17, -0.45)
        print(r)
        self.assertTrue(r < 0)
        """감소::음수 -> 음수"""
        r = imath.relchg(-0.23, -0.57)
        print(r)
        self.assertTrue(r < 0)



if __name__ == "__main__":
    unittest.main(
        module='__main__',
        argv=None,
        testRunner=None,
        testLoader=unittest.defaultTestLoader,
        verbosity=2,
        failfast=None,
        buffer=None,
        warnings=None
    )
