
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
                print('got:', self.data)
                self.bot.send_all(self.data)
                self.data = ""

    def send_msg(self,msg):
        self.conn.send(msg)

    def close(self):
        self.conn.close()


class AstroBotTelegram():
    chat_ids = {}

    def __init__(self, token, host, port):
        self.bot = telepot.Bot(token)
        self.bot.message_loop(self.handle)

        self.astro_client = AstroClient(host,port, self)
        self.astro_client.daemon = True
        self.astro_client.start()

    def send_all(self, to_send):
        print(self.chat_ids)
        send_words = to_send.split('#')
        for key, value in self.chat_ids.items():
            if value[0] == True:
                self.bot.sendMessage(chat_id, send_words[0])
            if value[1] == True:
                self.bot.sendMessage(chat_id, send_words[1])

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            self.bot.sendMessage(chat_id, "Non capisco")
            return

        command = msg['text'].strip().lower()

        if command == '/register1':
            if not chat_id in self.chat_ids:
                self.chat_ids[chat_id] = [False, False]
            self.chat_ids[chat_id][0] = True
            self.bot.sendMessage(chat_id, "Fatto, riceverai messaggi da me!")

        if command == '/register2':
            if not chat_id in self.chat_ids:
                self.chat_ids[chat_id] = [False, False]
            self.chat_ids[chat_id][1] = True
            self.bot.sendMessage(chat_id, "Fatto, riceverai messaggi da me!")

        elif command == '/unregister1':
            if not chat_id in self.chat_ids:
                self.chat_ids[chat_id] = [False, False]
            self.chat_ids[chat_id][0] = False
            self.bot.sendMessage(chat_id, "Fatto, non riceverai piu' messaggi da me!")
        elif command == '/unregister2':
            if not chat_id in self.chat_ids:
                self.chat_ids[chat_id] = [False, False]
            self.chat_ids[chat_id][1] = False
            self.bot.sendMessage(chat_id, "Fatto, non riceverai piu' messaggi da me!")
        else:
            self.bot.sendMessage(chat_id, "Non capisco")


def main():
    TOKEN ='379783514:AAGzRiOPUzk6-BWPYgeHgmf8YRjIgOkl1Dw'
    host = ''
    port = 12345
    bot = AstroBotTelegram(TOKEN, host, port)

    import time
    while True:
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('closing')
