import os
import shutil
from art import text2art

def cmd_init():
    clear_cmd() # 清空cmd
    terminal_size = get_terminal_size()
    max_width = terminal_size.columns  # 获取最大宽度
    print("\n" * 1)
    print("-" * max_width)
    print("\n" * 3)
    # 生成并打印适应大小的字符艺术字
    art_text = generate_sized_art("WxRobot", max_width)
    print(art_text)
    print("\n" * 3)
    print("-" * max_width)

def clear_cmd():
    os.system('cls')

def get_terminal_size():
    # 获取终端大小
    return shutil.get_terminal_size((80, 20))  # 默认值可以设置为80x20字符

def generate_sized_art(text, max_width):
    # 生成字符艺术字，并限制宽度
    art = text2art(text)
    lines = art.split('\n')
    sized_lines = []
    for line in lines:
        if len(line) > max_width:
            # 如果行宽超过最大宽度，则截断
            sized_lines.append(line[:max_width])
        else:
            sized_lines.append(line)
    return '\n'.join(sized_lines)
