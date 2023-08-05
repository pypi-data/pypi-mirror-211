# vLogs SDK for Python

A simple way to collect logs and send to the server via simple SDK.

-   [x] Collect the logs
-   [ ] Support local retries

### Install via `pip`

```shell
pip install vlogs
```

### Usages

```python
from vlogs.sdk import VLogs, VLogsOptions
from vlogs.model import Collector, CollectorType, CollectorSource
import asyncio

appId = "72bd14c306a91fa8a590330e3898ddcc"
apiKey = "vlogs_gX9WwSdKatMNdpUClLU0IfCx575tvdoeQ"

# Create VLogs instance
sdk = VLogs.create(
    VLogsOptions.builder()
    .apiKey(apiKey)
    .appId(appId)
    .build()
)

async def main():
    response = await sdk.collect(
        Collector.builder()
        .type(CollectorType.Error)
        .source(CollectorSource.Other)
        .message("This is a test message")
        .build()
    )

    print("Response: ", response)

# Run the async function
asyncio.run(main())
```

### Build, Install, and Test from Source

```shell
make
```

### Build and Install from Source

```shell
make build install
```

### Run test

```shell
make test
```

### Publish

-   Set Token

```shell
poetry config pypi-token.pypi my-token
```

-   Publish

```shell
make publish
```

### Contributors

-   Sambo Chea <sombochea@cubetiqs.com>
