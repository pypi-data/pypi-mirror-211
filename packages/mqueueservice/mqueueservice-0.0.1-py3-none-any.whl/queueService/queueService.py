import stomp

class MyListener(stomp.ConnectionListener):
    
    ''' MyListener() is the message listener class  to handle incoming messages.'''
    def on_message(self, headers, message):
        print("Received message:", message)


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
        self.conn = stomp.Connection([(self.host, self.port)])
        self.conn.connect(self.username, self.password, wait=True)

    def send_message(self, message):
        
        ''' The send_message() sends a message to the queue '''
        self.conn.send(self.destination, message)

    def receive_message(self):
        
        ''' The receive_message() subscribes to the queue and starts listening for incoming messages '''
        self.conn.set_listener('', MyListener())  
        self.conn.subscribe(self.destination)

    def disconnect(self):
        
        ''' The disconnect() closes the connection'''
        self.conn.disconnect()
