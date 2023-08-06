from typing import List, Dict
import torch
import codefast as cf

def device() -> str:
    return 'cuda' if torch.cuda.is_available() else 'cpu'
