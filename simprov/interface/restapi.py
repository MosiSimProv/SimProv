from threading import Thread

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from simprov.interface.browser_api_blueprint import BrowserAPI
from simprov.interface.capturer_api_blueprint import CapturerAPI
from simprov.interface.debug_api_blueprint import DebugAPI


class RestAPI():

    def __init__(self, simprov) -> None:
        super().__init__()
        path = "../../webinterface"
        self.simprov = simprov
        self.app = Flask(__name__, instance_relative_config=True, template_folder=path, static_folder=path,
                         static_url_path="/")
        self.socketio = SocketIO(self.app,logger=True,engineio_logger=True,cors_allowed_origins="*")
        CORS(self.app)
        self.__load_blueprints()

    def start(self):
        Thread(target=lambda: self.socketio.run(self.app, host="0.0.0.0", allow_unsafe_werkzeug=True, debug=True,
                                                use_reloader=False)).start()

    def __load_blueprints(self):
        self.__load_blueprint(CapturerAPI, prefix="/capturer")
        self.__load_blueprint(DebugAPI, prefix="/debug")
        self.__load_blueprint(BrowserAPI)

    def __load_blueprint(self, wrapped_blueprint_class, prefix=""):
        wrappend_blueprint_instance = wrapped_blueprint_class(self.simprov)
        self.app.register_blueprint(wrappend_blueprint_instance.blueprint, url_prefix=prefix)
