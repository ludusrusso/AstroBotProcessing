import socket
import threading
import sys

import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space



class AstroClient(threading.Thread):

    def __init__(self, host, port, bot):
        super(AstroClient, self).__init__()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))
        self.data = ""
        self.bot = bot

    def run(self):
        while True:
            self.data = self.conn.recv(1024)
            if self.data != "":
                print 'got:', self.data
                self.bot.send_all(self.data)
                self.data = ""

    def send_msg(self,msg):
        self.conn.send(msg)

    def close(self):
        self.conn.close()


class AstroBotTelegram():
    from sets import Set
    chat_ids = Set([])

    def __init__(self, token, host, port):
        self.bot = telepot.Bot(token)
        self.bot.message_loop(self.handle)

        self.astro_client = AstroClient(host,port, self)
        self.astro_client.daemon = True
        self.astro_client.start()

    def send_all(self, to_send):
        print self.chat_ids
        for chat_id in self.chat_ids:
            self.bot.sendMessage(chat_id, to_send)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            self.bot.sendMessage(chat_id, "Non capisco")
            return

        command = msg['text'].strip().lower()

        if command == '/register':
            if chat_id not in self.chat_ids:
                self.chat_ids.add(chat_id)
                self.bot.sendMessage(chat_id, "Fatto, riceverai messaggi da me!")
            else:
                self.bot.sendMessage(chat_id, "Sei gia' registrato! Usa /unregister se non vuoi ricevere messaggi")

        elif command == '/unregister':
            self.chat_ids.discard(chat_id)
            self.bot.sendMessage(chat_id, "Fatto, non riceverai piu' messaggi da me!")
        else:
            self.bot.sendMessage(chat_id, "Non capisco")


def main():
    TOKEN ='USA IL TUO TOKEN'
    host = ''
    port = 5204
    bot = AstroBotTelegram(TOKEN, host, port)

    import time
    while True:
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'closing'
