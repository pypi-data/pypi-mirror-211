from sender import RabbitSender
import time

s = RabbitSender('localhost',5672, 'guest', 'guest', 'ATOM')
s.connect()
while True:
    s.send_message('direct_exchange', 'test', 10, 'Hello World')
    print('Sent one message')
    time.sleep(5)
