from operator import methodcaller

import numpy as np
import pytest

import pandas as pd
from pandas import (
    MultiIndex,
    Series,
    date_range,
)
import pandas._testing as tm


class TestSeries:
    @pytest.mark.parametrize("func", ["rename_axis", "_set_axis_name"])
    def test_set_axis_name_mi(self, func):
        ser = Series(
            [11, 21, 31],
            index=MultiIndex.from_tuples(
                [("A", x) for x in ["a", "B", "c"]], names=["l1", "l2"]
            ),
        )

        result = methodcaller(func, ["L1", "L2"])(ser)
        assert ser.index.name is None
        assert ser.index.names == ["l1", "l2"]
        assert result.index.name is None
        assert result.index.names, ["L1", "L2"]

    def test_set_axis_name_raises(self):
        ser = Series([1])
        msg = "No axis named 1 for object type Series"
        with pytest.raises(ValueError, match=msg):
            ser._set_axis_name(name="a", axis=1)

    def test_get_bool_data_preserve_dtype(self):
        ser = Series([True, False, True])
        result = ser._get_bool_data()
        tm.assert_series_equal(result, ser)

    def test_nonzero_single_element(self):
        # allow single item via bool method
        ser = Series([True])
        assert ser.bool()

        ser = Series([False])
        assert not ser.bool()

    @pytest.mark.parametrize("data", [np.nan, pd.NaT, True, False])
    def test_nonzero_single_element_raise_1(self, data):
        # single item nan to raise
        series = Series([data])

        msg = "The truth value of a Series is ambiguous"
        with pytest.raises(ValueError, match=msg):
            bool(series)

    @pytest.mark.parametrize("data", [np.nan, pd.NaT])
    def test_nonzero_single_element_raise_2(self, data):
        series = Series([data])

        msg = "bool cannot act on a non-boolean single element Series"
        with pytest.raises(ValueError, match=msg):
            series.bool()

    @pytest.mark.parametrize("data", [(True, True), (False, False)])
    def test_nonzero_multiple_element_raise(self, data):
        # multiple bool are still an error
        series = Series([data])

        msg = "The truth value of a Series is ambiguous"
        with pytest.raises(ValueError, match=msg):
            bool(series)
        with pytest.raises(ValueError, match=msg):
            series.bool()

    @pytest.mark.parametrize("data", [1, 0, "a", 0.0])
    def test_nonbool_single_element_raise(self, data):
        # single non-bool are an error
        series = Series([data])

        msg = "The truth value of a Series is ambiguous"
        with pytest.raises(ValueError, match=msg):
            bool(series)

        msg = "bool cannot act on a non-boolean single element Series"
        with pytest.raises(ValueError, match=msg):
            series.bool()

    def test_metadata_propagation_indiv_resample(self):
        # resample
        ts = Series(
            np.random.rand(1000),
            index=date_range("20130101", periods=1000, freq="s"),
            name="foo",
        )
        result = ts.resample("1T").mean()
        tm.assert_metadata_equivalent(ts, result)

        result = ts.resample("1T").min()
        tm.assert_metadata_equivalent(ts, result)

        result = ts.resample("1T").apply(lambda x: x.sum())
        tm.assert_metadata_equivalent(ts, result)

    def test_metadata_propagation_indiv(self, monkeypatch):
        # check that the metadata matches up on the resulting ops

        ser = Series(range(3), range(3))
        ser.name = "foo"
        ser2 = Series(range(3), range(3))
        ser2.name = "bar"

        result = ser.T
        tm.assert_metadata_equivalent(ser, result)

        def finalize(self, other, method=None, **kwargs):
            for name in self._metadata:
                if method == "concat" and name == "filename":
                    value = "+".join(
                        [
                            getattr(obj, name)
                            for obj in other.objs
                            if getattr(obj, name, None)
                        ]
                    )
                    object.__setattr__(self, name, value)
                else:
                    object.__setattr__(self, name, getattr(other, name, None))

            return self

        with monkeypatch.context() as m:
            m.setattr(Series, "_metadata", ["name", "filename"])
            m.setattr(Series, "__finalize__", finalize)

            ser.filename = "foo"
            ser2.filename = "bar"

            result = pd.concat([ser, ser2])
            assert result.filename == "foo+bar"
            assert result.name is None
