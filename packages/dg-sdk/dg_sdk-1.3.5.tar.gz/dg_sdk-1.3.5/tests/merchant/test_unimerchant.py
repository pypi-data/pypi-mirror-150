import unittest
from tests.conftest import *


class TestUniPayMerchant(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_apply_register_mer(self):
        file = dg_sdk.FileInfo("F120", "file_idfile_id", "fileName")
        file2 = dg_sdk.FileInfo("F121", "file_idfile_id", "fileName")
        file_list = [file, file2]
        result = dg_sdk.UniPayMerchant.apply_register_mer(mer_type="MERCHANT_02",
                                                          legal_mobile="13122223333",
                                                          deal_type="02",
                                                          contract_id_no="3104222233222222",
                                                          file_list=file_list,
                                                          )
        assert result["sub_resp_code"] == "00000003"

    def test_query_apply_reg(self):
        result = dg_sdk.UniPayMerchant.query_apply_reg(serial_no="wk521722712574541824")
        assert result["sub_resp_code"] == "00000003"

    def test_query_mer_base_info(self):
        result = dg_sdk.UniPayMerchant.query_mer_base_info(mer_no="521722712545181696")
        assert result["sub_resp_code"] == "00000000"

    def test_query_activity_list(self):
        result = dg_sdk.UniPayMerchant.query_activity_list()
        assert result["sub_resp_code"] == "00000000"

    def test_enlist_activity(self):
        result = dg_sdk.UniPayMerchant.enlist_activity(activity_id="activity_id",
                                                       mer_no="521722712545181696")
        assert result["sub_resp_code"] == "00000003"

    def test_query_enlish_activity_status(self):
        result = dg_sdk.UniPayMerchant.query_enlish_activity_status(enlist_id="enlist_id")
        assert result["sub_resp_code"] == "00000003"
