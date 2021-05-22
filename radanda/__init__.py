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

    def __len__(self):
        for value in self._data.values():
            return len(value)

        


    def StringMethods(self):
        pass

    def add_docs(sefl):
        pass


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
    pass