from pandas_parallel_apply.utils import get_n_cores
from multiprocessing import cpu_count

def test_get_n_cores():
    fake_df = [0] * (cpu_count() + 10)
    try:
        _ = get_n_cores(-100, fake_df)
        _ = get_n_cores(-2, fake_df)
    except AssertionError:
        pass

    assert get_n_cores(-1, fake_df) == cpu_count() - 1
    assert get_n_cores(0, fake_df) == 0
    assert get_n_cores(1, fake_df) == 1
    assert get_n_cores(cpu_count() + 1, fake_df) == cpu_count() + 1
    assert get_n_cores(cpu_count() + 11, fake_df) == cpu_count() + 10
