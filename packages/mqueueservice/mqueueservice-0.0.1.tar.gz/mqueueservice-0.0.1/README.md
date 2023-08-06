# activeMqServices

To build a free queue service in Python using ActiveMQ and package it as a reusable package.

## requirements

For running this, you need to have `python3` installed on your system.


## Installation
```
Download the tar file from the below link:
https://github.com/Soniyasharma6868/queueServicePkg.git

pip install queue-service-1.0.0.tar.gz

```

## Example

1. Queue Service Configuration
```
from pyqservice.queue_service import QueueService

* Create an instance of the QueueService class
service = QueueService(host='localhost', port=61613, username='admin', password='admin', destination='/queue/test')
```

2. Connect to ActiveMQ
service.connect()

3. Send a message
service.send_message('Hello, World!')

4. Receive messages
service.receive_message()  # This will start listening for incoming messages

5. Disconnect from ActiveMQ
service.disconnect()
