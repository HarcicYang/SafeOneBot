import API
import Listener
import threading
from Logger import *
import websocket
import ConfigLoader
import queue

report = queue.Queue()
config = ConfigLoader.load_config()
logger = Logger()
logger.set_level(config.log_level)
try:
    ws = websocket.WebSocketApp(url=config.onebot_url, on_message=Listener.ws_listen)
    threading.Thread(target=API.run, args=(report, ws)).start()
    logger.log("启动API监听")
    threading.Thread(target=Listener.run, args=(report, ws)).start()
    logger.log("启动OneBot监听")
    logger.log("SafeOneBot 开始监听和转发请求")
except KeyboardInterrupt:
    logger.log("即将退出...")