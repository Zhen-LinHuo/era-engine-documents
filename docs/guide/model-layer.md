# 模型层

Model 层是引擎的**数据容器**，分为两个子系统：**DataModel**（运行时业务数据）和 **ViewModel**（UI 模板定义）。

## Model — 顶层容器

Model 在 `_Ready()` 中执行两件事：
1. 加载 `ViewModel.tscn` 场景，提取 UI 模板引用（Unit/Suite/Box/View）
2. 创建 `DataModel` 根节点，为后续数据存储准备

Model 作为 `GameManager` 的直接子节点，持有两棵子树：

- **ViewModel** (Node) — 来自 ViewModel.tscn 场景
    - Unit — UI 单元模板 (TextUnit, ButtonUnit)
    - Suite — 套件模板
    - Box — 盒子模板 (HBox, VBox)
    - View — 主视图实例（被 Duplicate 到 GameManager）
- **DataModel** (Node) — 运行时数据根
    - Character → Resources: "紫三思", "紫二思"
    - Item → Resources: "长剑"
    - Attributes → Resources: "勇猛"

## DataModel — 数据存储单元

```csharp
[GlobalClass]
public partial class DataModel : Node
{
    [Export] public Dictionary<String, Resource> Resources { get; set; }
}
```

每个数据类别对应一个 `DataModel` 节点（节点名 = `class_name`），内部使用 `Dictionary<String, Resource>` 存储：

- **Key**: GDScript `_uid()` 返回值（如角色名 "紫三思"）
- **Value**: Godot Resource 对象（GDScript 数据类实例）

## ModelService API

ModelService 是 Model 层的统一访问接口，所有数据操作通过它完成：

| 方法 | 签名 | 说明 |
|------|------|------|
| `Save` | `Save(Resource) → Resource` | 按继承链最具体基类名创建/查找 DataModel 节点，调用 `_uid()` 获取 key 存入 Resources 字典 |
| `Find` | `Find(globalName, uid) → Resource` | 按全局类名 + uid 查找数据实例 |
| `Find` | `Find(parent, uid) → Node` | 在指定父节点下按名称查找子节点 |
| `Find` | `Find(query) → Node` | 按点号分隔路径查找（如 `"DataModel.Character"`） |
| `Get` | `Get(path) → Node` | `Model.GetNode(path)` 的代理 |
| `Get` | `Get(idx) → Node` | `Model.GetChild(idx)` 的代理 |
| `Remove` | `Remove(idx)` | 按索引移除并释放子节点 |
| `Delete` | `Delete(uid)` | 按名称查找并释放子节点 |

> 数据查找形成了**单一数据源（Single Source of Truth）**：所有数据实例存储在 Model.DataModel 中，任何地方都通过 `ModelService.Find()` 获取引用。

## ViewModel 组件

ViewModel 相关的 C# 类均为轻量包装：

- **ViewModel.cs** — 空 `Node` 类，仅作为 ViewModel.tscn 的根节点类型标记
- **UnitContainer.cs** — 继承 `PanelContainer`，导出 `Element` 属性指向第一个子节点（实际内容：Label 或 Button），是所有 UI 单元的包装器
- **ButtonUnit.cs** — 直接继承 `UnitContainer`，无额外逻辑。在 ViewModel.tscn 模板中，其第一个子节点预置为 Button 控件
- **MainContent.cs** — 继承 `ScrollContainer`，监听垂直滚动条变化，自动滚动到底部（模拟控制台滚动行为）

## Model 初始化流程

1. `GameManager._Ready()` 开始
2. 创建/获取 Model 节点：`Model ??= Utils.GetOrAddNode<Model>(this)`
3. `Model._Ready()` 执行：
    - 加载 ViewModel：`ViewModel = Load("ViewModel.tscn").Instantiate()` → ViewModel 子树就绪（Unit/Suite/Box/View 模板）
    - 创建 DataModel：`DataModel = GetOrAddNode<DataModel>(this)`
4. `Controller.ModelService._Init(Model)` → ModelService 持有 Model 引用

## 跨模型引用

GDScript 数据类中的 `@export var weapon: Item` 声明跨模型依赖。DataService 在拓扑排序时通过反射检测这些引用（`type == Variant.Type.Object`），确保被依赖者先加载。

在 GDScript 中，通过基类方法获取引用：

```gdscript
func get_object_by_name(global_name, object_name) -> Object:
    return GameManager.Controller.ModelService.Find(global_name, object_name)
```
