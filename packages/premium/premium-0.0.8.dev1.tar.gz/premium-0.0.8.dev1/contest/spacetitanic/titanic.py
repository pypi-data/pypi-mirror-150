#!/usr/bin/env python
from typing import Dict, List, Optional, Set, Tuple
import codefast as cf
import numpy as np
import pandas as pd

import premium as pm
from premium.models.benchmark import Benchmark, get_classifiers
from spacetitanic.finetune import FineTune

if __name__ == '__main__':
    ft = FineTune()
    ft.run()
