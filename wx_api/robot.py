import time
from queue import Empty
from threading import Thread
import logging
from .job_mgmt import Job
from wcferry import Wcf, WxMsg
from .utils import cmd_init,log_folder_init
from .configuration import Config

class Robot(Job):

    def __init__(self, config: Config, wcf: Wcf) -> None:
        self.wcf = wcf
        self.wxid = self.wcf.get_self_wxid()

        log_folder = 'logs/robot_log'
        cmd_init()
        log_folder_init(log_folder)
        self.LOG = logging.getLogger("root")
        time.sleep(1)

        self.LOG.info(f"机器人启动成功  wxid = {self.wxid}")

        self.LOG.warning("12331")

        # self.LOG.error("错误")


    def enableRecvMsg(self) -> None:
        self.wcf.enable_recv_msg(self.onMsg)

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    print("******************************")
                    print("接收到的信息为 = ",msg)
                    print("******************************")
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    print(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()

    def sendTextMsg(self, msg: str, receiver: str) -> None:
        """ 
            发送消息
        """
        at_list=""
        self.wcf.send_text(f"{msg}", receiver, at_list)
            
    def keepRunningAndBlockProcess(self) -> None:
        """
            保持机器人运行，不让进程退出
        """
        while True:
            self.runPendingJobs()
            time.sleep(1)