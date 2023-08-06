CONFIG_FILE = '/etc/rvr/config.ini'

LOG_TYPE_APPLICATION_EVENT = 'app_event'

VALID_MESSAGE_TYPES = {'debug', 'info', 'warning', 'error'}

NOTIFY_APPLICATION_EVENT = '{type} on {node}: {message}.'

# Messages
MSG_POST_DATA_SUCCESS = 'Accepted payload: {body}.'
MST_STARTING = 'Starting, notify URL:{url}.'

# Errors:
ERR_POST_DATA = 'Unable to Write: {status_code}.'
ERR_POST_DATA_TO_AZURE = 'Failed to post data to Azure. Error: {message}.'
ERR_GETTING_TOKEN = 'Failed to get a valid token from Azure. Error: {status_code}.'
ERR_GETTING_AZURE_DATA = 'Failed to read from Azure Log Analytics workspace. Error {status_code}'
ERR_INIT_AZURE_READER_API = 'Failed to initialize the Azure_reader_api with error: {error}'
