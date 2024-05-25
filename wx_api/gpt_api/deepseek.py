from openai import OpenAI

# sk-10d4455cdba64892933c394e93ef1f6d
API_KEY="sk-10d4455cdba64892933c394e93ef1f6d"

prompt_str="""
请你根据下面的内容为我撰写菜谱
例如，我问你  xxx
你将以下面的模板回复我
xxx是xxxx菜，主要由xxx食材制作而成。制作方法是xxx,这部分简单介绍一下。xxx菜的特点是xxxx
菜谱为
1.xxx
-xxxx
-xxx
2.xxxx
3.xxx
这道菜的关键在于xxxxxxx
为保证你理解，下面是示例
西红柿炒鸡蛋是一道简单而美味的家常菜，主要由西红柿和鸡蛋两种食材制作而成。制作方法通常是将鸡蛋打散后在锅中炒至半熟，然后加入切块的西红柿继续翻炒，直至西红柿出汁、鸡蛋完全熟透。这道菜色泽鲜艳，口感酸甜适中，营养丰富，深受人们喜爱。

1. 准备食材：
   - 新鲜西红柿2-3个（根据大小和个人口味调整）
   - 鸡蛋3-4个
   - 盐适量
   - 白糖少许（可选，用于调整酸甜度）
   - 葱花少许（可选，用于增加香气）
   - 食用油适量

2. 处理食材：
   - 西红柿洗净后切成小块。
   - 鸡蛋打入碗中，加入少许盐，用筷子或打蛋器打散。

3. 烹饪步骤：
   - 在锅中倒入适量食用油，加热至油温适中（约150-180°C）。
   - 倒入打散的鸡蛋液，快速翻炒至鸡蛋凝固但仍保持嫩滑，然后盛出备用。
   - 在同一个锅中加入少许油，加热后放入西红柿块，翻炒至西红柿开始出汁。
   - 如果喜欢甜味，可以在这一步加入少许白糖。
   - 当西红柿炒至软烂出汁时，将之前炒好的鸡蛋倒回锅中，快速翻炒均匀。
   - 根据口味调整盐的量，撒上葱花，炒匀后即可出锅。

4. 装盘：
   - 将炒好的西红柿炒鸡蛋装入盘中，即可享用。

这道菜的关键在于掌握好火候，使鸡蛋保持嫩滑，西红柿的酸甜味与鸡蛋完美融合。根据个人口味，还可以添加其他调料，如胡椒粉、蒜末等，以增加风味。

注意在我问你具体的菜谱名称前，你只需要介绍你自己是谁，你能做什么事。
如果你收到菜名以外的内容，你要回答“我是做菜大师，除了做菜我什么也不会”
"""

prompt_str_2="你需要使用中文回答问题，并且注意你的回答要尽可能避免markdown的语法，例如#或*，注意你的回答不应该用双星号来进行加粗，你只需要输出纯文字，除了正常用语的标点符号或者序号.你回答时应尽可能保证你是作为一个人来回答问题，而不是机器人，你要假装你是人"

class DeepSeek:
    def __init__(self) -> None:
        self.stream_=False
        self.client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
        self.conversation_history = [
            {"role": "system", "content": prompt_str_2},
        ]

    def __repr__(self):
        return 'DeepSeek'

    def get_answer_communicate(self, msg: str, sender: str = None) -> str:
        self.conversation_history.append({"role": "user", "content": msg})
        # "你需要使用中文回答问题，并且注意你的回答要尽可能避免markdown的语法，例如#或*，注意你的回答不应该用双星号来进行加粗，你只需要输出纯文字，除了正常用语的标点符号或者序号.你回答时应尽可能保证你是作为一个人来回答问题，而不是机器人，你要假装你是人"
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.conversation_history,
            stream=False
        )
        assistant_response = response.choices[0].message.content
    
        # Append the assistant's response to the conversation history
        self.conversation_history.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
    
    def get_answer_role(self, msg: str, sender: str = None) -> str:
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt_str},
                {"role": "user", "content": msg},
            ],
            stream=False
        )
        return response.choices[0].message.content