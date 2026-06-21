# 布局容器

当你的游戏有多个按钮时，它们默认按顺序从上到下排列。但有时候你希望按钮水平排列、分组显示，或者让文本和按钮在同一个区域内。这就是 `BOX()` 函数的用武之地。

## 什么是 BOX()？

`BOX()` 是一个**布局容器函数**。它接收一个 UI 元素数组，将它们组合在一起，以特定的布局方式显示。

### 基本语法

```gdscript
BOX([元素1, 元素2, 元素3, ...])
```

数组中的每个元素可以是 `TXT()`、`BTN()`，甚至可以是另一个 `BOX()`（嵌套容器）。

## 水平排列按钮

默认情况下，多个 `BTN()` 是垂直排列的：

```gdscript
func main_state():
    TXT("请选择一个选项：")
    BTN("选项 A", "state_a")
    BTN("选项 B", "state_b")
    BTN("选项 C", "state_c")
```

运行后，三个按钮从上到下依次排列。

使用 `BOX()` 可以让它们水平排列：

```gdscript
func main_state():
    TXT("请选择一个选项：")
    BOX([
        BTN("选项 A", "state_a"),
        BTN("选项 B", "state_b"),
        BTN("选项 C", "state_c"),
    ])
```

现在三个按钮会并排显示在同一行。

> 💡 在 GDScript 中，数组元素之间用逗号分隔。最后一个元素后面的逗号是可选的，但保留它可以让后续添加元素更方便。

## 混合文本和按钮

`BOX()` 的强大之处在于可以将 `TXT()` 和 `BTN()` 混在一起：

```gdscript
func main_state():
    TXT("=== 角色状态 ===")
    BOX([
        TXT("生命值: 100/100"),
        TXT("魔力值: 50/50"),
        BTN("使用药水", "use_potion"),
    ])
```

这样文本和按钮会在同一个容器区域内显示，形成一个逻辑上相关的信息组。

## 嵌套容器实现复杂布局

你可以将一个 `BOX()` 嵌套在另一个 `BOX()` 内部，构建更复杂的布局：

```gdscript
func main_state():
    TXT("=== 冒险者公会 ===")

    BOX([
        TXT("欢迎来到冒险者公会！"),
        TXT("请选择你的行动："),

        BOX([
            BTN("接受任务", "accept_quest"),
            BTN("购买装备", "buy_equipment"),
        ]),

        BOX([
            BTN("与同伴交谈", "talk_companion"),
            BTN("休息恢复", "rest"),
        ]),

        BTN("离开公会", "leave_guild"),
    ])
```

运行效果：

- 顶部显示描述性文本
- 中间两个水平排列的按钮组（任务/装备 和 交谈/休息）
- 底部一个独立的"离开"按钮

## Box / HBox / VBox 的区别

ERA-Engine 的布局系统底层支持三种容器类型：

| 容器类型 | 排列方向 | 使用场景 |
|:---------|:---------|:---------|
| **HBox** | 水平（Horizontal） | 将多个按钮或元素并排放在一行 |
| **VBox** | 垂直（Vertical） | 将元素从上到下依次排列 |
| **Box** | 自动判断（预留） | 枚举中定义，尚未实现自动切换 |

> ⚠️ **重要**: `BOX()` 当前**始终创建 HBox（水平布局）**。引擎不会自动检测上下文或智能切换布局类型。VBox 在 `ViewModels` 枚举中已定义，但尚未对接任何 GDScript 命令。如果你需要垂直布局，直接使用多个独立的 `TXT()` / `BTN()` 即可（默认排列方式即为垂直）。

## 完整布局示例

以下是一个游戏主菜单的完整布局示例：

```gdscript
extends Node

func main_state():
    TXT("╔══════════════════╗")
    TXT("║   ERA 传奇      ║")
    TXT("╚══════════════════╝")

    BOX([
        BTN("🎮 开始新游戏", "new_game"),
        BTN("📂 继续游戏", "load_game"),
        BTN("⚙️ 游戏设置", "settings"),
        BTN("🚪 退出游戏", "quit_game"),
    ])

    TXT("v0.1.0 - Powered by ERA-Engine")

func new_game():
    TXT("新游戏即将开始……")
    TXT("请选择你的角色：")
    BOX([
        BTN("战士", "class_warrior"),
        BTN("法师", "class_mage"),
        BTN("游侠", "class_ranger"),
    ])
    BTN("返回", "main_state")

func class_warrior():
    TXT("你选择了战士！")
    TXT("身披重甲，手持利剑，你是战场上的中流砥柱。")
    BTN("开始冒险", "game_start")
    BTN("重新选择", "new_game")

func class_mage():
    TXT("你选择了法师！")
    TXT("精通元素之力，你的法术可以改变战局。")
    BTN("开始冒险", "game_start")
    BTN("重新选择", "new_game")

func class_ranger():
    TXT("你选择了游侠！")
    TXT("擅长弓箭与追踪，森林是你的主场。")
    BTN("开始冒险", "game_start")
    BTN("重新选择", "new_game")

func load_game():
    TXT("载入存档功能：")
    TXT("（请参考进阶教程 - 存档与读档）")
    BTN("返回", "main_state")

func settings():
    TXT("设置功能：")
    TXT("（请在 project.godot 中配置）")
    BTN("返回", "main_state")

func quit_game():
    TXT("确定要退出吗？")
    BOX([
        BTN("确定退出", "confirm_quit"),
        BTN("取消", "main_state"),
    ])

func confirm_quit():
    TXT("再见，冒险者！")
    TXT("期待你的再次归来。")

func game_start():
    TXT("你的冒险即将开始……")
    TXT("（后续章节敬请期待）")
    BTN("返回主菜单", "main_state")
```

运行这个示例，你将看到一个带有主菜单、角色选择和退出确认的完整游戏框架。

---

布局技巧掌握之后，下一步是让你的游戏内容更加丰富——前往 [添加数据](add-data.md)，学习如何使用 CSV 数据文件管理角色、物品等游戏数据。
