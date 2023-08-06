import numpy as np
from .config import get_bmap

bmap = get_bmap()

def line2cline(sample):
  return np.vectorize(bmap.get)(sample)