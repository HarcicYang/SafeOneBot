import queue
from flask import Flask, request
from tools import *
import httpx
import ConfigLoader
import websocket
import json
from Logger import *

config = ConfigLoader.load_config()
listener = Flask(__name__)
logger = Logger()
logger.set_level(config.log_level)
global report, ws


@listener.route("/")
def listen():
    data = analysis(request)
    response = httpx.post(config.report_url, json=data)
    logger.log("转发上报到客户端", levels.TRACE)
    try:
        return response.json()
    except:
        return response.text


def ws_listen(ws_method, post):
    data = json.loads(post)
    if data.get("echo") is not None:
        report.put(data)
    else:
        if data.get("raw_message") and type(data.get("message")) is not str:
            data["raw_message"] = CQCode.to_text(data["message"])
        response = httpx.post(config.report_url, json=data)
        logger.log("转发上报到客户端", levels.TRACE)
        try:
            return response.json()
        except:
            return response.text


def run(report_queue: queue.Queue, socket: websocket.WebSocketApp) -> None:
    global report, ws
    report = report_queue
    ws = socket
    if config.listen_protocol == "HTTP":
        listener.run(debug=False, host="0.0.0.0", port=config.onebot_port)
        logger.log(f"成功在端口{config.onebot_port}启动OneBot监听")
    elif config.listen_protocol == "ForwardWebSocket":
        ws.run_forever()
    else:
        logger.log(f"未知的协议 {config.listen_protocol}", level=levels.CRITICAL)
