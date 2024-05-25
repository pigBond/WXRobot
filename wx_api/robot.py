import re
import time
from queue import Empty
from threading import Thread
import logging
from .job_mgmt import Job
from wcferry import Wcf, WxMsg
from .utils import cmd_init,log_folder_init
from .configuration import Config
from .gpt_api.deepseek import DeepSeek

class Robot(Job):

    def __init__(self, config: Config, wcf: Wcf, type_:int) -> None:
        self.wcf = wcf
        self.wxid = self.wcf.get_self_wxid()
        self.config = config
        self.chat_type=type_
        log_folder = 'logs/robot_log'
        cmd_init()
        log_folder_init(log_folder)
        self.LOG = logging.getLogger("root")
        time.sleep(1)
        self.LOG.info(f"机器人启动成功  wxid = {self.wxid}")
        self.chat=self.initRobotModel()

    def initRobotModel(self):
        model = DeepSeek()
        self.LOG.info("当前 gpt 模型: deepseek-chat")
        return model

    def enableRecvMsg(self) -> None:
        self.wcf.enable_recv_msg(self.onMsg)

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    self.LOG.info(msg)
                    self.processMsg(msg)
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    self.LOG.exception(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()

    def toAt(self, msg: WxMsg) -> bool:
        """
            处理被 @ 消息
            param msg: 微信消息结构
            return: 处理状态,True 成功,False 失败
        """
        return self.toChitchat(msg)
    
    def toChitchat(self, msg: WxMsg) -> bool:
        """
            闲聊，接入 ChatGPT
        """
        if not self.chat:  # 没接 ChatGPT，固定回复
            rsp = "目前并不在线"
        else:  # 接了 ChatGPT，智能回复
            q = re.sub(r"@.*?[\u2005|\s]", "", msg.content).replace(" ", "")

            content=q
            # 检查是否包含特定指令格式 "#指令"
            if content.startswith("#"):
                command = content[1:].strip()
                if command == "介绍自己":
                    if msg.from_group():
                        self.sendTextMsg("我是机器人", msg.roomid,msg.sender)
                    else:
                        self.sendTextMsg("我是机器人",msg.sender)
                    return True
            else:
                # rsp = self.chat.get_answer(q, (msg.roomid if msg.from_group() else msg.sender))
                if self.chat_type==0:
                    # 对话交流
                    rsp = self.chat.get_answer_communicate(q, (msg.roomid if msg.from_group() else msg.sender))
                elif self.chat_type==1:
                    # 职业厨师
                    rsp = self.chat.get_answer_role(q, (msg.roomid if msg.from_group() else msg.sender))
                elif self.chat_type==2:
                    if msg.from_group():
                        self.sendPictureMsg(r"C:\Users\PIGPIG\Documents\GitHub\WXRobot\0.png",msg.roomid,msg.sender)
                    else:
                        self.sendPictureMsg(r"C:\Users\PIGPIG\Documents\GitHub\WXRobot\0.png",msg.sender)
                    return True
        if rsp:
            if msg.from_group():
                self.sendTextMsg(rsp, msg.roomid, msg.sender)
            else:
                self.sendTextMsg(rsp, msg.sender)

            return True
        else:
            self.LOG.error(f"无法从 GPT 获得答案")
            return False

    def onMsg(self, msg: WxMsg) -> int:
        try:
            self.LOG.info(msg)  # 打印信息
            self.processMsg(msg)
        except Exception as e:
            self.LOG.error(e)
        return 0
    
    def processMsg(self, msg: WxMsg) -> None:
        """
            当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
            此处可进行自定义发送的内容,如通过 msg.content 关键字自动获取当前天气信息，并发送到对应的群组@发送者
            群号:msg.roomid  微信ID:msg.sender  消息内容:msg.content
            content = "xx天气信息为:"
            receivers = msg.roomid
            self.sendTextMsg(content, receivers, msg.sender)
        """
        # 群聊消息
        if msg.from_group():
            # 如果在群里被 @
            if msg.roomid not in self.config.GROUPS:  # 不在配置的响应的群列表里，忽略
                return

            if msg.is_at(self.wxid):  # 被@
                self.toAt(msg)

            return  # 处理完群聊信息，后面就不需要处理了

        # 非群聊信息，按消息类型进行处理
        if msg.type == 37:  # 好友请求
            # self.autoAcceptFriendRequest(msg)
            pass

        elif msg.type == 10000:  # 系统信息
            # self.sayHiToNewFriend(msg)
            pass
        elif msg.type == 0x01:  # 文本消息
            if msg.from_self():
                if msg.content == "^更新$":
                    self.config.reload()
                    self.LOG.info("已更新")
            else:
                self.toChitchat(msg)  # 闲聊

    def sendTextMsg(self, msg: str, receiver: str, at_list: str = "") -> None:
        """ 
            发送消息
            param msg: 消息字符串
            param receiver: 接收人wxid或者群id
            param at_list: 要@的wxid, @所有人的wxid为:notify@all
        """
        # msg 中需要有 @ 名单中一样数量的 @
        ats = ""
        if at_list:
            if at_list == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = at_list.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f" @{self.wcf.get_alias_in_chatroom(wxid, receiver)}"

        # {msg}{ats} 表示要发送的消息内容后面紧跟@，例如 北京天气情况为：xxx @张三
        if ats == "":
            # 个人私聊回复
            self.LOG.info(f"To {receiver}: {msg}")
            self.wcf.send_text(f"{msg}", receiver, at_list)
        else:
            self.LOG.info(f"To {receiver}: {ats}\r{msg}")
            self.wcf.send_text(f"{ats}\n\n{msg}", receiver, at_list)

    def sendPictureMsg(self,path_: str,room:str,receiver: str):
        if room=="":
            # 个人
            sender_code,sender_name=self.get_info_by_wxid(receiver)
            self.LOG.info(f"To code:{sender_code} - name:{sender_name} - wxid:{receiver} : Picture Path: {path_}")
            self.wcf.send_image(path_,receiver)  
        else:
            # 群
            self.LOG.info(f"To roomid:{receiver} : Picture Path: {path_}")
            self.wcf.send_image(path_,room) 

    def keepRunningAndBlockProcess(self) -> None:
        """
            保持机器人运行，不让进程退出
        """
        while True:
            self.runPendingJobs()
            time.sleep(1)

    def get_info_by_wxid(self,receiver:str):
        receiver_info=self.wcf.get_info_by_wxid(receiver)
        # print(receiver_info)
        info_name=receiver_info["name"]
        info_code=receiver_info["code"]
        return info_code,info_name