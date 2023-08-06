#!/usr/bin/env python
import random
import re, os, sys, joblib
from collections import defaultdict
from functools import reduce
import codefast as cf
from premium import mop

results = [f for f in cf.io.walk('spacetitanic/results')]
over80 = [f for f in results if '_8' in f]
print(results)
for f in over80:
    print(cf.io.basename(f))

res = mop.hard_vote(over80)
res['Transported'] = res['Transported'].astype(bool)
print(res)
res.to_csv('hard_vote_over80.csv', index=False)
