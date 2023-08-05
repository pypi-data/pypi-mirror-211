import pandas as pd
from pandas_parallel_apply import GroupByParallel
import numpy as np

from pandas_parallel_apply.data_frame_parallel import DataFrameParallel

data_static = {
    "A": [1,1,2,3,5,3],
    "B": ["hello", "darkness", "hi", "dafuq", "who", "asdf"],
    1: [(1,2), (3,4), "yolo", 1, 2, 3]
}

N = 10000000
data_random = {
    "A": np.random.randint(0, 10, size=(N, )),
    "B": np.arange(N),
    "C": [chr(ord("A") + np.random.randint(0, 26)) for _ in range(N)]
}

# functions must be global, not lambdas
def global_fn(df):
    return df.iloc[0]

def test_one_col_return_series():
    df = pd.DataFrame(data_random)
    Y = df.groupby("A").apply(len)
    K = GroupByParallel(df.groupby("A"), n_cores=4, pbar=False).apply(len)
    P = DataFrameParallel(df, n_cores=4, pbar=False).groupby("A").apply(len)

    assert np.allclose(Y.values, K.values)
    assert np.allclose(Y.values, P.values)

def test_one_col_return_df():
    df = pd.DataFrame(data_random)
    Y = df.groupby("A").apply(global_fn)
    K = GroupByParallel(df.groupby("A"), n_cores=4, pbar=False).apply(global_fn)
    P = DataFrameParallel(df, n_cores=4, pbar=False).groupby("A").apply(global_fn)
    assert (Y != K).sum().sum() == 0
    assert (Y != P).sum().sum() == 0

def test_one_col_return_df_multithread():
    df = pd.DataFrame(data_random)
    Y = df.groupby("A").apply(global_fn)
    K = GroupByParallel(df.groupby("A"), n_cores=4, pbar=False, parallelism="multithread").apply(global_fn)
    P = DataFrameParallel(df, n_cores=4, pbar=False, parallelism="multithread").groupby("A").apply(global_fn)
    assert (Y != K).sum().sum() == 0
    assert (Y != P).sum().sum() == 0

def run_one_col_return_tricky_df_no_index(df):
    def f(df):
        np.random.seed(42)
        N = np.random.randint(1, len(df) + 1)
        return df.iloc[0 : N]

    df = pd.DataFrame(data_random)
    Y = df.groupby("A").apply(f)
    K = GroupByParallel(df.groupby("A"), n_cores=4, pbar=False, keep_original_indexes=False).apply(f)
    P = DataFrameParallel(df, n_cores=4, pbar=False).groupby("A").apply(f)
    assert (Y.values != K.values).sum() == 0
    assert (Y.values != P.values).sum() == 0

def run_one_col_return_tricky_df_plus_index(df):
    def f(df):
        np.random.seed(42)
        N = np.random.randint(1, len(df) + 1)
        return df.iloc[0 : N]

    df = pd.DataFrame(data_random)
    Y = df.groupby("A").apply(f)
    K = GroupByParallel(df.groupby("A"), n_cores=4, pbar=False, keep_original_indexes=True).apply(f)
    assert (Y != K).sum().sum() == 0
