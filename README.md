# WXRobot

## 🔥 运行

**创建虚拟环境**

```
python -m venv venv
```

**window**

```
.\venv\Scripts\activate
```

**ubuntu**

```
source venv/bin/activate
```

**安装依赖**

```
# 升级 pip
python -m pip install -U pip
# 安装必要依赖
pip install -r requirements.txt
```



## 🔆 新功能

[2024/05/24] 



# 📝Thinkings

[2024/05/24] 

当我在调用语言大模型的api时，一次只能进行一次问答，即我问他回答,然后再重复进行问答操作，但是日常中的问答是多次的。假如我想分多次提问，先问他你知道西红柿炒鸡蛋吗？然后再问这道菜怎么做？
这是两次问答，但是内容是关连的，我该如何实现呢？

**策略**
如果API支持会话跟踪（session tracking），可以在开始对话时创建一个会话，并在随后的每次提问中传递这个会话ID。这样，模型就能记住之前的交互内容。

如果API不支持会话跟踪，可以在每次请求中手动传递上下文信息。
示例：
第一次问答：
问：你知道什么是西红柿炒鸡蛋吗？
答：西红柿炒鸡蛋是一种中国家常菜，主要由西红柿和鸡蛋炒制而成。

第二次问答：
问：
【问：你知道什么是西红柿炒鸡蛋吗？
答：西红柿炒鸡蛋是一种中国家常菜，主要由西红柿和鸡蛋炒制而成。】
这道菜应该如何去做？
答：西红柿炒鸡蛋的做法通常是先将鸡蛋打散炒熟盛出，然后炒西红柿至出汁，最后将炒好的鸡蛋倒回锅中与西红柿一起翻炒，加入适量的盐和糖调味即可。

在实际API调用中，可能需要将这种格式化的上下文作为请求的一部分发送给模型：

```
{
  "context": "问：你知道什么是西红柿炒鸡蛋吗？\n答：西红柿炒鸡蛋是一种中国家常菜，主要由西红柿和鸡蛋炒制而成。",
  "query": "这道菜应该如何去做？"
}
```





# 🛠️待办

- [ ] 使用WeChatFerry项目实现对微信的接受信息和输出信息的功能
- [ ] 对群内信息进行操作，即 允许相应的群组中被@才能回复对应的信息
- [ ] 对接deepseek大语言模型，实现简单的api调用
- [ ] 实现大语言模型的简单对话





## 🍀 致谢

- **WeChatFerry**
  - 作者: lich0821
  - 项目地址: [GitHub](https://github.com/lich0821/WeChatFerry)
  - 描述: WeChatFerry 是一个用于微信消息互通的开源项目，提供了丰富的功能和灵活的配置选项。
  - 许可证: [MIT License](https://github.com/lich0821/WeChatFerry/blob/master/LICENSE)
- **WeChatRobot**
  - 作者: lich0821
  - 项目地址: [GitHub](https://github.com/lich0821/WeChatRobot)
  - 描述: WeChatRobot 是一个用于自动化微信交互的开源项目，它允许用户通过编程方式控制微信账号，实现自动回复、消息管理等功能。
  - 许可证: [MIT License](https://github.com/lich0821/WeChatRobot/blob/master/LICENSE)



































