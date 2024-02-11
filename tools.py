import flask
import re
from Logger import *
import ConfigLoader

config = ConfigLoader.load_config()
logger = Logger()
logger.set_level(config.log_level)


class CQCode:
    @staticmethod
    def to_text(coded: list) -> str:
        text = ""
        for i in coded:
            if i["type"] == "text":
                text += str(i["data"]["text"])
            else:
                cq_text = f"[CQ:{i['type']}"
                for j in i["data"]:
                    cq_text += f",{j}={i['data'][j]}"
                cq_text += "]"
                text += cq_text
        logger.log("成功解析消息", levels.TRACE)
        return text

    @staticmethod
    def to_code(text: str) -> list:
        pattern = r'\[CQ:[a-zA-Z0-9]{2,}(?:,[^]]*)*\]'
        code_list = []
        coded = []
        cq = re.search(pattern, text)
        while cq:
            code_list.append(cq.group())
            text = text.replace(cq.group(), "DIV&_a1W1a_DIV&")
            cq = re.search(pattern, text)

        text_list = text.split("DIV&")
        j = 0
        for i in text_list:
            if i != "_a1W1a_":
                if i == "":
                    continue
                coded.append({"type": "text", "data": {"text": i}})
            else:
                data = {}
                try:
                    to_code = (str(code_list[j])
                               .replace("[", "")
                               .replace("]", "")
                               .replace("CQ:", "")).split(",")
                except IndexError:
                    continue
                j += 1
                code_type = ""
                for k in to_code:
                    k = k.split("=")
                    if len(k) == 1:
                        code_type = k[0]
                        continue
                    key = k[0]
                    value = k[1]
                    data[key] = value
                coded.append({"type": code_type, "data": data})
        logger.log("成功解析CQ码", levels.TRACE)
        return coded


def analysis(requested: flask.request) -> dict:
    if requested.method == "POST":
        if requested.is_json:
            return requested.json
        else:
            json_data = {}
            for key in requested.form:
                json_data[key] = requested.form[key]
            return rewrite(json_data)
    else:
        json_data = {}
        for key in requested.args:
            json_data[key] = requested.args[key]
        return rewrite(json_data)


def rewrite(json_data: dict) -> dict:
    if json_data.get("user_id"):
        json_data["user_id"] = int(json_data["user_id"])
    if json_data.get("group_id"):
        json_data["group_id"] = int(json_data["group_id"])
    if json_data.get("message_id"):
        json_data["message_id"] = int(json_data["message_id"])
    if json_data.get("times"):
        json_data["times"] = int(json_data["times"])
    if json_data.get("duration"):
        json_data["duration"] = int(json_data["duration"])
    if json_data.get("delay"):
        json_data["delay"] = int(json_data["delay"])
    logger.log("修正不规范开发", levels.TRACE)
    return json_data
