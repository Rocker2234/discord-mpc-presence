import logging
import os
import time

import bs4
import pypresence
import requests

mpc_url = 'http://localhost:13579/'
keep_extentions = False
update_interval = 2


class MPCPresence:
    def __init__(self, presence: pypresence.Presence, url: str, interval: float, preserve_ext: bool,
                 logs: logging.Logger):
        self.mpc_client = presence
        self.interval = interval
        self.url = url.rstrip('/')
        self.is_connected = False
        self.is_running = False
        self.responce = None
        self.keep_exn = preserve_ext
        self.title = ''
        self.statestring = ''
        self.load_time = 0
        self.logger = logs

    def connect_mpc(self):
        if self.is_connected:
            return
        print("Connecting MPC Presence!")
        self.mpc_client.connect()
        self.is_connected = True

    def close_mpc(self):
        if self.is_connected:
            print('Closing MPC Presence!')
            self.mpc_client.close()
            self.is_running = False
            self.is_connected = False
            self.title = ''
            self.statestring = ''
            self.load_time = 0

    def get_status(self):
        try:
            responce = requests.get(f"{self.url}/variables.html")
            if responce.status_code == 200:
                self.is_running = True
                self.responce = responce
            elif self.is_connected:
                self.close_mpc()
        except requests.exceptions.ConnectionError:
            self.is_running = False

    def update_presence(self):
        soup = bs4.BeautifulSoup(self.responce.text, features='lxml')
        state = int(soup.find('p', {"id": 'state'}).text)
        if state != -1:
            title = soup.find('p', {"id": 'file'}).text
            if not self.keep_exn:
                title = ".".join(title.split('.')[:-1])
            self.statestring = soup.find('p', {"id": 'statestring'}).text.lower()
            if self.title != title:
                self.title = title
                self.load_time = int(time.time())
                if not self.is_connected:
                    self.connect_mpc()
            if self.is_connected:
                self.mpc_client.update(state=self.title, details='Playing Media', start=self.load_time,
                                       large_image='mpc_hc', large_text='MPC HC', small_image=self.statestring)

    def run(self):
        while True:
            self.get_status()
            if self.is_running:
                self.update_presence()
            elif self.is_connected:
                self.close_mpc()
            time.sleep(self.interval)

    def __del__(self):
        self.close_mpc()


if not os.path.isdir('Logs'):
    print('Creating Logs Folder')
    os.mkdir('Logs')
if not os.path.isfile('Logs/run.log'):
    print('Creating Log File')
    open('Logs/run.log', 'a').close()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(module)s:%(levelname)s:%(asctime)s:%(message)s")

log_file = logging.FileHandler('Logs/run.log', 'a')
log_file.setFormatter(fmt)
logger.addHandler(log_file)


def get_presence(client_id: str) -> pypresence.Presence:
    while 1:
        try:
            return pypresence.Presence(client_id=client_id)
        except pypresence.exceptions.DiscordNotFound:
            print('No dis')
            time.sleep(3)


try:
    print("Starting")
    mpc = MPCPresence(get_presence('1074295283049054248'), mpc_url, update_interval, keep_extentions, logger)
    mpc.run()
except KeyboardInterrupt:
    exit(0)
except pypresence.exceptions.InvalidID:
    print("Client ID is invalid or you are not connected to the internet!")
    logger.error("Invalid Client ID or no internet connection!")
except Exception as e:
    print("Unhandeled exception as occured!")
    logger.critical('An unhandeled exception as occured!', exc_info=e)
