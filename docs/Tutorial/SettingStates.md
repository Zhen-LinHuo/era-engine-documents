# 设置状态

## 概述

在 `FSM 模式` 下，游戏本质上是状态 `state` 间的转移，因此显而易见的，制作游戏的主要工作便是各个状态的脚本。

## 创造你的第一个状态

1. 创建并编辑 `main_state.gd`
2. 编写状态
   - 创建一个 `main_state` 函数，作为这个状态的入口：
     
     ```gdscript
      func main_state():
          TXT("era靛紫档案")  # Create a text unit
          BOX([   # Create a series of units, pack in a box
              BTN("开始游戏", "start_game"),  # Create a button unit, and set corresponding next state name
              BTN("读取存档", "load_game")
              ])
      ```
       你可以使用 `BOX` 来包裹一组界面显示单元，并且用这种方式调整它们的布局。对于各个UI元素，诸如 `TXT`、`BTN`、`BOX` 等，参考API文档来查看更进一步的参数选项。

   - 可以注意到的是，一个按钮 `BTN` 显然会带来状态的转换，因此在它声明时也指定了它被点击时应当转向的新状态的名字。
3. 下一个状态函数
   1.使用如下代码来设置下一个状态 (`start_game` 和 `load_game`):
   
      ```gdscript
      func start_game():
          TXT("你喜欢什么样的主角？")
          BTN("喜爱淑女的主角", "select_char_0")
          BTN("财大气粗的主角", "select_char_1")
          BTN("神父气质的主角", "select_char_2")
          BTN("流氓热血的主角", "select_char_3")

      func load_game():
          TXT("读取存档")
          BTN("读取不了，返回", "main_state")
     
      # Continue with select_char_0, select_char_1, select_char_2, select_char_3...
      ```
      现在，你的 `main_state` 的按钮应该可以正常工作了。如果你希望继续完成编码工作，那么 `start_game` 部分声明了更多状态，你可以继续完善这些代码。
   2. 遵循这样的工作流程，你就可以逐步构建你的第一个游戏 