import unittest
import mock

from rvrbase.api import Azure_reader_api


class Testrvrconfig(unittest.TestCase):

    @mock.patch('requests.post')
    def test_initialize_happy(self, mock_requests_post):
        mock_requests_post.return_value = mock.Mock()
        mock_requests_post.return_value.status_code = 200
        mock_requests_post.return_value.content = b'{"access_token":"bsaccessToken"}'

        tenant = '13ebf573-f6a0-4a5a-a14e-578ba97ec355'
        sp_id = '274cef59-fa12-4b39-92f7-5175bc279424'
        sp_secret = '3p78Q~pLBhy.dsafjowieup_xoafasfwea89.'
        az_workspace_id = '274cef59-fa12-4b39-92f7-5175bc279424'
        Azure_reader_api(tenant, sp_id, sp_secret, az_workspace_id)

        mock_requests_post.assert_called()

    @mock.patch('requests.post')
    def test_initialize_unhappy(self, mock_requests_post):

        mock_requests_post.return_value = mock.Mock()
        mock_requests_post.return_value.status_code = 400
        mock_requests_post.return_value.content = b'{"access_token":"bsaccessToken"}'

        tenant = '13ebf573-f6a0-4a5a-a14e-578ba97ec355'
        sp_id = '274cef59-fa12-4b39-92f7-5175bc279424'
        sp_secret = '3p78Q~pLBhy.dsafjowieup_xoafasfwea89.'
        az_workspace_id = '274cef59-fa12-4b39-92f7-5175bc279424'

        with self.assertRaises(RuntimeError):
            Azure_reader_api(tenant, sp_id, sp_secret, az_workspace_id)

    @mock.patch('requests.get')
    @mock.patch('requests.post')
    def test_get_data_happy(self, mock_requests_post, mock_requests_get):
        mock_requests_post.return_value = mock.Mock()
        mock_requests_post.return_value.status_code = 200
        mock_requests_post.return_value.content = b'{"access_token":"bsaccessToken"}'

        mock_requests_get.return_value = mock.Mock()
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.content = b'{"some":"json"}'

        tenant = '13ebf573-f6a0-4a5a-a14e-578ba97ec355'
        sp_id = '274cef59-fa12-4b39-92f7-5175bc279424'
        sp_secret = '3p78Q~pLBhy.dsafjowieup_xoafasfwea89.'
        az_workspace_id = '274cef59-fa12-4b39-92f7-5175bc279424'
        api = Azure_reader_api(tenant, sp_id, sp_secret, az_workspace_id)

        query = 'Some KQL query'
        api.get_data(query)

        mock_requests_get.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.post')
    def test_get_data_unhappy(self, mock_requests_post, mock_requests_get):
        mock_requests_post.return_value = mock.Mock()
        mock_requests_post.return_value.status_code = 200
        mock_requests_post.return_value.content = b'{"access_token":"bsaccessToken"}'

        mock_requests_get.return_value = mock.Mock()
        mock_requests_get.return_value.status_code = 400
        mock_requests_get.return_value.content = b'{"some":"json"}'

        tenant = '13ebf573-f6a0-4a5a-a14e-578ba97ec355'
        sp_id = '274cef59-fa12-4b39-92f7-5175bc279424'
        sp_secret = '3p78Q~pLBhy.dsafjowieup_xoafasfwea89.'
        az_workspace_id = '274cef59-fa12-4b39-92f7-5175bc279424'
        api = Azure_reader_api(tenant, sp_id, sp_secret, az_workspace_id)

        query = 'Some KQL query'
        with self.assertRaises(RuntimeError):
            api.get_data(query)


if __name__ == '__main__':
    unittest.main()
