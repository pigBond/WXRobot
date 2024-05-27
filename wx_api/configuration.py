import logging.config
import os
import shutil

import yaml

class Config(object):
    def __init__(self) -> None:
        self.reload()

    def _load_config(self) -> dict:
        pwd = os.path.dirname(os.path.abspath(__file__))

        # 定义目录路径
        directory = "logs\\robot_log"

        # 检查目录是否存在
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory {directory} created.")

        try:
            # 尝试打开并读取config.yaml文件
            with open(f"{pwd}\config.yaml", "rb") as fp:
                print("fp = ",fp)
                yconfig = yaml.safe_load(fp)
        except FileNotFoundError:
            # 如果config.yaml不存在，则从模板复制一个
            shutil.copyfile(f"{pwd}\config.yaml.template", f"{pwd}\config.yaml")
            with open(f"{pwd}\config.yaml", "rb") as fp:
                yconfig = yaml.safe_load(fp)

        # 返回加载的配置
        return yconfig

    def reload(self) -> None:
        yconfig = self._load_config()
        # 使用配置初始化日志系统
        logging.config.dictConfig(yconfig["logging"])
        self.GROUPS = yconfig["groups"]["enable"] # 允许响应的群