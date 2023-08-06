from flask import Flask, request
from typing import Callable
from daisyfl.server.task_manager import TaskManager
import threading

class ServerListener:
    def __init__(
            self,
            ip: str,
            port: int,
            task_manager: TaskManager,
            cnd_stop: threading.Condition,
        ):
        self.app = Flask(__name__)
        self._ip: str = ip
        self._port: int = port
        self._task_manager: TaskManager = task_manager
        self._cnd_stop: threading.Condition = cnd_stop
        
        @self.app.route("/shutdown", methods=["POST"])
        def shutdown():
            with self._cnd_stop:
                self._cnd_stop.notify()
            return {}, 200
        
        @self.app.route("/receive_task", methods=["POST"])
        def receive_task():
            js = request.get_json()
            self._task_manager.receive_task(task_config=js)
            return js, 200

    def run(self,):
        self.app.run(host=self._ip, port=self._port)

