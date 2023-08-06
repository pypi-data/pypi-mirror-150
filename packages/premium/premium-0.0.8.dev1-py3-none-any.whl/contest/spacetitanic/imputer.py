#!/usr/bin/env python
from cgitb import reset
from operator import index
import random
import re
import os
import sys
import joblib
from collections import defaultdict
from functools import reduce
import codefast as cf
from typing import List, Dict, Tuple, Set, Optional
import time
import datetime
import pandas as pd
import csv


class Row(object):
    def __init__(self, _list) -> None:
        keys = ['pid', 'home', 'cryo_sleep', 'cabin', 'dest', 'age', 'vip', 'room',
                'food', 'shopping', 'spa', 'deck', 'transported', 'first_named', 'last_name']
        for i, v in enumerate(_list):
            setattr(self, keys[i], v)

    def __repr__(self) -> str:
        return ','.join([str(getattr(self, k)) for k in self.__dict__.keys()])

    def to_list(self) -> list:
        return [getattr(self, k) for k in self.__dict__.keys()]


def fill_home():
    with open('/tmp/uniq.csv') as f:
        reader = csv.reader(f)
        rows = [Row(row) for row in reader]
        rows.sort(key=lambda e: (e.last_name, e.pid, e.home,
                                 e.cabin, e.dest))
        hit, missed = 0, 0
        for index, cur in enumerate(rows):
            cur.ppid = cur.pid.split('_')[0]
            if cur.ppid == 'PassengerId':
                cur.ppid = 'ppid'

            if cur.home == '':
                if rows[index+1].last_name == cur.last_name:
                    # print(cur, rows[index+1], sep='\n')
                    # print('-'*100)
                    hit += 1
                    cur.home = rows[index+1].home
                elif rows[index-1].last_name == cur.last_name:
                    # print(cur, rows[index-1], sep='\n')
                    # print('='*100)
                    hit += 1
                    cur.home = rows[index-1].home
                else:
                    # print(cur)
                    # print('x'*100)
                    missed += 1
        print('hit/missed: {}/{}'.format(hit, missed))
    return rows


def fill_carbin(rows):
    hit, missed = 0, 0
    rows.sort(key=lambda e: (e.last_name, e.ppid, e.home,
                             e.dest, e.cabin, e.pid, e.vip))

    def related(a, b):
        return a.ppid == b.ppid or a.last_name == b.last_name

    for index, cur in enumerate(rows):
        if cur.cabin == '':
            if related(cur, rows[index+1]):
                # print(cur, rows[index+1], sep='\n')
                # print('-'*100)
                hit += 1
                cur.cabin = rows[index+1].cabin
            elif related(cur, rows[index-1]):
                # print(cur, rows[index-1], sep='\n')
                # print('='*100)
                hit += 1
                cur.cabin = rows[index-1].cabin
            else:
                print(cur)
                print(rows[index+1])
                print('x'*100)
                missed += 1
    print('hit/missed: {}/{}'.format(hit, missed))

    return rows


def fill_dest(rows):
    hit, missed = 0, 0
    rows.sort(key=lambda e: (e.last_name, e.ppid, e.home,
                             e.cabin, e.pid, e.vip))

    def related(a, b):
        return a.ppid == b.ppid \
            or a.last_name == b.last_name \
            or (a.home == b.home and a.cabin == b.cabin)

    for index, cur in enumerate(rows):
        if cur.dest == '':
            if related(cur, rows[index+1]):
                # print(cur, rows[index+1], sep='\n')
                # print('-'*100)
                hit += 1
                cur.dest = rows[index+1].dest
            elif related(cur, rows[index-1]):
                # print(cur, rows[index-1], sep='\n')
                # print('='*100)
                hit += 1
                cur.dest = rows[index-1].dest
            else:
                print(cur)
                print(rows[index+1])
                print('x'*100)
                missed += 1
    print('dest hit/missed: {}/{}'.format(hit, missed))

    return rows


def fill_sleep(rows):
    hit, missed = 0, 0
    rows.sort(key=lambda e: (e.last_name, e.ppid, e.home,
                             e.cabin, e.dest, e.pid, e.vip))

    def related(a, b):
        return a.ppid == b.ppid \
            or a.last_name == b.last_name

    for index, cur in enumerate(rows):
        if cur.cryo_sleep == '':
            if related(cur, rows[index+1]):
                print(cur, rows[index+1], sep='\n')
                print('-'*100)
                hit += 1
                cur.cryo_sleep = rows[index+1].cryo_sleep
            elif related(cur, rows[index-1]):
                print(cur, rows[index-1], sep='\n')
                print('='*100)
                hit += 1
                cur.cryo_sleep = rows[index-1].cryo_sleep
            else:
                print(cur)
                print(rows[index+1])
                print('x'*100)
                missed += 1
    print('sleep hit/missed: {}/{}'.format(hit, missed))

    return rows


def fill_vip(rows):
    hit, missed = 0, 0
    rows.sort(key=lambda e: (e.last_name, e.ppid, e.home,
                             e.cabin, e.dest, e.pid, e.cryo_sleep))

    def related(a, b):
        return a.ppid == b.ppid \
            or a.last_name == b.last_name

    for index, cur in enumerate(rows):
        if cur.vip == '':
            if related(cur, rows[index+1]):
                print(cur, rows[index+1], sep='\n')
                print('-'*100)
                hit += 1
                cur.vip = rows[index+1].vip
            elif related(cur, rows[index-1]):
                print(cur, rows[index-1], sep='\n')
                print('='*100)
                hit += 1
                cur.vip = rows[index-1].vip
            else:
                print(cur)
                print(rows[index+1])
                print('x'*100)
                missed += 1
    print('vip hit/missed: {}/{}'.format(hit, missed))

    return rows


rows = fill_home()
rows = fill_carbin(rows)
rows = fill_dest(rows)
rows = fill_sleep(rows)
rows = fill_vip(rows)


def empty_last(s):
    return 0 if s == 'Transported' else (1 if s != '' else 2)


rows.sort(key=lambda e: (empty_last(e.transported), e.ppid))

with open('export.csv', 'w') as wf:
    writer = csv.writer(wf)
    for row in rows:
        writer.writerow(row.to_list())
