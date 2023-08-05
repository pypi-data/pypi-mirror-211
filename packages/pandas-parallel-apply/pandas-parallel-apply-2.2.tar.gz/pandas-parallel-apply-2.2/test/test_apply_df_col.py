import pandas as pd
from pandas_parallel_apply import DataFrameParallel, SeriesParallel
import numpy as np

data = np.random.randn(1000000, 3)
df = pd.DataFrame(data, columns=["A", "B", 1])

def f(x):
    return x + 99

def test_apply_df_col_1():
    asdf = df["A"].apply(f)

    dfp = DataFrameParallel(df, n_cores=4, pbar=False)
    asdf2 = dfp["A"].apply(f)
    assert np.allclose(asdf, asdf2)

    asdf4 = SeriesParallel(df["A"], n_cores=4, pbar=False).apply(f)
    assert np.allclose(asdf, asdf4)
