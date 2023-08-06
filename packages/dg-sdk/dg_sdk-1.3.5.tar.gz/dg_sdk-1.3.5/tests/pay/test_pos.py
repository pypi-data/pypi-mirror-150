import unittest
from tests.conftest import *


class TestPos(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_device_info(self):
        terminal_device_data = json.dumps({"device_id": "660035152267200170401",
                                           "client_ip": "127.0.0.1",
                                           "network": '1',
                                           "sendTime": "20220107143632"})
        result = dg_sdk.POS.query("20091225", "1",
                                  terminal_device_data,
                                  out_order_id="out_order_id")
        assert result["resp_code"] == "23000001"
