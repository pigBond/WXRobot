from wcferry import Wcf
from wx_api.robot import Robot
from wx_api.configuration import Config

def main():
    print("******原神启动*******")
    config = Config()
    wcf = Wcf(debug=True)

    # 0 对话交流
    # 1 职业厨师
    robot = Robot(config,wcf,1)

    # 机器人启动发送测试消息
    robot.sendTextMsg("机器人启动成功！", "filehelper")

    # 机器人接收信息
    robot.enableReceivingMsg()

    # 让机器人一直跑
    robot.keepRunningAndBlockProcess()

if __name__ == "__main__":
    main()
