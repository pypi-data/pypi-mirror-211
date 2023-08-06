import stomp
from stomp.exception import ConnectFailedException,NotConnectedException
import logging
import time

console = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)
logging.getLogger().setLevel(logging.INFO)
LOGGER = logging.getLogger('my-client')

class MyListener(stomp.ConnectionListener):
    
    ''' MyListener() is the message listener class  to handle incoming messages.'''
    
    def on_error(self, message):
        logging.error('received an error "%s"' % message.body)
    
    def on_message(self, message):
        logging.debug('message recieved')
        logging.info('message: "%s"' % message)
        logging.debug('message processed: "%s"' % str(message.body))
        logging.info('response sent')


class QueueService:
    
    ''' ActiveMQ configuration '''
    def __init__(self, host, port, username, password, destination):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.destination = destination
        self.conn = None

    def connect(self):
        
        ''' The connect() method establishes a connection to the ActiveMQ broker '''
        try:
            self.conn = stomp.Connection()
            self.conn.connect(self.username, self.password, wait=True)
            logging.info("Connection successful")
        except ConnectFailedException as e:
            logging.error(f"Failed to connect to the STOMP server: {str(e)}")
        except NotConnectedException:
            logging.error("Not connected to the STOMP server")

    def send_message(self, message):
        
        ''' The send_message() sends a message to the queue '''
        self.conn.send(destination=self.destination, body=message)

    def receive_message(self):
        ''' The receive_message() subscribes to the queue and starts listening for incoming messages '''
        self.conn.set_listener('', MyListener())  
        self.conn.subscribe(destination=self.destination,id=1,ack="auto")
    

    def disconnect(self):
        
        ''' The disconnect() closes the connection'''
        time.sleep(2)
        self.conn.disconnect()


