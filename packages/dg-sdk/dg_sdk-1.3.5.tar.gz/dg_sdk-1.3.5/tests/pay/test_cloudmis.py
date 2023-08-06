import unittest
from tests.conftest import *


class TestCloudmis(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_device_info(self):
        result = dg_sdk.Cloudmis.device_info(device_id="device_id",
                                             json_data="{\"bgRetUrl\":\"virgo://https://www.baidu.com\",\"channelId\":\"acquire\",\"goodsDesc\":\"测试交易\",\"interfaceType\":\"payment\",\"ordAmt\":\"1\",\"outOrdId\":\"202110281322319876\"}")
        assert result["resp_code"] == "10000000"
