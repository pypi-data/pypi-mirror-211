# -*- coding: utf-8 -*-
import os
import sys
import subprocess


# 모든 단위테스트를 한번에 수행할 수 있는 cmd 또는 함수를 제공
if __name__ == "__main__":
    print(f"\n{'*'*50} {os.path.abspath(__file__)}\n{__doc__}")
    print(f"sys.argv : {sys.argv}")
    subprocess.run("python3 -m unittest utest/ifile.py", shell=True, check=True)
