import os
from ws4py.client.tornadoclient import TornadoWebSocketClient
import json


DATA_DIR = '/tmp/boomchat/'
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


class PresenceClient(TornadoWebSocketClient):

    def __init__(self, url, token, onreceive, *args, **kw):
        TornadoWebSocketClient.__init__(self, url, *args, **kw)
        self.onreceive = onreceive
        self.token = token

    def opened(self):
        self.send(json.dumps({'token': self.token,
                              'action': 'auth'}))

    def received_message(self, msg):
        data = json.loads(msg.data)
        print 'received from presence: %s' % str(data)
        self.onreceive(data)

    def _cleanup(self):
        pass


class Presence(object):
    def __init__(self):
        self.prefs_file = os.path.join(DATA_DIR, 'prefs')

        if not os.path.exists(self.prefs_file):
            prefs = {'appid': '3c7d8f58-6bf4-45ff-9eb6-c8dba534eafc',
                     'service': 'ws://presence.services.mozilla.com/_presence/myapps/',
                     'token': '05eed446-9b1d-403b-95c6-744b8e1e6015'}

        else:
            with open(self.prefs_file) as f:
                prefs = json.loads(f.read())

        self.appid = prefs['appid']
        self.service = prefs['service']
        self.token = prefs['token']
        self.sync()

        self.statuses = {}
        self._subs = []
        self._ws = None
        self.initialize()

    def sync(self):
        prefs = {'appid': self.appid,
                 'service': self.service,
                 'token': self.token}

        with open(self.prefs_file, 'w') as f:
            f.write(json.dumps(prefs))

    def initialize(self):
        if self._ws is not None and not self._ws.terminated:
            self._ws.close()

        url = os.path.join(self.service, self.appid)
        self._ws = PresenceClient(url, token=self.token,
                                  onreceive=self.update_status)

        self._ws.connect()

    def register(self, callable):
        self._subs.append(callable)

    def unregister(self, callable):
        self._subs.remove(callable)

    def get_status(self, email):
        return self.statuses.get(email, 'unknown')

    # triggered by the presence service via websockets
    def update_status(self, data):
        # proxying the data directly
        # to all
        for sub in self._subs:
            sub(data)

    def notify(self, source, target, message):
        self._ws.send(json.dumps({'token': self.token,
                                  'action': 'notify',
                                  'source': source,
                                  'target': target,
                                  'message': message}))
