import pandas as pd
from pandas_parallel_apply import DataFrameParallel
from datetime import datetime
import numpy as np

data = {
    "A": [1,2,3],
    "B": ["hello", "darkness", "hi"],
    1: [(1,2), (3,4), "yolo"]
}

data = np.random.randn(100000, 3)
df = pd.DataFrame(data, columns=["A", "B", 1])

def f(x):
    return [x["A"] + 99, x["B"], x[1]]

def test_apply_df_1():
    asdf = df.apply(f, axis=1)
    dfp = DataFrameParallel(df, n_cores=4, pbar=False)
    asdf2 = dfp.apply(f, axis=1)
    assert np.allclose(np.concatenate(asdf), np.concatenate(asdf2))
