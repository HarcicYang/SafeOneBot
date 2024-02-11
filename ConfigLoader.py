import json
from Logger import *

with open("config.json", "r", encoding="utf-8") as config:
    config = json.load(config)


class Config:
    def __init__(self):
        self.report_url = ""
        self.listen_port = ""
        self.onebot_port = ""
        self.onebot_url = ""
        self.listen_protocol = ""
        self.log_level = levels.INFO


def load_config() -> Config:
    configs = Config()
    configs.report_url = config["report_url"]
    configs.listen_port = int(config["listen_port"])
    configs.onebot_url = config["onebot_url"]
    configs.onebot_port = int(config["onebot_port"])
    configs.listen_protocol = config["listen_protocol"]
    configs.log_level = levels.level_names[config["log_level"]]
    if not configs.report_url or not configs.listen_port or not configs.listen_protocol or not configs.onebot_url or not configs.onebot_port:
        Logger().log("不合法的配置文件，请重新编辑", level=levels.CRITICAL)
        sys.exit(1)
    return configs
