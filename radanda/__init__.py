import numpy as np

__version__ = '0.0.1'


class DataFrame:

    def __init__(self, data):
        
        self._check_input_types(data)

        self._check_array_legths(data)

        self._data = self._convert_unicode_to_object(data)

      #  self.str = StringMethods(self)
        
        self.add_docs()

        print("in init statement")



    def _check_input_types(self, data):
        pass

    def _check_array_legths(self, data):
        pass
    
    def _convert_unicode_to_object(self,data):
        pass

    def StringMethods(self):
        pass

    def add_docs(sefl):
        pass