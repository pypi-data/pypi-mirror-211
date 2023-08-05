import json
import time
from vlogs.util import generate_uuid


class CollectorType:
    Error = "Error"
    Event = "Event"
    Metric = "Metric"
    Trace = "Trace"
    Log = "Log"
    Span = "Span"


class CollectorSource:
    Web = "Web"
    Mobile = "Mobile"
    Server = "Server"
    Desktop = "Desktop"
    IoT = "IoT"
    Other = "Other"


class TelegramParseMode:
    Markdown = "Markdown"
    MarkdownV2 = "MarkdownV2"
    HTML = "HTML"


class TelegramOptions:
    def __init__(self, token=None, chatId=None, parseMode=None, disabled=None, extras=None):
        self.token = token
        self.chatId = chatId
        self.parseMode = parseMode
        self.disabled = disabled
        self.extras = extras


class Telegram:
    def __init__(self, options=None):
        options = options or TelegramOptions()
        self.token = options.token
        self.chatId = options.chatId
        self.parseMode = options.parseMode
        self.disabled = options.disabled
        self.extras = options.extras

    def to_map(self):
        return {
            "token": self.token,
            "chat_id": self.chatId,
            "parse_mode": self.parseMode,
            "disabled": self.disabled,
            "extras": self.extras,
        }

    @staticmethod
    def builder():
        return TelegramBuilder()


class TelegramBuilder:
    def __init__(self):
        self._token = None
        self._chatId = None
        self._parseMode = None
        self._disabled = None
        self._extras = None

    def token(self, token=None):
        self._token = token
        return self

    def chat_id(self, chat_id=None):
        self._chatId = chat_id
        return self

    def parse_mode(self, parse_mode=None):
        self._parseMode = parse_mode
        return self

    def disabled(self, disabled=None):
        self._disabled = disabled
        return self

    def extras(self, extras=None):
        self._extras = extras
        return self

    def build(self):
        return Telegram(
            TelegramOptions(
                token=self._token,
                chatId=self._chatId,
                parseMode=self._parseMode,
                disabled=self._disabled,
                extras=self._extras,
            )
        )


class Discord:
    def __init__(self, webhookId=None, webhookToken=None, webhookUrl=None, disabled=None, extras=None):
        self.webhookId = webhookId
        self.webhookToken = webhookToken
        self.webhookUrl = webhookUrl
        self.disabled = disabled
        self.extras = extras

    def to_map(self):
        return {
            "webhook_id": self.webhookId,
            "webhook_token": self.webhookToken,
            "webhook_url": self.webhookUrl,
            "disabled": self.disabled,
            "extras": self.extras,
        }

    @staticmethod
    def builder():
        return DiscordBuilder()


class DiscordBuilder:
    def __init__(self):
        self._webhookId = None
        self._webhookToken = None
        self._webhookUrl = None
        self._disabled = None
        self._extras = None

    def webhookId(self, webhookId):
        self._webhookId = webhookId
        return self

    def webhookToken(self, webhookToken):
        self._webhookToken = webhookToken
        return self

    def webhookUrl(self, webhookUrl):
        self._webhookUrl = webhookUrl
        return self

    def disabled(self, disabled):
        self._disabled = disabled
        return self

    def extras(self, extras):
        self._extras = extras
        return self

    def build(self):
        return Discord(
            webhookId=self._webhookId,
            webhookToken=self._webhookToken,
            webhookUrl=self._webhookUrl,
            disabled=self._disabled,
            extras=self._extras
        )


class SDKInfo:
    def __init__(self, name=None, version=None, versionCode=None, hostname=None, sender=None):
        self.name = name
        self.version = version
        self.versionCode = versionCode
        self.hostname = hostname
        self.sender = sender

    def toMap(self):
        return {
            'name': self.name,
            'version': self.version,
            'version_code': self.versionCode,
            'hostname': self.hostname,
            'sender': self.sender
        }

    @staticmethod
    def builder():
        return SDKInfoBuilder()


class SDKInfoBuilder:
    def __init__(self):
        self._name = None
        self._version = None
        self._versionCode = None
        self._hostname = None
        self._sender = None

    def name(self, name):
        self._name = name
        return self

    def version(self, version):
        self._version = version
        return self

    def versionCode(self, versionCode):
        self._versionCode = versionCode
        return self

    def hostname(self, hostname):
        self._hostname = hostname
        return self

    def sender(self, sender):
        self._sender = sender
        return self

    def build(self):
        return SDKInfo(
            name=self._name,
            version=self._version,
            versionCode=self._versionCode,
            hostname=self._hostname,
            sender=self._sender
        )


class Target:
    def __init__(self, telegram=None, discord=None, sdkInfo=None):
        self.telegram = telegram
        self.discord = discord
        self.sdkInfo = sdkInfo

    def toMap(self):
        return {
            'telegram': self.telegram.toMap() if self.telegram else None,
            'discord': self.discord.toMap() if self.discord else None,
            'sdk_info': self.sdkInfo.toMap() if self.sdkInfo else None
        }

    def merge(self, defaultTarget=None):
        if not defaultTarget:
            return
        self.telegram = self.telegram or defaultTarget.telegram
        self.discord = self.discord or defaultTarget.discord

    @staticmethod
    def withTelegram(chatId, token=None, parseMode=None, disabled=None, extras=None):
        telegram = Telegram(chatId, token, parseMode, disabled, extras)
        return Target(telegram=telegram)

    @staticmethod
    def withDiscord(webhookUrl, webhookId=None, webhookToken=None, disabled=None, extras=None):
        discord = Discord(webhookUrl, webhookId,
                          webhookToken, disabled, extras)
        return Target(discord=discord)

    @staticmethod
    def builder():
        return TargetBuilder()


class TargetBuilder:
    def __init__(self):
        self._telegram = None
        self._discord = None
        self._sdkInfo = None

    def telegram(self, telegram):
        self._telegram = telegram
        return self

    def discord(self, discord):
        self._discord = discord
        return self

    def sdkInfo(self, sdkInfo):
        self._sdkInfo = sdkInfo
        return self

    def build(self):
        return Target(telegram=self._telegram, discord=self._discord, sdkInfo=self._sdkInfo)


class Collector:
    def __init__(self, id=None, type=None, source=None, message=None, data=None, userAgent=None, timestamp=None, target=None, tags=None):
        self.id = id
        self.type = type
        self.source = source
        self.message = message
        self.data = data
        self.userAgent = userAgent
        self.timestamp = timestamp
        self.target = target
        self.tags = tags

    def getId(self):
        if not self.id:
            self.id = generate_uuid()
        return self.id

    def getTimestamp(self):
        if not self.timestamp:
            self.timestamp = int(time.time() * 1000)
        return self.timestamp

    def toMap(self):
        return {
            'id': self.getId(),
            'type': self.type,
            'source': self.source,
            'message': self.message,
            'data': self.data,
            'user_agent': self.userAgent,
            'timestamp': self.getTimestamp(),
            'target': self.target.toMap() if self.target else None,
            'tags': self.tags,
        }

    def toJson(self):
        return json.dumps(self.toMap())

    @staticmethod
    def builder():
        return CollectorBuilder()


class CollectorBuilder:
    def __init__(self):
        self._id = None
        self._type = None
        self._source = None
        self._message = None
        self._data = None
        self._userAgent = None
        self._timestamp = None
        self._target = None
        self._tags = None

    def id(self, id):
        self._id = id
        return self

    def type(self, type):
        self._type = str(type) if type else None
        return self

    def source(self, source):
        self._source = str(source) if source else None
        return self

    def message(self, message):
        self._message = message
        return self

    def data(self, data):
        self._data = data
        return self

    def userAgent(self, userAgent):
        self._userAgent = userAgent
        return self

    def timestamp(self, timestamp):
        self._timestamp = timestamp
        return self

    def target(self, target):
        self._target = target
        return self

    def tags(self, tags):
        self._tags = tags
        return self

    def build(self):
        return Collector(
            id=self._id,
            type=self._type,
            source=self._source,
            message=self._message,
            data=self._data,
            userAgent=self._userAgent,
            timestamp=self._timestamp,
            target=self._target,
            tags=self._tags,
        )


class CollectorResponse:
    def __init__(self, message=None, id=None):
        self.message = message
        self.id = id


class VLogsOptions:
    def __init__(self, url=None, appId=None, apiKey=None, connectionTimeout=None, testConnection=None, target=None):
        self.url = url
        self.appId = appId
        self.apiKey = apiKey
        self.connectionTimeout = connectionTimeout
        self.testConnection = testConnection
        self.target = target

    @staticmethod
    def builder():
        return VLogsOptionsBuilder()


class VLogsOptionsBuilder:
    def __init__(self):
        self._url = None
        self._appId = None
        self._apiKey = None
        self._connectionTimeout = None
        self._testConnection = None
        self._target = None

    def url(self, url):
        self._url = url
        return self

    def appId(self, appId):
        self._appId = appId
        return self

    def apiKey(self, apiKey):
        self._apiKey = apiKey
        return self

    def connectionTimeout(self, connectionTimeout):
        self._connectionTimeout = connectionTimeout
        return self

    def testConnection(self, testConnection):
        self._testConnection = testConnection
        return self

    def target(self, target):
        self._target = target
        return self

    def telegram(self, telegram):
        if not self._target:
            self._target = Target.builder().telegram(telegram).build()
        else:
            self._target.telegram = telegram
        return self

    def discord(self, discord):
        if not self._target:
            self._target = Target.builder().discord(discord).build()
        else:
            self._target.discord = discord
        return self

    def build(self):
        return VLogsOptions(
            url=self._url,
            appId=self._appId,
            apiKey=self._apiKey,
            connectionTimeout=self._connectionTimeout,
            testConnection=self._testConnection,
            target=self._target,
        )
