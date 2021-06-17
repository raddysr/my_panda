from typing import NewType
import numpy as np
from numpy.lib import unique

__version__ = '0.0.1'


class DataFrame:
    def __init__(self, data):
        self._check_input_types(data)
        self._check_array_legths(data)
        self._data = self._convert_unicode_to_object(data)
     #   self.str = StringMethods(self)
        self.add_docs()

    def _check_input_types(self, data):
        if not isinstance(data, dict):
            raise TypeError('`data` must be a dictionary')
        for key, value in data.items():
            if not isinstance(key, str):
                raise TypeError('key must be string')
            if not isinstance(value, np.ndarray):
                raise TypeError('value must be numpy array')
            if value.ndim != 1:
                raise ValueError('value must be one dimensional')

    def _check_array_legths(self, data):
        for i, value in enumerate(data.values()):
            if i == 0:
                length = len(value)
            elif length != len(value):
                raise ValueError(
                    'The arrays values must ne with the same length')

    def _convert_unicode_to_object(self, data):
        new_data = {}
        for key, value in data.items():
            if value.dtype.kind == 'U':
                new_data[key] = value.astype('object')
            else:
                new_data[key] = value
        return new_data

    @property
    def columns(self):
        return(list(self._data))

    @columns.setter
    def columns(self, columns):
        if not isinstance(columns, list):
            raise TypeError('`columns` must be a list')
        if len(columns) != len(self._data):
            raise ValueError('`new` colums must be equal length with as df')
        for column in columns:
            if not isinstance(column, str):
                raise TypeError('`col` must be a string')
        if len(columns) != len(set(columns)):
            raise ValueError('Your column have duplicates')
        self._data = dict(zip(columns, self._data.values()))

    def __len__(self):
        return len(next(iter(self._data.values())))

    def StringMethods(self):
        pass

    def add_docs(sefl):
        pass

    @property
    def shape(self):
        return len(self), len(self._data)

    def _repr_html_(self):
        """
        Used to create a string of HTML to nicely display the DataFrame
        in a Jupyter Notebook. Different string formatting is used for
        different data types.

        The structure of the HTML is as follows:
        <table>
            <thead>
                <tr>
                    <th>data</th>
                    ...
                    <th>data</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
                ...
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
            </tbody>
        </table>
        """
        html = '<table><thead><tr><th></th>'
        for col in self.columns:
            html += f"<th>{col:10}</th>"
        html += '</tr></thead>'
        html += "<tbody>"
        only_head = False
        num_head = 10
        num_tail = 10
        if len(self) <= 20:
            only_head = True
            num_head = len(self)
        for i in range(num_head):
            html += f'<tr><td><strong>{i}</strong></td>'
            for col, values in self._data.items():
                kind = values.dtype.kind
                if kind == 'f':
                    html += f'<td>{values[i]:10.3f}</td>'
                elif kind == 'b':
                    html += f'<td>{values[i]}</td>'
                elif kind == 'O':
                    v = values[i]
                    if v is None:
                        v = 'None'
                    html += f'<td>{v:10}</td>'
                else:
                    html += f'<td>{values[i]:10}</td>'
            html += '</tr>'
        if not only_head:
            html += '<tr><strong><td>...</td></strong>'
            for i in range(len(self.columns)):
                html += '<td>...</td>'
            html += '</tr>'
            for i in range(-num_tail, 0):
                html += f'<tr><td><strong>{len(self) + i}</strong></td>'
                for col, values in self._data.items():
                    kind = values.dtype.kind
                    if kind == 'f':
                        html += f'<td>{values[i]:10.3f}</td>'
                    elif kind == 'b':
                        html += f'<td>{values[i]}</td>'
                    elif kind == 'O':
                        v = values[i]
                        if v is None:
                            v = 'None'
                        html += f'<td>{v:10}</td>'
                    else:
                        html += f'<td>{values[i]:10}</td>'
                html += '</tr>'

        html += '</tbody></table>'
        return html

    @property
    def values(self):
        return np.column_stack(list(self._data.values()))

    @property
    def dtypes(self):
        DTYPE_NAME = {'O': 'string', 'i': 'int', 'f': 'float', 'b': 'bool'}
        col_names = np.array(list(self._data.keys()))
        dtypes = [DTYPE_NAME[value.dtype.kind]
                  for value in self._data.values()]
        dtypes = np.array(dtypes)
        new_data = {'Column Name': col_names, 'Data Type': dtypes}
        return DataFrame(new_data)

    def __getitem__(self, item):
        if isinstance(item, str):
            return DataFrame({item: self._data[item]})
        if isinstance(item, list):
            return DataFrame({col: self._data[col] for col in item})
        if isinstance(item, DataFrame):
            if item.shape[1] != 1:
                raise ValueError('item must be a two column dataframe')
            arr = next(iter(item._data.values()))
            if arr.dtype.kind != 'b':
                raise ValueError('item must a one-column boolean DataFrame')
            new_data = ({col: value[arr] for col, value in self._data.items()})
            return DataFrame(new_data)
        if isinstance(item, tuple):
            return self._getitem_tuple(item)
        raise TypeError(
            "The input must be string, list, DataFrame or tuple!!!")

    def _getitem_tuple(self, item):
        if len(item) != 2:
            raise ValueError('item tuple must have length 2')
        row_selection, col_selection = item
        if isinstance(row_selection, int):
            row_selection = [row_selection]
        elif isinstance(row_selection, DataFrame):
            if row_selection.shape[1] != 1:
                raise ValueError('Row selection DataFrame must be one column')
            row_selection = next(iter(row_selection._data.values()))
            if row_selection.dtype.kind != 'b':
                raise TypeError('row selection DataFrame must be a boolean')
        elif not isinstance(row_selection, (list, slice)):
            raise TypeError(
                "row selectiom must bee int, list, slice or DataFrame")
        if isinstance(col_selection, int):
            col_selection = [self.columns[col_selection]]
        elif isinstance(col_selection, str):
            col_selection = [col_selection]
        elif isinstance(col_selection, list):
            new_col_selection = []
            for col in col_selection:
                if isinstance(col, int):
                    new_col_selection.append(self.columns[col])
                else:
                    new_col_selection.append(col)
            col_selection = new_col_selection
        elif isinstance(col_selection, slice):
            start = col_selection.start
            stop = col_selection.stop
            step = col_selection.step
            if isinstance(start, str):
                start = self.columns.index(start)
            if isinstance(stop, str):
                stop = self.columns.index(stop) + 1
            col_selection = self.columns[start:stop:step]
        else:
            raise TypeError('column must list, str, int or slice')
        new_data = {}
        for col in col_selection:
            new_data[col] = self._data[col][row_selection]
        return DataFrame(new_data)

    def _ipython_key_completions_(self):
        # allow tab completion when doing df['c....']
        return self.columns

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise NotImplementedError('Setting only a single column')
        if isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise ValueError("Setting only a one dimetional array")
            if len(value) != len(self):
                raise ValueError('Length of setting array must match length')
        elif isinstance(value, DataFrame):
            if value.shape[1] != 1:
                raise ValueError('Setting must be one column')
            if len(value) != len(self):
                raise ValueError('Setting DataFrame must be same length')
            value = next(iter(value._data.values()))
        elif isinstance(value, (int, bool, str, float)):
            value = np.repeat(value, len(self))
        else:
            raise TypeError("Setting object must array, DataFrame or ....")      
        if value.dtype.kind == 'U':
            value = value.astype('object')  
        self._data[key] = value
            
    def head(self, n=5):
        return self[:n,:]

    def tail(self, n=5):
        tail = len(self) - n # or -n
        return self[tail: , :]

    def min(self):
        return self._agg(np.min)

    def max(self):
        return self._agg(np.max)

    def mean(self):
        return self._agg(np.mean)

    def median(self):
        return self._agg(np.median)

    def sum(self):
        return self._agg(np.sum)

    def var(self):
        return self._agg(np.var)

    def std(self):
        return self._agg(np.std)

    def all(self):
        return self._agg(np.all)

    def any(self):
        return self._agg(np.any)

    def argmax(self):
        return self._agg(np.argmax)

    def argmin(self):
        return self._agg(np.argmin)

    def _agg(self, aggfunc):
        new_data = {}
        for col, value in self._data.items():
            try:
                new_data[col] = np.array([aggfunc(value)])
            except TypeError:
                pass
        return DataFrame(new_data)
    
    def is_nan(self):    
        new_data = {}
        for col, value in self._data.items():
            if value.dtype.kind == 'O':
                new_data[col] = value == None
            else:
                new_data[col] = np.isnan(value)
        return DataFrame(new_data)

    def count(self):     
        df = self.is_nan()      
        new_data = {}
        length = len(df)
        for col, value in df._data.items():
            new_data[col] = np.array([length - value.sum()])
        return DataFrame(new_data)
    
    def unique(self):               
        dfs = []
        for col,value in self._data.items():
            new_data = {col: np.unique(value)}
            dfs.append(DataFrame(new_data))
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def nunique(self):
        new_data = {}
        for col,value in self._data.items():
            new_data[col] = np.array([len(np.unique(value))])
        return DataFrame(new_data)

    def value_counts(self, normalize=False):
        dfs = []
        for col, value in self._data.items():
            uniques, counts = np.unique(value, return_counts=True)
            order = np.argsort(-counts)
            uniques = uniques[order]
            counts = counts[order]
            if normalize:
                counts = counts/len(self)
            df =DataFrame({col: uniques, 'count': counts})
            dfs.append(df)
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def rename(self, columns):
        if not isinstance(columns, dict):
            raise ValueError("Columns must be a dict type")
        new_data = {}
        for col, value in self._data.items():
            new_col = columns.get(col, col)
            new_data[new_col] = value
        return DataFrame(new_data)

    def drop(self, columns):
        if isinstance(columns,str):
            columns = [columns]
        elif not isinstance(columns, list):
            raise TypeError("Columns must be a string")
        new_data = {}
        for col, value in self._data.items():
            if not col in columns:
                new_data[col] = value
        return DataFrame(new_data)
        
    def abs(self):
        """
        Takes the absolute value of each value in the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.abs)

    def cummin(self):
        """
        Finds cumulative minimum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.minimum.accumulate)

    def cummax(self):
        """
        Finds cumulative maximum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.maximum.accumulate)

    def cumsum(self):
        """
        Finds cumulative sum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.cumsum)

    def clip(self, lower=None, upper=None):
        """
        All values less than lower will be set to lower
        All values greater than upper will be set to upper

        Parameters
        ----------
        lower: number or None
        upper: number or None

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.clip, a_min=lower, a_max=upper)

    def round(self, n):
        """
        Rounds values to the nearest n decimals

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.round, 'if', decimals=n)

    def copy(self):
        """
        Copies the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.copy)

    def _non_agg(self, funcname, kinds='bif', **kwargs):
        """
        Generic non-aggregation function

        Parameters
        ----------
        funcname: numpy function
        args: extra arguments for certain functions

        Returns
        -------
        A DataFrame


        """
        new_data = {}
        for col, values in self._data.items():
            if values.dtype.kind in kinds:
                values = funcname(values, **kwargs)
            else:
                values = values.copy()
            new_data[col] = values
        return DataFrame(new_data)

    def diff(self, n=1):
        """
        Take the difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(values):
            values = values.astype('float')
            values_shifted = np.roll(values, n)
            values = values - values_shifted
            if n >= 0:
                values[:n] = np.NAN
            else:
                values[n:] = np.NAN
            return values
        return self._non_agg(func)
        #### Arithmetic and Comparison Operators ####

    def __add__(self, other):
        return self._oper('__add__', other)

    def __radd__(self, other):
        return self._oper('__radd__', other)

    def __sub__(self, other):
        return self._oper('__sub__', other)

    def __rsub__(self, other):
        return self._oper('__rsub__', other)

    def __mul__(self, other):
        return self._oper('__mul__', other)

    def __rmul__(self, other):
        return self._oper('__rmul__', other)

    def __truediv__(self, other):
        return self._oper('__truediv__', other)

    def __rtruediv__(self, other):
        return self._oper('__rtruediv__', other)

    def __floordiv__(self, other):
        return self._oper('__floordiv__', other)

    def __rfloordiv__(self, other):
        return self._oper('__rfloordiv__', other)

    def __pow__(self, other):
        return self._oper('__pow__', other)

    def __rpow__(self, other):
        return self._oper('__rpow__', other)

    def __gt__(self, other):
        return self._oper('__gt__', other)

    def __lt__(self, other):
        return self._oper('__lt__', other)

    def __ge__(self, other):
        return self._oper('__ge__', other)

    def __le__(self, other):
        return self._oper('__le__', other)

    def __ne__(self, other):
        return self._oper('__ne__', other)

    def __eq__(self, other):
        return self._oper('__eq__', other)

    def _oper(self, op, other):
        """
        Generic operator method

        Parameters
        ----------
        op: str name of special method
        other: the other object being operated on

        Returns
        -------
        A DataFrame
        """
        if isinstance(other, DataFrame):
            if other.shape[1] != 1:
                raise ValueError('`other` must be a one-column DataFrame')
            other = next(iter(other._data.values()))
        new_data = {}
        for col, values in self._data.items():
            func = getattr(values, op)
            new_data[col] = func(other)
        return DataFrame(new_data)

    def pct_change(self, n=1):
        """
        Take the percentage difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(values):
            values = values.astype('float')
            values_shifted = np.roll(values, n)
            values = values - values_shifted
            if n >= 0:
                values[:n] = np.NAN
            else:
                values[n:] = np.NAN
            return values / values_shifted
        return self._non_agg(func)
    
    def sort_values(self, by, asc=True):
        if isinstance(by, str):
            order = np.argsort(self._data[by])
        elif isinstance(by, list):
            by = [self._data[col] for col in by[::-1]]
            order = np.lexsort(by)
        else:
            raise TypeError('`by` must be either a list `')

        if not asc:
            order = order[::-1]

        return self[order.tolist(), :]

    def sample(self, n=None, frac=None, replace=False, seed=None):
        if seed:
            np.random.seed(seed)

        if frac is not None:
            if frac <= 0:
                raise ValueError('`frac` must be positive')
            
            n = int(frac * len(self))
        if n is not None:
            if not isinstance(n, int):
                raise TypeError('`n` must be an int')

            rows = np.random.choice(range(len(self)), n, replace=replace).tolist()
            
        return self[rows, :]

def read_csv(fn):
    """ 
    Read in a comma-separated value file as a DataFrame

    Parameters
    ----------
    fn: string of file location

    Returns
    -------
    A DataFrame
    """
 