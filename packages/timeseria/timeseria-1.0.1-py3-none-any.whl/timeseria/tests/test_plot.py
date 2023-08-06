import unittest
import os
from ..datastructures import DataTimePointSeries, DataTimePoint

# Setup logging
from .. import logger
logger.setup()

# Set test data path
TEST_DATA_PATH = '/'.join(os.path.realpath(__file__).split('/')[0:-1]) + '/test_data/'


class TestPlot(unittest.TestCase):

    def test_dygraph_plot(self):

        data_time_point_series = DataTimePointSeries(DataTimePoint(t=60, data=[23.8]),
                                                     DataTimePoint(t=120, data=[24.1]),
                                                     DataTimePoint(t=180, data=[23.9]),
                                                     DataTimePoint(t=240, data=[23.1]),
                                                     DataTimePoint(t=300, data=[22.7]))
        
        #print(data_time_point_series.plot(return_dygraph_html=True))














