from sender import RabbitSender
import time
import sys

ca_cert = sys.argv[1]
client_cert = sys.argv[2]
client_key = sys.argv[3]
s = RabbitSender('localhost',5671, 'guest', 'guest', 'ATOM', ca_cert=ca_cert, client_cert=client_cert, client_key=client_key)
s.connect()
while True:
    s.send_message('direct_exchange', 'test', 10, 'Hello World')
    print('Sent one message')
    time.sleep(5)
