from vlogs.model import Collector, CollectorResponse, SDKInfo, Target, VLogsOptions
from vlogs.service import VLogsService
from vlogs.util import get_system_hostname, get_system_username
from vlogs.config import BASE_URL


class VLogs:
    _logger = print
    NAME = 'vlogs'
    VERSION = '1.0.0'
    VERSION_CODE = '1'
    APP_ID_HEADER_PREFIX = 'x-app-id'
    API_KEY_HEADER_PREFIX = 'x-api-key'
    DEFAULT_CONNECT_TIMEOUT = 60  # seconds

    def __init__(self, options: VLogsOptions):
        if not options.appId or not options.apiKey:
            raise ValueError('AppID and ApiKey are required')

        # Set default options
        self._options = options
        self._options.url = self._options.url or BASE_URL

        # Initialize service
        self._service = VLogsService(self._options.url)

        VLogs._logger(
            f'VLogs: Initialized AppID: {self._options.appId} | SDK Version: {VLogs.VERSION}-{VLogs.VERSION_CODE}')

    async def collect(self, request: Collector) -> CollectorResponse:
        VLogs._logger(f'VLogs: Collecting logs for {request.getId()}')

        headers = {
            VLogs.APP_ID_HEADER_PREFIX: self._options.appId,
            VLogs.API_KEY_HEADER_PREFIX: self._options.apiKey,
            'Content-Type': 'application/json',
        }

        hostname = get_system_hostname()
        sender = get_system_username()
        sdk_info = SDKInfo.builder().hostname(hostname).sender(sender).name(
            VLogs.NAME).version(VLogs.VERSION).versionCode(VLogs.VERSION_CODE).build()

        if not request.target:
            if self._options.target:
                request.target = self._options.target
            else:
                request.target = Target.builder().build()
        else:
            if self._options.target:
                request.target.merge(self._options.target)

        # Set SDK info to request
        request.target.sdk_info = sdk_info

        # Append user agent to request
        request.useragent = f'vlogs-python-sdk/{VLogs.VERSION}-{VLogs.VERSION_CODE} ({hostname})'

        response = await self._service.post(request.to_map(), headers, self._options.connectionTimeout or VLogs.DEFAULT_CONNECT_TIMEOUT)
        return response

    @staticmethod
    def create(options: VLogsOptions) -> 'VLogs':
        return VLogs(options)

    @staticmethod
    def create_with(appId: str, apiKey: str) -> 'VLogs':
        return VLogs.create(
            VLogsOptions.builder()
            .api_key(apiKey)
            .app_id(appId)
            .build()
        )
