#!/usr/bin/bash
#pytest tests/test_dataframe.py::TestDataFrameCreation::$1  
#pytest tests/test_dataframe.py::TestAggregation
#pytest tests/test_dataframe.py::TestSelection::$1  

pytest tests/test_dataframe.py::TestOtherMethods::$1

# Run this file with test_<function name> as a argument
