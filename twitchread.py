import os
import socket
import logging
from emoji import demojize
import stats


sock = socket.socket()

server = 'irc.chat.twitch.tv'
port = 6667
nickname = os.environ["NICKNAME"]
token = os.environ["TOKEN"]
channel = os.environ["CHANNEL"]

sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))
resp = sock.recv(2048).decode('utf-8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8', mode='w')])

while True:

    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    elif len(resp) > 0:
        if 'Bets are OPEN for' in resp:
            logging.info(demojize(resp))
            stats.run()

        if 'Bets are locked' in resp:
            logging.info(demojize(resp))

        if 'wins! Payouts to' in resp:
            logging.info(demojize(resp))
            stats.run()
            
        print(resp) #uncomment to read chat live in container logs