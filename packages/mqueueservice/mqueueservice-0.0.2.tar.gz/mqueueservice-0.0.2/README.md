# activeMqServices

To build a free queue service in Python using ActiveMQ and package it as a reusable package.

## requirements

For running this, you need to have `python3` installed on your system.


## Installation
```

pip install mqueueservice==0.0.1

```

## Example

```
from queueService.queueService import QueueService

#Create an instance of the QueueService class
service = QueueService(host='localhost', port=61613, username='your_username', password='your_password', destination='/queue/test')

service.connect() #Connect to ActiveMQ

service.send_message('Hello, World Mr Shrijeet!') # Send a message

msg=service.receive_message()  # This will start listening for incoming messages# Receive messages

service.disconnect() # Disconnect from ActiveMQ
```