from study_lyte.adjustments import (get_directional_mean, get_neutral_bias_at_border, get_normalized_at_border, \
                                    merge_time_series, remove_ambient, apply_calibration,
                                    aggregate_by_depth, get_points_from_fraction, assume_no_upward_motion,
                                    convert_force_to_pressure)
import pytest
import pandas as pd
import numpy as np


@pytest.mark.parametrize("n_samples, fraction, expected", [
    (10, 0.5, 5),
    (5, 0.95, 4),
    (10, 0, 1),
    (10, 1, 9),

])
def test_get_points_from_fraction(n_samples, fraction, expected):
    idx = get_points_from_fraction(n_samples, fraction)
    assert idx == expected


@pytest.mark.parametrize('data, fractional_basis, direction, expected', [
    # Test the directionality
    ([1, 1, 2, 2], 0.5, 'forward', 1),
    ([1, 1, 2, 2], 0.5, 'backward', 2),
    #  fractional basis
    ([1, 3, 4, 6], 0.25, 'forward', 1),
    ([1, 3, 5, 6], 0.75, 'forward', 3)
])
def test_directional_mean(data, fractional_basis, direction, expected):
    """
    Test the directional mean function
    """
    df = pd.DataFrame({'data': np.array(data)})
    value = get_directional_mean(df['data'], fractional_basis=fractional_basis, direction=direction)
    assert value == expected


@pytest.mark.parametrize('data, fractional_basis, direction, zero_bias_idx', [
    # Test the directionality
    ([1, 1, 2, 2], 0.5, 'forward', 0),
    ([1, 1, 2, 2], 0.5, 'backward', -1),
])
def test_get_neutral_bias_at_border(data, fractional_basis, direction, zero_bias_idx):
    """
    Test getting neutral bias at the borders of the data, use the zero_bias_idx to assert
    where the bias of the data should be zero
    """
    df = pd.DataFrame({'data': np.array(data)})
    result = get_neutral_bias_at_border(df['data'], fractional_basis=fractional_basis, direction=direction)
    assert result.iloc[zero_bias_idx] == 0


@pytest.mark.parametrize('data, fractional_basis, direction, ideal_norm_index', [
    # Test the directionality
    ([1, 1, 2, 2], 0.5, 'forward', 0),
    ([1, 1, 2, 2], 0.5, 'backward', -1),
    ([0, 0, 2, 2], 0.5, 'backward', -1),

])
def test_get_normalized_at_border(data, fractional_basis, direction, ideal_norm_index):
    """
    Test getting a dataset normalized by its border where the border values of the data should be one
    """
    df = pd.DataFrame({'data': np.array(data)})
    result = get_normalized_at_border(df['data'], fractional_basis=fractional_basis, direction=direction)
    assert result.iloc[ideal_norm_index] == 1


@pytest.mark.parametrize('data_list, expected', [
    # Typical use, low sample to high res
    ([np.linspace(1, 4, 4), np.linspace(1, 4, 2)], 2 * [np.linspace(1, 4, 4)]),
    # No data
    ([], []),
])
def test_merge_time_series(data_list, expected):
    # build a convenient list of dataframes
    other_dfs = []
    expected_dict = {}
    for i, data in enumerate(data_list):
        name = f'data_{i}'
        # Let the number of values determine the sampling of time, always across 1 second
        ts = np.linspace(0, 1, len(data)).astype(float)
        df = pd.DataFrame({'time': ts, name: data})
        df = df.set_index('time')
        other_dfs.append(df)

        # Build the expected dictionary
        expected_dict[name] = expected[i]

    result = merge_time_series(other_dfs)
    if 'time' in result.columns:
        result = result.set_index('time')
    # Build the expected using the expected input
    expected_df = pd.DataFrame(expected_dict)

    if expected_dict:
        expected_df['time'] = np.linspace(0, 1, len(expected_dict['data_0'])).astype(float)
        expected_df = expected_df.set_index('time')

    exp_cols = expected_df.columns

    pd.testing.assert_frame_equal(result[exp_cols], expected_df, check_index_type=False)


@pytest.mark.parametrize('active, ambient, min_ambient_range, expected', [
    # Test normal situation with ambient present
    ([200, 200, 400, 1000], [200, 200, 0, 0], 100, [0, 0, 300, 1000]),
    # Test no cleaning required
    ([200, 200, 400, 400], [210, 210, 200, 200], 90, [200, 200, 400, 400])

])
def test_remove_ambient(active, ambient, min_ambient_range, expected):
    """
    Test that subtraction removes the ambient but re-scales back to the
    original values
    """
    active = pd.Series(np.array(active))
    ambient = pd.Series(np.array(ambient))
    result = remove_ambient(active, ambient, min_ambient_range=100)
    np.testing.assert_equal(result.values, expected)

@pytest.mark.parametrize('data, coefficients, expected', [
    ([1, 2, 3, 4], [2, 0], [2, 4, 6, 8])
])
def test_apply_calibration(data, coefficients, expected):
    data = np.array(data)
    expected = np.array(expected)
    result = apply_calibration(data, coefficients)
    np.testing.assert_equal(result, expected)


@pytest.mark.parametrize("data, depth, new_depth, agg_method, expected_data", [
    # Test w/ intuitive data
    # ([2, 4, 6, 8, 10, 12], [1, 2, 3, 4, 5, 6], [2, 4, 6], 'mean', [3, 7, 11]),
    # Test with negative depths
    ([[2, 4, 6, 8]], [-10, -20, -30, -40], [-20, -40], 'mean', [[3, 7]]),
    # Test with column specific agg methods
    ([[2, 4, 6, 8], [1, 1, 1, 1]], [-10, -20, -30, -40], [-20, -40], {'data0': 'mean','data1':'sum'}, [[3, 7], [2, 2]])

])
def test_aggregate_by_depth(data, depth, new_depth, agg_method, expected_data):
    """
    """
    data_dict = {f'data{i}':d for i,d in enumerate(data)}
    data_dict['depth'] = depth
    df = pd.DataFrame.from_dict(data_dict)

    exp = {'data': expected_data, 'depth': new_depth}
    exp = {f'data{i}':d for i,d in enumerate(expected_data)}
    exp['depth'] = new_depth

    expected = pd.DataFrame.from_dict(exp)
    result = aggregate_by_depth(df, new_depth, agg_method=agg_method)

    pd.testing.assert_frame_equal(result, expected, check_dtype=False)

@pytest.mark.skip('Function not ready')
@pytest.mark.parametrize('data, method, expected', [
    # Simple minor up tick to be smoothed out
    ([7, 6, 5, 4, 5, 6, 2], 'nanmean', [7, 6, 5, 5, 5, 5, 2]),
    # No uptick, check it is mostly unaffected.
    ([5, 4, 3, 2, 1], 'nanmean', [5, 4, 3, 2, 1]),
    # Double hump
    ([10, 9, 11, 8, 7, 6, 5, 4, 5, 6, 2], 'nanmean', [10, 10, 10, 8, 7, 6, 5, 5, 5, 5, 2]),
    # Replacement for original function
    ([4, 5, 2], 'nanmin', [4, 4, 2]),

])
def test_assume_no_upward_motion(data, method, expected):
    s = pd.Series(np.array(data).astype(float), index=range(0, len(data)))
    exp_s = pd.Series(np.array(expected).astype(float), index=range(0, len(expected)))
    result = assume_no_upward_motion(s, method=method)
    from study_lyte.plotting import plot_ts
    ax = plot_ts(s, alpha=0.5, show=False)
    ax = plot_ts(result,ax=ax, show=True)
    #ax = plot_ts(exp_s, ax=ax, show=True)

    pd.testing.assert_series_equal(result, exp_s)


@pytest.mark.skip('Function not ready')
@pytest.mark.parametrize('fname, column, method, expected_depth', [
    # ('hard_surface_hard_stop.csv', 'depth', 'nanmean', 83),
    # ('baro_w_bench.csv', 'filtereddepth', 'nanmedian', 44),
    # ('baro_w_tails.csv', 'filtereddepth', 'nanmean', 50),
    # ('smooth.csv', 'filtereddepth', 'nanmedian', 63),
    # ('low_zpfo_baro.csv', 'filtereddepth', 'nanmedian', 62),
    # ('lower_slow_down.csv', 'filtereddepth', 'nanmedian', 57),
    # ('rough_bench.csv', 'filtereddepth', 'nanmean', 52),
])
def test_assume_no_upward_motion_real(raw_df, fname, column, method, expected_depth):
    result = assume_no_upward_motion(raw_df[column], method=method)
    delta_d = abs(result.max() - result.min())
    from study_lyte.plotting import plot_ts
    ax = plot_ts(raw_df[column] - raw_df[column].max(), alpha=0.5, show=False)
    ax = plot_ts(result - result.max(), ax=ax, show=True)
    assert pytest.approx(delta_d, abs=3) == expected_depth


@pytest.mark.parametrize('force, tip_diameter, adj, expected', [
    ([4, 8], 0.005, 1, [203.718327, 407.436654])
])
def test_convert_force_to_pressure(force, tip_diameter, adj, expected):
    force_series = pd.Series(np.array(force).astype(float), index=range(0, len(force)))
    expected = pd.Series(np.array(expected).astype(float), index=range(0, len(expected)))
    result = convert_force_to_pressure(force_series, tip_diameter, adj)
    pd.testing.assert_series_equal(result, expected)
