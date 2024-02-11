import queue
import websocket
from flask import Flask, request, jsonify
from tools import *
import httpx
import ConfigLoader
from Logger import *
import json
import random

config = ConfigLoader.load_config()
api_app = Flask(__name__)
logger = Logger()
logger.set_level(config.log_level)
global report, ws


@api_app.route("/", methods=["POST"])
def api_test():
    data = analysis(request)
    return jsonify(data)


@api_app.route("/<api>", methods=["GET", "POST"])
def http_handler(api):
    data = analysis(request)
    if data.get("message") and type(data["message"]) is str:
        data["message"] = CQCode.to_code(data["message"])
    if config.listen_protocol == "HTTP":
        if request.method == "POST" or request.method == "GET":
            response = httpx.post(config.onebot_url + "/" + api, json=data)
            logger.log(f"转发请求{api}({config.listen_protocol})")
        else:
            logger.log(f"收到不被允许的请求方式：{request.method}", levels.ERROR)
            return jsonify({"error": "Method Not Allowed"}), 405
        return response.json(), 200
    else:
        echo = "harcic_safe_ob_" + str(random.randint(1000, 9999))
        payload = {
            "action": api,
            "params": rewrite(data),
            "echo": echo
        }
        # print(payload)
        ws.send(json.dumps(payload))
        logger.log(f"转发请求{api}({config.listen_protocol})")
        response = report.get()
        try:
            return json.loads(response), 200
        except TypeError:
            return response, 200


def run(report_queue: queue.Queue, socket: websocket.WebSocketApp) -> None:
    global report, ws
    report = report_queue
    ws = socket
    api_app.run(debug=False, host="0.0.0.0", port=config.listen_port)
    logger.log(f"成功在端口{config.listen_port}启动OneBot API监听")
