from wcferry import Wcf
from wx_api.robot import Robot

def main():
    print("******原神启动*******")

    wcf = Wcf(debug=True)

    robot = Robot(wcf)

    # 机器人启动发送测试消息
    robot.sendTextMsg("机器人启动成功！", "filehelper")

    # 机器人接收信息
    robot.enableReceivingMsg()

    # 让机器人一直跑
    robot.keepRunningAndBlockProcess()

if __name__ == "__main__":
    main()
