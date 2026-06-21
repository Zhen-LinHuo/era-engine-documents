# 流程控制

FlowService 实现了引擎的 **FSM（有限状态机）** 流程控制。游戏流程被建模为一系列 GDScript 状态函数，每个状态函数输出文本/按钮/盒子等 UI 指令，通过 Godot 信号传递给 ViewService 渲染。

## 核心信号

| 信号 | 发射方 | 接收方 | 参数 | 说明 |
|------|--------|--------|------|------|
| `TextCommanded` | FlowService | ViewService | `text: string` | 命令显示文本 |
| `ButtonCommanded` | FlowService | ViewService | `text: string, state: string` | 命令创建按钮 |
| `BoxCommanded` | FlowService | ViewService | `nodes: Array<Node>` | 命令创建布局容器 |
| `ButtonExecuted` | ViewService | FlowService | `state: string` | 用户点击按钮回调 |

**信号连接**（在 `Controller._Ready()` 中建立）：

- FlowService → ViewService: `TextCommanded`, `ButtonCommanded`, `BoxCommanded`
- ViewService → FlowService: `ButtonExecuted`

数据流向：

- FlowService 发射 → ViewService 处理：`TextCommanded("hello")` → `OnTextCommanded()`, `ButtonCommanded("OK","s")` → `OnButtonCommanded()`, `BoxCommanded([nodes])` → `OnBoxCommanded()`
- ViewService 发射 → FlowService 处理：`ButtonExecuted("next")` → `OnButtonExecuted()`

## 状态机入口与状态切换

```csharp
// 启动：动态加载 main_state.gd 并调用 main_state()
public void CallMainState()
{
    var gdScript = GD.Load<GDScript>("res://Prototype/GdsScript/Flow/main_state.gd");
    MainState = (GodotObject)gdScript.New();
    MainState.Call("main_state");
}

// 按钮回调：根据 state 参数调用对应的状态函数
public void OnButtonExecuted(string state)
{
    MainState.Call(state);
}
```

## 命令方法

FlowService 提供三个命令方法，供 GDScript 流程脚本调用：

| 方法 | 功能 |
|------|------|
| `CommandText(text)` | 发射 `TextCommanded` 信号，返回 CurrentUnit |
| `CommandButton(text, state)` | 发射 `ButtonCommanded` 信号，返回 CurrentUnit |
| `CommandBox(units)` | 发射 `BoxCommanded` 信号，返回 CurrentUnit |

## GDScript Flow 层

`Flow.gd` 基类封装了与 C# 引擎的通信：

```gdscript
class_name Flow extends Object

var flow_service
var model_service

func _init() -> void:
    flow_service = GameManager.Controller.FlowService
    model_service = GameManager.Controller.ModelService

func TXT(text: String) -> Node:
    return flow_service.CommandText(text)

func BTN(text: String, state: String) -> Node:
    return flow_service.CommandButton(text, state)

func BOX(nodes: Array[Node]) -> Node:
    return flow_service.CommandBox(nodes)
```

- `TXT(text)` — 显示文本
- `BTN(text, state)` — 显示按钮，`state` 即点击后执行的状态函数名
- `BOX([nodes])` — 组合多个 UI 单元为水平盒子
- `find(type, name)` — 查询 ModelService 中的数据

## 状态生命周期

1. **用户进入游戏** → `FlowService.CallMainState()` 加载并执行 `main_state()`
2. **`main_state()` 执行** → 输出文本和按钮 → 屏幕渲染完成，等待用户点击
3. **用户点击按钮** → `ViewService.OnButtonPressed()` 禁用按钮，发射 `ButtonExecuted(state)` 信号
4. **FlowService 接收** → `OnButtonExecuted(state)` 调用 `MainState.Call(state)` 切换到下一状态
5. **目标状态函数执行** → 输出新的 UI → 等待下一次点击...

## 关键设计

### 1. 按钮状态即函数名
`BTN(text, state)` 中的 `state` 参数直接对应 MainState 上的方法名。通过 `MainState.Call(state)` 动态调用，实现**字符串驱动的状态路由**。

### 2. 无显式状态栈
当前实现没有状态栈（push/pop），每次按钮触发直接切换到目标状态函数。状态图是隐式的，由 `state` 参数串联。

### 3. 跨语言调用
- GDScript → C#: 通过 `GameManager.Controller.FlowService` 直接访问
- C# → GDScript: 使用 Godot 的 `Object.Call()` 动态方法调用

### 4. Global 全局变量
`Global` 是第二个 Autoload（`global.gd`），存储跨状态的运行时数据（`day`, `action_point`, `gold` 等），状态函数中直接访问无需传递上下文。
