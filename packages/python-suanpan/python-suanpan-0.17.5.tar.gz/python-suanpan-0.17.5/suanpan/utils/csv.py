# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan import path
from suanpan.lazy_import import lazy_import

pd = lazy_import('pandas')

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO  # pylint: disable=bad-option-value


def load(file, *args, **kwargs):
    kwargs.setdefault("index_col", 0)
    return pd.read_csv(file, *args, **kwargs)


def loads(string, *args, **kwargs):
    return pd.read_csv(StringIO(string), *args, **kwargs)


def dump(dataframe, file, *args, **kwargs):
    path.safeMkdirsForFile(file)
    dataframe.to_csv(file, *args, **kwargs)
    return file


def dumps(dataframe, *args, **kwargs):
    output = StringIO()
    dataframe.to_csv(output, *args, **kwargs)
    return output.getvalue()
