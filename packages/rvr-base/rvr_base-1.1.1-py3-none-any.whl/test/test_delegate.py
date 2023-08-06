import unittest
import mock

import rvrbase
from rvrbase.constants import ERR_POST_DATA


class Testrvrconfig(unittest.TestCase):

    def test_rvrconfig_wrong_file(self):
        with self.assertRaises(FileNotFoundError):
            rvrbase.Rvrbase('filedoesnotexist.ini')

    # Patching a private method requires to set the objectname very specific:
    # https://stackoverflow.com/questions/55512708/how-to-properly-mock-private-members-of-a-class
    @mock.patch('requests.post')
    @mock.patch.object(rvrbase.api.Azure_reader_api, '_Azure_reader_api__get_token')
    def test_rvrconfig_q1_success(self, mock_azure_reader_api, mock_requests_post):
        mock_requests_post.return_value = mock.Mock()
        mock_requests_post.return_value.status_code = 200

        config = rvrbase.Rvrbase('src/test/testdata/config.ini')
        self.assertEqual(config.q1('MyfirstLogAnalytics_workspace_id'),
                         '7756814b-7720-4b6d-9fb6-0aa03fe97658')

    @mock.patch('requests.post')
    @mock.patch.object(rvrbase.api.Azure_reader_api, '_Azure_reader_api__get_token')
    def test_rvrconfig_q1_non_existing_key(self, mock_azure_reader_api, mock_requests_post):
        mock_requests_post.return_value = mock.Mock()
        mock_requests_post.return_value.status_code = 200

        config = rvrbase.Rvrbase('src/test/testdata/config.ini')
        self.assertEqual(config.q1('doesnotexist'), None)

    # Happy flow of all the functionality in delegate.
    @mock.patch('requests.post')
    @mock.patch('notify_run.Notify.send')
    @mock.patch('logging.info')
    @mock.patch('logging.warning')
    @mock.patch('logging.error')
    @mock.patch.object(rvrbase.api.Azure_reader_api, '_Azure_reader_api__get_token')
    def test_log_application_event_success2(self, mock_azure_reader_api, mock_logging_error,
                                            mock_logging_warning, mock_logging_info, mock_notify,
                                            mock_requests_post):
        mock_requests_post.return_value = mock.Mock()
        mock_requests_post.return_value.status_code = 200

        rvrlogger = rvrbase.Rvrbase('src/test/testdata/config.ini')
        rvrlogger.log_app_event(
            type='warning', message='No worries, just testing here.', notify_message=True)

        rvrlogger.log_app_event(
            type='error', message='No worries, just testing here.', notify_message=True)

        mock_requests_post.assert_called()
        mock_notify.assert_called()
        mock_logging_info.assert_called()  # should always be called with starting message
        mock_logging_warning.assert_called()
        mock_logging_error.assert_called()

    # Unhappy flow send_az_app_event
    @mock.patch('rvrbase.api.azure_logger_api')
    @mock.patch('logging.error')
    @mock.patch('notify_run.Notify.send')
    @mock.patch.object(rvrbase.api.Azure_reader_api, '_Azure_reader_api__get_token')
    def test_send_az_app_event_error(self, mock_azure_reader_api, mock_notify, mock_logging_error,
                                     mock_azure_logger_api):
        mock_azure_logger_api.side_effect = RuntimeError(
            mock.Mock(ERR_POST_DATA.format(status_code=404)))

        mock_azure_reader_api = mock.Mock()
        mock_azure_reader_api.__get_token = mock.Mock()
        mock_azure_reader_api.__get_token.return_value = 'afa'

        rvrbase.Rvrbase('src/test/testdata/config.ini')

        # An error should be logged to logger and send using notify.
        mock_logging_error.assert_called()
        mock_notify.assert_called()


if __name__ == '__main__':
    unittest.main()
