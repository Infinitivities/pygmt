"""
Tests for the _to_numpy function in the clib.conversion module.
"""

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt.clib.conversion import _to_numpy


def _check_result(result, expected_dtype):
    """
    A helper function to check if the result of the _to_numpy function is a C-contiguous
    NumPy array with the expected dtype.
    """
    assert isinstance(result, np.ndarray)
    assert result.flags.c_contiguous
    assert result.dtype.type == expected_dtype


########################################################################################
# Test the _to_numpy function with Python built-in types.
########################################################################################
@pytest.mark.parametrize(
    ("data", "expected_dtype"),
    [
        pytest.param([1, 2, 3], np.int64, id="int"),
        pytest.param([1.0, 2.0, 3.0], np.float64, id="float"),
        pytest.param(
            [complex(+1), complex(-2j), complex("-Infinity+NaNj")],
            np.complex128,
            id="complex",
        ),
    ],
)
def test_to_numpy_python_types_numeric(data, expected_dtype):
    """
    Test the _to_numpy function with Python built-in numeric types.
    """
    result = _to_numpy(data)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, data)


########################################################################################
# Test the _to_numpy function with NumPy arrays.
#
# There are 24 fundamental dtypes in NumPy. Not all of them are supported by PyGMT.
#
# - Numeric dtypes:
#   - int8, int16, int32, int64, longlong
#   - uint8, uint16, uint32, uint64, ulonglong
#   - float16, float32, float64, longdouble
#   - complex64, complex128, clongdouble
# - bool
# - datetime64, timedelta64
# - str_
# - bytes_
# - object_
# - void
#
# Reference: https://numpy.org/doc/2.1/reference/arrays.scalars.html
########################################################################################
np_dtype_params = [
    pytest.param(np.int8, np.int8, id="int8"),
    pytest.param(np.int16, np.int16, id="int16"),
    pytest.param(np.int32, np.int32, id="int32"),
    pytest.param(np.int64, np.int64, id="int64"),
    pytest.param(np.longlong, np.longlong, id="longlong"),
    pytest.param(np.uint8, np.uint8, id="uint8"),
    pytest.param(np.uint16, np.uint16, id="uint16"),
    pytest.param(np.uint32, np.uint32, id="uint32"),
    pytest.param(np.uint64, np.uint64, id="uint64"),
    pytest.param(np.ulonglong, np.ulonglong, id="ulonglong"),
    pytest.param(np.float16, np.float16, id="float16"),
    pytest.param(np.float32, np.float32, id="float32"),
    pytest.param(np.float64, np.float64, id="float64"),
    pytest.param(np.longdouble, np.longdouble, id="longdouble"),
    pytest.param(np.complex64, np.complex64, id="complex64"),
    pytest.param(np.complex128, np.complex128, id="complex128"),
    pytest.param(np.clongdouble, np.clongdouble, id="clongdouble"),
]


@pytest.mark.parametrize(("dtype", "expected_dtype"), np_dtype_params)
def test_to_numpy_ndarray_numpy_dtypes_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with NumPy arrays of NumPy numeric dtypes.

    Test both 1-D and 2-D arrays which are not C-contiguous.
    """
    # 1-D array that is not C-contiguous
    array = np.array([1, 2, 3, 4, 5, 6], dtype=dtype)[::2]
    assert array.flags.c_contiguous is False
    result = _to_numpy(array)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, array, strict=True)

    # 2-D array that is not C-contiguous
    array = np.array([[1, 2, 3, 4], [5, 6, 7, 8]], dtype=dtype)[::2, ::2]
    assert array.flags.c_contiguous is False
    result = _to_numpy(array)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, array, strict=True)


########################################################################################
# Test the _to_numpy function with pandas.Series.
#
# In pandas, dtype can be specified by
#
# 1. NumPy dtypes (see above)
# 2. pandas dtypes
# 3. PyArrow dtypes
#
# pandas provides following dtypes:
#
# - Numeric dtypes:
#   - Int8, Int16, Int32, Int64
#   - UInt8, UInt16, UInt32, UInt64
#   - Float32, Float64
# - DatetimeTZDtype
# - PeriodDtype
# - IntervalDtype
# - StringDtype
# - CategoricalDtype
# - SparseDtype
# - BooleanDtype
# - ArrowDtype: a special dtype used to store data in the PyArrow format.
#
# References:
# 1. https://pandas.pydata.org/docs/reference/arrays.html
# 2. https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
# 3. https://pandas.pydata.org/docs/user_guide/pyarrow.html
########################################################################################
@pytest.mark.parametrize(("dtype", "expected_dtype"), np_dtype_params)
def test_to_numpy_pandas_series_numpy_dtypes_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with pandas.Series of NumPy numeric dtypes.
    """
    series = pd.Series([1, 2, 3, 4, 5, 6], dtype=dtype)[::2]  # Not C-contiguous
    result = _to_numpy(series)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, series)


@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param(pd.Int8Dtype(), np.int8, id="Int8"),
        pytest.param(pd.Int16Dtype(), np.int16, id="Int16"),
        pytest.param(pd.Int32Dtype(), np.int32, id="Int32"),
        pytest.param(pd.Int64Dtype(), np.int64, id="Int64"),
        pytest.param(pd.UInt8Dtype(), np.uint8, id="UInt8"),
        pytest.param(pd.UInt16Dtype(), np.uint16, id="UInt16"),
        pytest.param(pd.UInt32Dtype(), np.uint32, id="UInt32"),
        pytest.param(pd.UInt64Dtype(), np.uint64, id="UInt64"),
        pytest.param(pd.Float32Dtype(), np.float32, id="Float32"),
        pytest.param(pd.Float64Dtype(), np.float64, id="Float64"),
    ],
)
def test_to_numpy_pandas_series_pandas_dtypes_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with pandas.Series of pandas numeric dtypes.
    """
    series = pd.Series([1, 2, 3, 4, 5, 6], dtype=dtype)[::2]  # Not C-contiguous
    result = _to_numpy(series)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, series)


@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param(pd.Int8Dtype(), np.float64, id="Int8"),
        pytest.param(pd.Int16Dtype(), np.float64, id="Int16"),
        pytest.param(pd.Int32Dtype(), np.float64, id="Int32"),
        pytest.param(pd.Int64Dtype(), np.float64, id="Int64"),
        pytest.param(pd.UInt8Dtype(), np.float64, id="UInt8"),
        pytest.param(pd.UInt16Dtype(), np.float64, id="UInt16"),
        pytest.param(pd.UInt32Dtype(), np.float64, id="UInt32"),
        pytest.param(pd.UInt64Dtype(), np.float64, id="UInt64"),
        pytest.param(pd.Float32Dtype(), np.float32, id="Float32"),
        pytest.param(pd.Float64Dtype(), np.float64, id="Float64"),
    ],
)
def test_to_numpy_pandas_series_pandas_dtypes_numeric_with_na(dtype, expected_dtype):
    """
    Test the _to_numpy function with pandas.Series of pandas numeric dtypes and NA.
    """
    series = pd.Series([1, 2, pd.NA, 4, 5, 6], dtype=dtype)[::2]  # Not C-contiguous
    assert series.isna().any()
    result = _to_numpy(series)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, np.array([1.0, np.nan, 5.0], dtype=expected_dtype))