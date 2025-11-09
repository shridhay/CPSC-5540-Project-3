from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from typing import Self, Union
import numpy as np
from fractions import Fraction
from functools import reduce
import sys
import time
import copy

def and_(l):
    if len(l) == 0:
        return True
    elif len(l) == 1:
        return bool(l[0]) 
    else:   
        return bool(l[0]) and and_(l[1:])

def or_(l):
    if len(l) == 0:
        return False
    elif len(l) == 1:
        return bool(l[0])
    else:
        return bool(l[0]) or or_(l[1:])

if __name__ == "__main__":
    pass
