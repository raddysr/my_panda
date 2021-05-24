from typing import Type
import numpy as np

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
            if i ==  0:
                length  = len(value)
            elif length != len(value):
                raise ValueError('The arrays values must ne with the same length')
            

    def _convert_unicode_to_object(self,data):
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
        self._data = dict(zip(columns,self._data.values()))

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
        DTYPE_NAME = {'O':'string', 'i':'int', 'f':'float', 'b':'bool'}
        col_names = np.array(list(self._data.keys()))
        dtypes = [DTYPE_NAME[value.dtype.kind] for value in self._data.values()]
        dtypes = np.array(dtypes)
        new_data = {'Column Name': col_names, 'Data Type': dtypes}
        return DataFrame(new_data)

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