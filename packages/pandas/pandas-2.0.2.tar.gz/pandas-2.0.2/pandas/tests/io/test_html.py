from functools import partial
from importlib import reload
from io import (
    BytesIO,
    StringIO,
)
import os
from pathlib import Path
import re
import threading
from typing import Iterator
from urllib.error import URLError

import numpy as np
import pytest

from pandas.compat import is_platform_windows
import pandas.util._test_decorators as td

import pandas as pd
from pandas import (
    NA,
    DataFrame,
    MultiIndex,
    Series,
    Timestamp,
    date_range,
    read_csv,
    to_datetime,
)
import pandas._testing as tm
from pandas.core.arrays import (
    ArrowStringArray,
    StringArray,
)

from pandas.io.common import file_path_to_url
import pandas.io.html
from pandas.io.html import read_html


@pytest.fixture(
    params=[
        "chinese_utf-16.html",
        "chinese_utf-32.html",
        "chinese_utf-8.html",
        "letz_latin1.html",
    ]
)
def html_encoding_file(request, datapath):
    """Parametrized fixture for HTML encoding test filenames."""
    return datapath("io", "data", "html_encoding", request.param)


def assert_framelist_equal(list1, list2, *args, **kwargs):
    assert len(list1) == len(list2), (
        "lists are not of equal size "
        f"len(list1) == {len(list1)}, "
        f"len(list2) == {len(list2)}"
    )
    msg = "not all list elements are DataFrames"
    both_frames = all(
        map(
            lambda x, y: isinstance(x, DataFrame) and isinstance(y, DataFrame),
            list1,
            list2,
        )
    )
    assert both_frames, msg
    for frame_i, frame_j in zip(list1, list2):
        tm.assert_frame_equal(frame_i, frame_j, *args, **kwargs)
        assert not frame_i.empty, "frames are both empty"


@td.skip_if_no("bs4")
@td.skip_if_no("html5lib")
def test_bs4_version_fails(monkeypatch, datapath):
    import bs4

    monkeypatch.setattr(bs4, "__version__", "4.2")
    with pytest.raises(ImportError, match="Pandas requires version"):
        read_html(datapath("io", "data", "html", "spam.html"), flavor="bs4")


def test_invalid_flavor():
    url = "google.com"
    flavor = "invalid flavor"
    msg = r"\{" + flavor + r"\} is not a valid set of flavors"

    with pytest.raises(ValueError, match=msg):
        read_html(url, match="google", flavor=flavor)


@td.skip_if_no("bs4")
@td.skip_if_no("lxml")
@td.skip_if_no("html5lib")
def test_same_ordering(datapath):
    filename = datapath("io", "data", "html", "valid_markup.html")
    dfs_lxml = read_html(filename, index_col=0, flavor=["lxml"])
    dfs_bs4 = read_html(filename, index_col=0, flavor=["bs4"])
    assert_framelist_equal(dfs_lxml, dfs_bs4)


@pytest.mark.parametrize(
    "flavor",
    [
        pytest.param("bs4", marks=[td.skip_if_no("bs4"), td.skip_if_no("html5lib")]),
        pytest.param("lxml", marks=td.skip_if_no("lxml")),
    ],
)
class TestReadHtml:
    @pytest.fixture
    def spam_data(self, datapath):
        return datapath("io", "data", "html", "spam.html")

    @pytest.fixture
    def banklist_data(self, datapath):
        return datapath("io", "data", "html", "banklist.html")

    @pytest.fixture(autouse=True)
    def set_defaults(self, flavor):
        self.read_html = partial(read_html, flavor=flavor)
        yield

    def test_to_html_compat(self):
        df = (
            tm.makeCustomDataframe(
                4,
                3,
                data_gen_f=lambda *args: np.random.rand(),
                c_idx_names=False,
                r_idx_names=False,
            )
            # pylint: disable-next=consider-using-f-string
            .applymap("{:.3f}".format).astype(float)
        )
        out = df.to_html()
        res = self.read_html(out, attrs={"class": "dataframe"}, index_col=0)[0]
        tm.assert_frame_equal(res, df)

    def test_dtype_backend(self, string_storage, dtype_backend):
        # GH#50286
        df = DataFrame(
            {
                "a": Series([1, np.nan, 3], dtype="Int64"),
                "b": Series([1, 2, 3], dtype="Int64"),
                "c": Series([1.5, np.nan, 2.5], dtype="Float64"),
                "d": Series([1.5, 2.0, 2.5], dtype="Float64"),
                "e": [True, False, None],
                "f": [True, False, True],
                "g": ["a", "b", "c"],
                "h": ["a", "b", None],
            }
        )

        if string_storage == "python":
            string_array = StringArray(np.array(["a", "b", "c"], dtype=np.object_))
            string_array_na = StringArray(np.array(["a", "b", NA], dtype=np.object_))

        else:
            pa = pytest.importorskip("pyarrow")
            string_array = ArrowStringArray(pa.array(["a", "b", "c"]))
            string_array_na = ArrowStringArray(pa.array(["a", "b", None]))

        out = df.to_html(index=False)
        with pd.option_context("mode.string_storage", string_storage):
            result = self.read_html(out, dtype_backend=dtype_backend)[0]

        expected = DataFrame(
            {
                "a": Series([1, np.nan, 3], dtype="Int64"),
                "b": Series([1, 2, 3], dtype="Int64"),
                "c": Series([1.5, np.nan, 2.5], dtype="Float64"),
                "d": Series([1.5, 2.0, 2.5], dtype="Float64"),
                "e": Series([True, False, NA], dtype="boolean"),
                "f": Series([True, False, True], dtype="boolean"),
                "g": string_array,
                "h": string_array_na,
            }
        )

        if dtype_backend == "pyarrow":
            import pyarrow as pa

            from pandas.arrays import ArrowExtensionArray

            expected = DataFrame(
                {
                    col: ArrowExtensionArray(pa.array(expected[col], from_pandas=True))
                    for col in expected.columns
                }
            )

        tm.assert_frame_equal(result, expected)

    @pytest.mark.network
    @tm.network(
        url=(
            "https://www.fdic.gov/resources/resolutions/"
            "bank-failures/failed-bank-list/index.html"
        ),
        check_before_test=True,
    )
    def test_banklist_url(self):
        url = "https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/index.html"  # noqa E501
        df1 = self.read_html(
            # lxml cannot find attrs leave out for now
            url,
            match="First Federal Bank of Florida",  # attrs={"class": "dataTable"}
        )
        # lxml cannot find attrs leave out for now
        df2 = self.read_html(
            url,
            match="Metcalf Bank",
        )  # attrs={"class": "dataTable"})

        assert_framelist_equal(df1, df2)

    @pytest.mark.network
    @tm.network(
        url=(
            "https://raw.githubusercontent.com/pandas-dev/pandas/main/"
            "pandas/tests/io/data/html/spam.html"
        ),
        check_before_test=True,
    )
    def test_spam_url(self):
        url = (
            "https://raw.githubusercontent.com/pandas-dev/pandas/main/"
            "pandas/tests/io/data/html/spam.html"
        )
        df1 = self.read_html(url, match=".*Water.*")
        df2 = self.read_html(url, match="Unit")

        assert_framelist_equal(df1, df2)

    @pytest.mark.slow
    def test_banklist(self, banklist_data):
        df1 = self.read_html(banklist_data, match=".*Florida.*", attrs={"id": "table"})
        df2 = self.read_html(banklist_data, match="Metcalf Bank", attrs={"id": "table"})

        assert_framelist_equal(df1, df2)

    def test_spam(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*")
        df2 = self.read_html(spam_data, match="Unit")
        assert_framelist_equal(df1, df2)

        assert df1[0].iloc[0, 0] == "Proximates"
        assert df1[0].columns[0] == "Nutrient"

    def test_spam_no_match(self, spam_data):
        dfs = self.read_html(spam_data)
        for df in dfs:
            assert isinstance(df, DataFrame)

    def test_banklist_no_match(self, banklist_data):
        dfs = self.read_html(banklist_data, attrs={"id": "table"})
        for df in dfs:
            assert isinstance(df, DataFrame)

    def test_spam_header(self, spam_data):
        df = self.read_html(spam_data, match=".*Water.*", header=2)[0]
        assert df.columns[0] == "Proximates"
        assert not df.empty

    def test_skiprows_int(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows=1)
        df2 = self.read_html(spam_data, match="Unit", skiprows=1)

        assert_framelist_equal(df1, df2)

    def test_skiprows_range(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows=range(2))
        df2 = self.read_html(spam_data, match="Unit", skiprows=range(2))

        assert_framelist_equal(df1, df2)

    def test_skiprows_list(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows=[1, 2])
        df2 = self.read_html(spam_data, match="Unit", skiprows=[2, 1])

        assert_framelist_equal(df1, df2)

    def test_skiprows_set(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows={1, 2})
        df2 = self.read_html(spam_data, match="Unit", skiprows={2, 1})

        assert_framelist_equal(df1, df2)

    def test_skiprows_slice(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows=1)
        df2 = self.read_html(spam_data, match="Unit", skiprows=1)

        assert_framelist_equal(df1, df2)

    def test_skiprows_slice_short(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows=slice(2))
        df2 = self.read_html(spam_data, match="Unit", skiprows=slice(2))

        assert_framelist_equal(df1, df2)

    def test_skiprows_slice_long(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows=slice(2, 5))
        df2 = self.read_html(spam_data, match="Unit", skiprows=slice(4, 1, -1))

        assert_framelist_equal(df1, df2)

    def test_skiprows_ndarray(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", skiprows=np.arange(2))
        df2 = self.read_html(spam_data, match="Unit", skiprows=np.arange(2))

        assert_framelist_equal(df1, df2)

    def test_skiprows_invalid(self, spam_data):
        with pytest.raises(TypeError, match=("is not a valid type for skipping rows")):
            self.read_html(spam_data, match=".*Water.*", skiprows="asdf")

    def test_index(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", index_col=0)
        df2 = self.read_html(spam_data, match="Unit", index_col=0)
        assert_framelist_equal(df1, df2)

    def test_header_and_index_no_types(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", header=1, index_col=0)
        df2 = self.read_html(spam_data, match="Unit", header=1, index_col=0)
        assert_framelist_equal(df1, df2)

    def test_header_and_index_with_types(self, spam_data):
        df1 = self.read_html(spam_data, match=".*Water.*", header=1, index_col=0)
        df2 = self.read_html(spam_data, match="Unit", header=1, index_col=0)
        assert_framelist_equal(df1, df2)

    def test_infer_types(self, spam_data):
        # 10892 infer_types removed
        df1 = self.read_html(spam_data, match=".*Water.*", index_col=0)
        df2 = self.read_html(spam_data, match="Unit", index_col=0)
        assert_framelist_equal(df1, df2)

    def test_string_io(self, spam_data):
        with open(spam_data, encoding="UTF-8") as f:
            data1 = StringIO(f.read())

        with open(spam_data, encoding="UTF-8") as f:
            data2 = StringIO(f.read())

        df1 = self.read_html(data1, match=".*Water.*")
        df2 = self.read_html(data2, match="Unit")
        assert_framelist_equal(df1, df2)

    def test_string(self, spam_data):
        with open(spam_data, encoding="UTF-8") as f:
            data = f.read()

        df1 = self.read_html(data, match=".*Water.*")
        df2 = self.read_html(data, match="Unit")

        assert_framelist_equal(df1, df2)

    def test_file_like(self, spam_data):
        with open(spam_data, encoding="UTF-8") as f:
            df1 = self.read_html(f, match=".*Water.*")

        with open(spam_data, encoding="UTF-8") as f:
            df2 = self.read_html(f, match="Unit")

        assert_framelist_equal(df1, df2)

    @pytest.mark.network
    @tm.network
    def test_bad_url_protocol(self):
        with pytest.raises(URLError, match="urlopen error unknown url type: git"):
            self.read_html("git://github.com", match=".*Water.*")

    @pytest.mark.slow
    @pytest.mark.network
    @tm.network
    def test_invalid_url(self):
        msg = (
            "Name or service not known|Temporary failure in name resolution|"
            "No tables found"
        )
        with pytest.raises((URLError, ValueError), match=msg):
            self.read_html("http://www.a23950sdfa908sd.com", match=".*Water.*")

    @pytest.mark.slow
    def test_file_url(self, banklist_data):
        url = banklist_data
        dfs = self.read_html(
            file_path_to_url(os.path.abspath(url)), match="First", attrs={"id": "table"}
        )
        assert isinstance(dfs, list)
        for df in dfs:
            assert isinstance(df, DataFrame)

    @pytest.mark.slow
    def test_invalid_table_attrs(self, banklist_data):
        url = banklist_data
        with pytest.raises(ValueError, match="No tables found"):
            self.read_html(
                url, match="First Federal Bank of Florida", attrs={"id": "tasdfable"}
            )

    def _bank_data(self, path, **kwargs):
        return self.read_html(path, match="Metcalf", attrs={"id": "table"}, **kwargs)

    @pytest.mark.slow
    def test_multiindex_header(self, banklist_data):
        df = self._bank_data(banklist_data, header=[0, 1])[0]
        assert isinstance(df.columns, MultiIndex)

    @pytest.mark.slow
    def test_multiindex_index(self, banklist_data):
        df = self._bank_data(banklist_data, index_col=[0, 1])[0]
        assert isinstance(df.index, MultiIndex)

    @pytest.mark.slow
    def test_multiindex_header_index(self, banklist_data):
        df = self._bank_data(banklist_data, header=[0, 1], index_col=[0, 1])[0]
        assert isinstance(df.columns, MultiIndex)
        assert isinstance(df.index, MultiIndex)

    @pytest.mark.slow
    def test_multiindex_header_skiprows_tuples(self, banklist_data):
        df = self._bank_data(banklist_data, header=[0, 1], skiprows=1)[0]
        assert isinstance(df.columns, MultiIndex)

    @pytest.mark.slow
    def test_multiindex_header_skiprows(self, banklist_data):
        df = self._bank_data(banklist_data, header=[0, 1], skiprows=1)[0]
        assert isinstance(df.columns, MultiIndex)

    @pytest.mark.slow
    def test_multiindex_header_index_skiprows(self, banklist_data):
        df = self._bank_data(
            banklist_data, header=[0, 1], index_col=[0, 1], skiprows=1
        )[0]
        assert isinstance(df.index, MultiIndex)
        assert isinstance(df.columns, MultiIndex)

    @pytest.mark.slow
    def test_regex_idempotency(self, banklist_data):
        url = banklist_data
        dfs = self.read_html(
            file_path_to_url(os.path.abspath(url)),
            match=re.compile(re.compile("Florida")),
            attrs={"id": "table"},
        )
        assert isinstance(dfs, list)
        for df in dfs:
            assert isinstance(df, DataFrame)

    def test_negative_skiprows(self, spam_data):
        msg = r"\(you passed a negative value\)"
        with pytest.raises(ValueError, match=msg):
            self.read_html(spam_data, match="Water", skiprows=-1)

    @pytest.mark.network
    @tm.network(url="https://docs.python.org/2/", check_before_test=True)
    def test_multiple_matches(self):
        url = "https://docs.python.org/2/"
        dfs = self.read_html(url, match="Python")
        assert len(dfs) > 1

    @pytest.mark.network
    @tm.network(url="https://docs.python.org/2/", check_before_test=True)
    def test_python_docs_table(self):
        url = "https://docs.python.org/2/"
        dfs = self.read_html(url, match="Python")
        zz = [df.iloc[0, 0][0:4] for df in dfs]
        assert sorted(zz) == sorted(["Repo", "What"])

    def test_empty_tables(self):
        """
        Make sure that read_html ignores empty tables.
        """
        html = """
            <table>
                <thead>
                    <tr>
                        <th>A</th>
                        <th>B</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>2</td>
                    </tr>
                </tbody>
            </table>
            <table>
                <tbody>
                </tbody>
            </table>
        """
        result = self.read_html(html)
        assert len(result) == 1

    def test_multiple_tbody(self):
        # GH-20690
        # Read all tbody tags within a single table.
        result = self.read_html(
            """<table>
            <thead>
                <tr>
                    <th>A</th>
                    <th>B</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>2</td>
                </tr>
            </tbody>
            <tbody>
                <tr>
                    <td>3</td>
                    <td>4</td>
                </tr>
            </tbody>
        </table>"""
        )[0]

        expected = DataFrame(data=[[1, 2], [3, 4]], columns=["A", "B"])

        tm.assert_frame_equal(result, expected)

    def test_header_and_one_column(self):
        """
        Don't fail with bs4 when there is a header and only one column
        as described in issue #9178
        """
        result = self.read_html(
            """<table>
                <thead>
                    <tr>
                        <th>Header</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>first</td>
                    </tr>
                </tbody>
            </table>"""
        )[0]

        expected = DataFrame(data={"Header": "first"}, index=[0])

        tm.assert_frame_equal(result, expected)

    def test_thead_without_tr(self):
        """
        Ensure parser adds <tr> within <thead> on malformed HTML.
        """
        result = self.read_html(
            """<table>
            <thead>
                <tr>
                    <th>Country</th>
                    <th>Municipality</th>
                    <th>Year</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Ukraine</td>
                    <th>Odessa</th>
                    <td>1944</td>
                </tr>
            </tbody>
        </table>"""
        )[0]

        expected = DataFrame(
            data=[["Ukraine", "Odessa", 1944]],
            columns=["Country", "Municipality", "Year"],
        )

        tm.assert_frame_equal(result, expected)

    def test_tfoot_read(self):
        """
        Make sure that read_html reads tfoot, containing td or th.
        Ignores empty tfoot
        """
        data_template = """<table>
            <thead>
                <tr>
                    <th>A</th>
                    <th>B</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>bodyA</td>
                    <td>bodyB</td>
                </tr>
            </tbody>
            <tfoot>
                {footer}
            </tfoot>
        </table>"""

        expected1 = DataFrame(data=[["bodyA", "bodyB"]], columns=["A", "B"])

        expected2 = DataFrame(
            data=[["bodyA", "bodyB"], ["footA", "footB"]], columns=["A", "B"]
        )

        data1 = data_template.format(footer="")
        data2 = data_template.format(footer="<tr><td>footA</td><th>footB</th></tr>")

        result1 = self.read_html(data1)[0]
        result2 = self.read_html(data2)[0]

        tm.assert_frame_equal(result1, expected1)
        tm.assert_frame_equal(result2, expected2)

    def test_parse_header_of_non_string_column(self):
        # GH5048: if header is specified explicitly, an int column should be
        # parsed as int while its header is parsed as str
        result = self.read_html(
            """
            <table>
                <tr>
                    <td>S</td>
                    <td>I</td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>1944</td>
                </tr>
            </table>
        """,
            header=0,
        )[0]

        expected = DataFrame([["text", 1944]], columns=("S", "I"))

        tm.assert_frame_equal(result, expected)

    @pytest.mark.slow
    def test_banklist_header(self, banklist_data, datapath):
        from pandas.io.html import _remove_whitespace

        def try_remove_ws(x):
            try:
                return _remove_whitespace(x)
            except AttributeError:
                return x

        df = self.read_html(banklist_data, match="Metcalf", attrs={"id": "table"})[0]
        ground_truth = read_csv(
            datapath("io", "data", "csv", "banklist.csv"),
            converters={"Updated Date": Timestamp, "Closing Date": Timestamp},
        )
        assert df.shape == ground_truth.shape
        old = [
            "First Vietnamese American Bank In Vietnamese",
            "Westernbank Puerto Rico En Espanol",
            "R-G Premier Bank of Puerto Rico En Espanol",
            "Eurobank En Espanol",
            "Sanderson State Bank En Espanol",
            "Washington Mutual Bank (Including its subsidiary Washington "
            "Mutual Bank FSB)",
            "Silver State Bank En Espanol",
            "AmTrade International Bank En Espanol",
            "Hamilton Bank, NA En Espanol",
            "The Citizens Savings Bank Pioneer Community Bank, Inc.",
        ]
        new = [
            "First Vietnamese American Bank",
            "Westernbank Puerto Rico",
            "R-G Premier Bank of Puerto Rico",
            "Eurobank",
            "Sanderson State Bank",
            "Washington Mutual Bank",
            "Silver State Bank",
            "AmTrade International Bank",
            "Hamilton Bank, NA",
            "The Citizens Savings Bank",
        ]
        dfnew = df.applymap(try_remove_ws).replace(old, new)
        gtnew = ground_truth.applymap(try_remove_ws)
        converted = dfnew
        date_cols = ["Closing Date", "Updated Date"]
        converted[date_cols] = converted[date_cols].apply(to_datetime)
        tm.assert_frame_equal(converted, gtnew)

    @pytest.mark.slow
    def test_gold_canyon(self, banklist_data):
        gc = "Gold Canyon"
        with open(banklist_data) as f:
            raw_text = f.read()

        assert gc in raw_text
        df = self.read_html(banklist_data, match="Gold Canyon", attrs={"id": "table"})[
            0
        ]
        assert gc in df.to_string()

    def test_different_number_of_cols(self):
        expected = self.read_html(
            """<table>
                        <thead>
                            <tr style="text-align: right;">
                            <th></th>
                            <th>C_l0_g0</th>
                            <th>C_l0_g1</th>
                            <th>C_l0_g2</th>
                            <th>C_l0_g3</th>
                            <th>C_l0_g4</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <th>R_l0_g0</th>
                            <td> 0.763</td>
                            <td> 0.233</td>
                            <td> nan</td>
                            <td> nan</td>
                            <td> nan</td>
                            </tr>
                            <tr>
                            <th>R_l0_g1</th>
                            <td> 0.244</td>
                            <td> 0.285</td>
                            <td> 0.392</td>
                            <td> 0.137</td>
                            <td> 0.222</td>
                            </tr>
                        </tbody>
                    </table>""",
            index_col=0,
        )[0]

        result = self.read_html(
            """<table>
                    <thead>
                        <tr style="text-align: right;">
                        <th></th>
                        <th>C_l0_g0</th>
                        <th>C_l0_g1</th>
                        <th>C_l0_g2</th>
                        <th>C_l0_g3</th>
                        <th>C_l0_g4</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                        <th>R_l0_g0</th>
                        <td> 0.763</td>
                        <td> 0.233</td>
                        </tr>
                        <tr>
                        <th>R_l0_g1</th>
                        <td> 0.244</td>
                        <td> 0.285</td>
                        <td> 0.392</td>
                        <td> 0.137</td>
                        <td> 0.222</td>
                        </tr>
                    </tbody>
                 </table>""",
            index_col=0,
        )[0]

        tm.assert_frame_equal(result, expected)

    def test_colspan_rowspan_1(self):
        # GH17054
        result = self.read_html(
            """
            <table>
                <tr>
                    <th>A</th>
                    <th colspan="1">B</th>
                    <th rowspan="1">C</th>
                </tr>
                <tr>
                    <td>a</td>
                    <td>b</td>
                    <td>c</td>
                </tr>
            </table>
        """
        )[0]

        expected = DataFrame([["a", "b", "c"]], columns=["A", "B", "C"])

        tm.assert_frame_equal(result, expected)

    def test_colspan_rowspan_copy_values(self):
        # GH17054

        # In ASCII, with lowercase letters being copies:
        #
        # X x Y Z W
        # A B b z C

        result = self.read_html(
            """
            <table>
                <tr>
                    <td colspan="2">X</td>
                    <td>Y</td>
                    <td rowspan="2">Z</td>
                    <td>W</td>
                </tr>
                <tr>
                    <td>A</td>
                    <td colspan="2">B</td>
                    <td>C</td>
                </tr>
            </table>
        """,
            header=0,
        )[0]

        expected = DataFrame(
            data=[["A", "B", "B", "Z", "C"]], columns=["X", "X.1", "Y", "Z", "W"]
        )

        tm.assert_frame_equal(result, expected)

    def test_colspan_rowspan_both_not_1(self):
        # GH17054

        # In ASCII, with lowercase letters being copies:
        #
        # A B b b C
        # a b b b D

        result = self.read_html(
            """
            <table>
                <tr>
                    <td rowspan="2">A</td>
                    <td rowspan="2" colspan="3">B</td>
                    <td>C</td>
                </tr>
                <tr>
                    <td>D</td>
                </tr>
            </table>
        """,
            header=0,
        )[0]

        expected = DataFrame(
            data=[["A", "B", "B", "B", "D"]], columns=["A", "B", "B.1", "B.2", "C"]
        )

        tm.assert_frame_equal(result, expected)

    def test_rowspan_at_end_of_row(self):
        # GH17054

        # In ASCII, with lowercase letters being copies:
        #
        # A B
        # C b

        result = self.read_html(
            """
            <table>
                <tr>
                    <td>A</td>
                    <td rowspan="2">B</td>
                </tr>
                <tr>
                    <td>C</td>
                </tr>
            </table>
        """,
            header=0,
        )[0]

        expected = DataFrame(data=[["C", "B"]], columns=["A", "B"])

        tm.assert_frame_equal(result, expected)

    def test_rowspan_only_rows(self):
        # GH17054

        result = self.read_html(
            """
            <table>
                <tr>
                    <td rowspan="3">A</td>
                    <td rowspan="3">B</td>
                </tr>
            </table>
        """,
            header=0,
        )[0]

        expected = DataFrame(data=[["A", "B"], ["A", "B"]], columns=["A", "B"])

        tm.assert_frame_equal(result, expected)

    def test_header_inferred_from_rows_with_only_th(self):
        # GH17054
        result = self.read_html(
            """
            <table>
                <tr>
                    <th>A</th>
                    <th>B</th>
                </tr>
                <tr>
                    <th>a</th>
                    <th>b</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>2</td>
                </tr>
            </table>
        """
        )[0]

        columns = MultiIndex(levels=[["A", "B"], ["a", "b"]], codes=[[0, 1], [0, 1]])
        expected = DataFrame(data=[[1, 2]], columns=columns)

        tm.assert_frame_equal(result, expected)

    def test_parse_dates_list(self):
        df = DataFrame({"date": date_range("1/1/2001", periods=10)})
        expected = df.to_html()
        res = self.read_html(expected, parse_dates=[1], index_col=0)
        tm.assert_frame_equal(df, res[0])
        res = self.read_html(expected, parse_dates=["date"], index_col=0)
        tm.assert_frame_equal(df, res[0])

    def test_parse_dates_combine(self):
        raw_dates = Series(date_range("1/1/2001", periods=10))
        df = DataFrame(
            {
                "date": raw_dates.map(lambda x: str(x.date())),
                "time": raw_dates.map(lambda x: str(x.time())),
            }
        )
        res = self.read_html(
            df.to_html(), parse_dates={"datetime": [1, 2]}, index_col=1
        )
        newdf = DataFrame({"datetime": raw_dates})
        tm.assert_frame_equal(newdf, res[0])

    def test_wikipedia_states_table(self, datapath):
        data = datapath("io", "data", "html", "wikipedia_states.html")
        assert os.path.isfile(data), f"{repr(data)} is not a file"
        assert os.path.getsize(data), f"{repr(data)} is an empty file"
        result = self.read_html(data, match="Arizona", header=1)[0]
        assert result.shape == (60, 12)
        assert "Unnamed" in result.columns[-1]
        assert result["sq mi"].dtype == np.dtype("float64")
        assert np.allclose(result.loc[0, "sq mi"], 665384.04)

    def test_wikipedia_states_multiindex(self, datapath):
        data = datapath("io", "data", "html", "wikipedia_states.html")
        result = self.read_html(data, match="Arizona", index_col=0)[0]
        assert result.shape == (60, 11)
        assert "Unnamed" in result.columns[-1][1]
        assert result.columns.nlevels == 2
        assert np.allclose(result.loc["Alaska", ("Total area[2]", "sq mi")], 665384.04)

    def test_parser_error_on_empty_header_row(self):
        result = self.read_html(
            """
                <table>
                    <thead>
                        <tr><th></th><th></tr>
                        <tr><th>A</th><th>B</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>a</td><td>b</td></tr>
                    </tbody>
                </table>
            """,
            header=[0, 1],
        )
        expected = DataFrame(
            [["a", "b"]],
            columns=MultiIndex.from_tuples(
                [("Unnamed: 0_level_0", "A"), ("Unnamed: 1_level_0", "B")]
            ),
        )
        tm.assert_frame_equal(result[0], expected)

    def test_decimal_rows(self):
        # GH 12907
        result = self.read_html(
            """<html>
            <body>
             <table>
                <thead>
                    <tr>
                        <th>Header</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1100#101</td>
                    </tr>
                </tbody>
            </table>
            </body>
        </html>""",
            decimal="#",
        )[0]

        expected = DataFrame(data={"Header": 1100.101}, index=[0])

        assert result["Header"].dtype == np.dtype("float64")
        tm.assert_frame_equal(result, expected)

    @pytest.mark.parametrize("arg", [True, False])
    def test_bool_header_arg(self, spam_data, arg):
        # GH 6114
        msg = re.escape(
            "Passing a bool to header is invalid. Use header=None for no header or "
            "header=int or list-like of ints to specify the row(s) making up the "
            "column names"
        )
        with pytest.raises(TypeError, match=msg):
            self.read_html(spam_data, header=arg)

    def test_converters(self):
        # GH 13461
        result = self.read_html(
            """<table>
                 <thead>
                   <tr>
                     <th>a</th>
                    </tr>
                 </thead>
                 <tbody>
                   <tr>
                     <td> 0.763</td>
                   </tr>
                   <tr>
                     <td> 0.244</td>
                   </tr>
                 </tbody>
               </table>""",
            converters={"a": str},
        )[0]

        expected = DataFrame({"a": ["0.763", "0.244"]})

        tm.assert_frame_equal(result, expected)

    def test_na_values(self):
        # GH 13461
        result = self.read_html(
            """<table>
                 <thead>
                   <tr>
                     <th>a</th>
                   </tr>
                 </thead>
                 <tbody>
                   <tr>
                     <td> 0.763</td>
                   </tr>
                   <tr>
                     <td> 0.244</td>
                   </tr>
                 </tbody>
               </table>""",
            na_values=[0.244],
        )[0]

        expected = DataFrame({"a": [0.763, np.nan]})

        tm.assert_frame_equal(result, expected)

    def test_keep_default_na(self):
        html_data = """<table>
                        <thead>
                            <tr>
                            <th>a</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td> N/A</td>
                            </tr>
                            <tr>
                            <td> NA</td>
                            </tr>
                        </tbody>
                    </table>"""

        expected_df = DataFrame({"a": ["N/A", "NA"]})
        html_df = self.read_html(html_data, keep_default_na=False)[0]
        tm.assert_frame_equal(expected_df, html_df)

        expected_df = DataFrame({"a": [np.nan, np.nan]})
        html_df = self.read_html(html_data, keep_default_na=True)[0]
        tm.assert_frame_equal(expected_df, html_df)

    def test_preserve_empty_rows(self):
        result = self.read_html(
            """
            <table>
                <tr>
                    <th>A</th>
                    <th>B</th>
                </tr>
                <tr>
                    <td>a</td>
                    <td>b</td>
                </tr>
                <tr>
                    <td></td>
                    <td></td>
                </tr>
            </table>
        """
        )[0]

        expected = DataFrame(data=[["a", "b"], [np.nan, np.nan]], columns=["A", "B"])

        tm.assert_frame_equal(result, expected)

    def test_ignore_empty_rows_when_inferring_header(self):
        result = self.read_html(
            """
            <table>
                <thead>
                    <tr><th></th><th></tr>
                    <tr><th>A</th><th>B</th></tr>
                    <tr><th>a</th><th>b</th></tr>
                </thead>
                <tbody>
                    <tr><td>1</td><td>2</td></tr>
                </tbody>
            </table>
        """
        )[0]

        columns = MultiIndex(levels=[["A", "B"], ["a", "b"]], codes=[[0, 1], [0, 1]])
        expected = DataFrame(data=[[1, 2]], columns=columns)

        tm.assert_frame_equal(result, expected)

    def test_multiple_header_rows(self):
        # Issue #13434
        expected_df = DataFrame(
            data=[("Hillary", 68, "D"), ("Bernie", 74, "D"), ("Donald", 69, "R")]
        )
        expected_df.columns = [
            ["Unnamed: 0_level_0", "Age", "Party"],
            ["Name", "Unnamed: 1_level_1", "Unnamed: 2_level_1"],
        ]
        html = expected_df.to_html(index=False)
        html_df = self.read_html(html)[0]
        tm.assert_frame_equal(expected_df, html_df)

    def test_works_on_valid_markup(self, datapath):
        filename = datapath("io", "data", "html", "valid_markup.html")
        dfs = self.read_html(filename, index_col=0)
        assert isinstance(dfs, list)
        assert isinstance(dfs[0], DataFrame)

    @pytest.mark.slow
    def test_fallback_success(self, datapath):
        banklist_data = datapath("io", "data", "html", "banklist.html")

        self.read_html(banklist_data, match=".*Water.*", flavor=["lxml", "html5lib"])

    def test_to_html_timestamp(self):
        rng = date_range("2000-01-01", periods=10)
        df = DataFrame(np.random.randn(10, 4), index=rng)

        result = df.to_html()
        assert "2000-01-01" in result

    def test_to_html_borderless(self):
        df = DataFrame([{"A": 1, "B": 2}])
        out_border_default = df.to_html()
        out_border_true = df.to_html(border=True)
        out_border_explicit_default = df.to_html(border=1)
        out_border_nondefault = df.to_html(border=2)
        out_border_zero = df.to_html(border=0)

        out_border_false = df.to_html(border=False)

        assert ' border="1"' in out_border_default
        assert out_border_true == out_border_default
        assert out_border_default == out_border_explicit_default
        assert out_border_default != out_border_nondefault
        assert ' border="2"' in out_border_nondefault
        assert ' border="0"' not in out_border_zero
        assert " border" not in out_border_false
        assert out_border_zero == out_border_false

    @pytest.mark.parametrize(
        "displayed_only,exp0,exp1",
        [
            (True, DataFrame(["foo"]), None),
            (False, DataFrame(["foo  bar  baz  qux"]), DataFrame(["foo"])),
        ],
    )
    def test_displayed_only(self, displayed_only, exp0, exp1):
        # GH 20027
        data = StringIO(
            """<html>
          <body>
            <table>
              <tr>
                <td>
                  foo
                  <span style="display:none;text-align:center">bar</span>
                  <span style="display:none">baz</span>
                  <span style="display: none">qux</span>
                </td>
              </tr>
            </table>
            <table style="display: none">
              <tr>
                <td>foo</td>
              </tr>
            </table>
          </body>
        </html>"""
        )

        dfs = self.read_html(data, displayed_only=displayed_only)
        tm.assert_frame_equal(dfs[0], exp0)

        if exp1 is not None:
            tm.assert_frame_equal(dfs[1], exp1)
        else:
            assert len(dfs) == 1  # Should not parse hidden table

    @pytest.mark.filterwarnings(
        "ignore:You provided Unicode markup but also provided a value for "
        "from_encoding.*:UserWarning"
    )
    def test_encode(self, html_encoding_file):
        base_path = os.path.basename(html_encoding_file)
        root = os.path.splitext(base_path)[0]
        _, encoding = root.split("_")

        try:
            with open(html_encoding_file, "rb") as fobj:
                from_string = self.read_html(
                    fobj.read(), encoding=encoding, index_col=0
                ).pop()

            with open(html_encoding_file, "rb") as fobj:
                from_file_like = self.read_html(
                    BytesIO(fobj.read()), encoding=encoding, index_col=0
                ).pop()

            from_filename = self.read_html(
                html_encoding_file, encoding=encoding, index_col=0
            ).pop()
            tm.assert_frame_equal(from_string, from_file_like)
            tm.assert_frame_equal(from_string, from_filename)
        except Exception:
            # seems utf-16/32 fail on windows
            if is_platform_windows():
                if "16" in encoding or "32" in encoding:
                    pytest.skip()
            raise

    def test_parse_failure_unseekable(self):
        # Issue #17975

        if self.read_html.keywords.get("flavor") == "lxml":
            pytest.skip("Not applicable for lxml")

        class UnseekableStringIO(StringIO):
            def seekable(self):
                return False

        bad = UnseekableStringIO(
            """
            <table><tr><td>spam<foobr />eggs</td></tr></table>"""
        )

        assert self.read_html(bad)

        with pytest.raises(ValueError, match="passed a non-rewindable file object"):
            self.read_html(bad)

    def test_parse_failure_rewinds(self):
        # Issue #17975

        class MockFile:
            def __init__(self, data) -> None:
                self.data = data
                self.at_end = False

            def read(self, size=None):
                data = "" if self.at_end else self.data
                self.at_end = True
                return data

            def seek(self, offset):
                self.at_end = False

            def seekable(self):
                return True

            # GH 49036 pylint checks for presence of __next__ for iterators
            def __next__(self):
                ...

            def __iter__(self) -> Iterator:
                # `is_file_like` depends on the presence of
                # the __iter__ attribute.
                return self

        good = MockFile("<table><tr><td>spam<br />eggs</td></tr></table>")
        bad = MockFile("<table><tr><td>spam<foobr />eggs</td></tr></table>")

        assert self.read_html(good)
        assert self.read_html(bad)

    @pytest.mark.slow
    def test_importcheck_thread_safety(self, datapath):
        # see gh-16928

        class ErrorThread(threading.Thread):
            def run(self):
                try:
                    super().run()
                except Exception as err:
                    self.err = err
                else:
                    self.err = None

        # force import check by reinitalising global vars in html.py
        reload(pandas.io.html)

        filename = datapath("io", "data", "html", "valid_markup.html")
        helper_thread1 = ErrorThread(target=self.read_html, args=(filename,))
        helper_thread2 = ErrorThread(target=self.read_html, args=(filename,))

        helper_thread1.start()
        helper_thread2.start()

        while helper_thread1.is_alive() or helper_thread2.is_alive():
            pass
        assert None is helper_thread1.err is helper_thread2.err

    def test_parse_path_object(self, datapath):
        # GH 37705
        file_path_string = datapath("io", "data", "html", "spam.html")
        file_path = Path(file_path_string)
        df1 = self.read_html(file_path_string)[0]
        df2 = self.read_html(file_path)[0]
        tm.assert_frame_equal(df1, df2)

    def test_parse_br_as_space(self):
        # GH 29528: pd.read_html() convert <br> to space
        result = self.read_html(
            """
            <table>
                <tr>
                    <th>A</th>
                </tr>
                <tr>
                    <td>word1<br>word2</td>
                </tr>
            </table>
        """
        )[0]

        expected = DataFrame(data=[["word1 word2"]], columns=["A"])

        tm.assert_frame_equal(result, expected)

    @pytest.mark.parametrize("arg", ["all", "body", "header", "footer"])
    def test_extract_links(self, arg):
        gh_13141_data = """
          <table>
            <tr>
              <th>HTTP</th>
              <th>FTP</th>
              <th><a href="https://en.wiktionary.org/wiki/linkless">Linkless</a></th>
            </tr>
            <tr>
              <td><a href="https://en.wikipedia.org/">Wikipedia</a></td>
              <td>SURROUNDING <a href="ftp://ftp.us.debian.org/">Debian</a> TEXT</td>
              <td>Linkless</td>
            </tr>
            <tfoot>
              <tr>
                <td><a href="https://en.wikipedia.org/wiki/Page_footer">Footer</a></td>
                <td>
                  Multiple <a href="1">links:</a> <a href="2">Only first captured.</a>
                </td>
              </tr>
            </tfoot>
          </table>
          """

        gh_13141_expected = {
            "head_ignore": ["HTTP", "FTP", "Linkless"],
            "head_extract": [
                ("HTTP", None),
                ("FTP", None),
                ("Linkless", "https://en.wiktionary.org/wiki/linkless"),
            ],
            "body_ignore": ["Wikipedia", "SURROUNDING Debian TEXT", "Linkless"],
            "body_extract": [
                ("Wikipedia", "https://en.wikipedia.org/"),
                ("SURROUNDING Debian TEXT", "ftp://ftp.us.debian.org/"),
                ("Linkless", None),
            ],
            "footer_ignore": [
                "Footer",
                "Multiple links: Only first captured.",
                None,
            ],
            "footer_extract": [
                ("Footer", "https://en.wikipedia.org/wiki/Page_footer"),
                ("Multiple links: Only first captured.", "1"),
                None,
            ],
        }

        data_exp = gh_13141_expected["body_ignore"]
        foot_exp = gh_13141_expected["footer_ignore"]
        head_exp = gh_13141_expected["head_ignore"]
        if arg == "all":
            data_exp = gh_13141_expected["body_extract"]
            foot_exp = gh_13141_expected["footer_extract"]
            head_exp = gh_13141_expected["head_extract"]
        elif arg == "body":
            data_exp = gh_13141_expected["body_extract"]
        elif arg == "footer":
            foot_exp = gh_13141_expected["footer_extract"]
        elif arg == "header":
            head_exp = gh_13141_expected["head_extract"]

        result = self.read_html(gh_13141_data, extract_links=arg)[0]
        expected = DataFrame([data_exp, foot_exp], columns=head_exp)
        tm.assert_frame_equal(result, expected)

    def test_extract_links_bad(self, spam_data):
        msg = (
            "`extract_links` must be one of "
            '{None, "header", "footer", "body", "all"}, got "incorrect"'
        )
        with pytest.raises(ValueError, match=msg):
            read_html(spam_data, extract_links="incorrect")

    def test_extract_links_all_no_header(self):
        # GH 48316
        data = """
        <table>
          <tr>
            <td>
              <a href='https://google.com'>Google.com</a>
            </td>
          </tr>
        </table>
        """
        result = self.read_html(data, extract_links="all")[0]
        expected = DataFrame([[("Google.com", "https://google.com")]])
        tm.assert_frame_equal(result, expected)

    def test_invalid_dtype_backend(self):
        msg = (
            "dtype_backend numpy is invalid, only 'numpy_nullable' and "
            "'pyarrow' are allowed."
        )
        with pytest.raises(ValueError, match=msg):
            read_html("test", dtype_backend="numpy")
