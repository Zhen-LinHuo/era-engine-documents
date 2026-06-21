# 添加数据

文本和按钮让游戏有了骨架，而数据赋予了游戏血肉。在本教程中，你将学习如何使用数据文件来管理角色、物品、对话等内容，并在状态函数中访问这些数据。

## 什么是数据文件？

在 ERA-Engine 中，游戏数据（角色属性、物品信息、对话文本等）存储在**数据文件**中（如 CSV 格式），放在 `Prototype/Data/` 目录下。

这样做的优势：

- **数据与逻辑分离**：写作者可以编辑数据文件来修改游戏内容，无需接触代码
- **便于批量编辑**：数据文件可以用 Excel、Google Sheets 等工具编辑
- **引擎自动加载**：ERA-Engine 启动时自动扫描 `Data/` 目录，加载所有数据文件

## 创建你的第一个数据文件

### 第一步：创建 Data 目录

在 Godot 的 **FileSystem** 面板中：

1. 右键点击 `Prototype` 目录
2. 选择 **新建文件夹（New Folder）**
3. 命名为 `Data`

> 💡 如果 `Data` 目录已经存在，跳过此步骤。

### 第二步：创建 Character.csv

在 `Prototype/Data/` 目录中创建一个名为 `Character.csv` 的文件（可以使用 Godot 内置编辑器或任意外部文本编辑器），内容如下：

```csv
id,name,hp,max_hp,mp,max_mp,description
warrior,战士,100,100,20,20,身披重甲的近战专家
mage,法师,60,60,100,100,精通元素魔法的施法者
ranger,游侠,80,80,50,50,擅长弓箭和追踪的森林行者
healer,祭司,70,70,80,80,能够治愈伤者的神圣使者
```

**CSV 结构说明**：

- **第一行**（表头）：定义了每一列的数据名称
- **后续行**（数据行）：每一行代表一个角色的完整数据
- 列之间用英文逗号 `,` 分隔

### 第三步：创建数据模型脚本

在 `Prototype/GdsScript/` 目录下创建一个新文件 `character.gd`：

```gdscript
extends "res://Engine/Data.gd"

# 这个脚本让 ERA-Engine 知道如何加载 Character.csv
# 字段名会自动映射到 CSV 的列名
```

> ⚠️ `extends "res://Engine/Data.gd"` 的路径需要根据你的项目结构调整。如果引擎的 `Data.gd` 在不同位置，请相应修改。

### 字段自动映射

当你创建好数据文件后，ERA-Engine 会将 CSV 的列自动映射为可访问的**属性（property）**：

| CSV 列名 | 角色属性 | 访问方式 |
|:---------|:---------|:---------|
| `id` | 唯一标识符 | `character.id` |
| `name` | 角色名称 | `character.name` |
| `hp` | 生命值 | `character.hp` |
| `max_hp` | 最大生命值 | `character.max_hp` |
| `mp` | 魔力值 | `character.mp` |
| `max_mp` | 最大魔力值 | `character.max_mp` |
| `description` | 描述文本 | `character.description` |

默认情况下，CSV 中的值都是**字符串类型**。如果需要进行数值计算（如扣减 HP），你需要在 GDScript 中做类型转换：

```gdscript
var current_hp = int(character.hp)
var new_hp = current_hp - 10
```

## 在状态函数中访问数据

以下是一个完整的示例，展示如何在状态函数中使用数据：

```gdscript
extends Node

func main_state():
    TXT("=== 角色列表 ===")
    TXT("请选择你要查看的角色：")

    # 遍历所有角色数据，为每个角色创建一个按钮
    # DataService 提供了角色数据的访问
    for character in Data.Character.all():
        var label = character.name + " (HP: " + character.hp + "/" + character.max_hp + ")"
        BTN(label, "character_detail")

    BTN("返回", "main_state")

func character_detail():
    TXT("角色详情页面（可在后续扩展）")
    BTN("返回", "main_state")
```

> 💡 上述代码中的 `Data.Character.all()` 是示意性的。实际项目中，数据访问的具体 API 可能有所不同，请参考引擎的实际 API 文档。

## 创建更多数据文件

掌握基本方法后，你可以为不同的数据类型创建更多的 CSV 文件：

### 物品数据（Item.csv）

```csv
id,name,type,price,effect,description
potion,回复药水,consumable,50,restore_hp_30,恢复30点生命值
elixir,魔力药水,consumable,80,restore_mp_50,恢复50点魔力值
sword,铁剑,weapon,200,atk_15,攻击力+15的基础武器
shield,木盾,armor,150,def_10,防御力+10的轻便盾牌
```

### 对话数据（Dialogue.csv）

```csv
id,character_id,stage,text
intro_warrior,warrior,greeting,"你好，旅行者。我叫亚瑟，曾是王国的骑士。"
intro_mage,mage,greeting,"啊，又一位对魔法感兴趣的人？我是艾琳。"
intro_ranger,ranger,greeting,"嘘——小声点。我在追踪一头鹿。"
```

### 场景数据（Scene.csv）

```csv
id,name,description,connections
crossroad,十字路口,你站在一个分叉路口的中央,crossroad_castle|crossroad_forest|crossroad_river
castle,古老城堡,一座宏伟的中世纪城堡矗立在眼前,crossroad
forest,幽暗森林,高大的树木遮蔽了阳光,crossroad
river,清澈河流,一条蜿蜒的河流静静流淌,crossroad
```

## 数据文件最佳实践

- **使用有意义的列名**：列名应该简洁但具有描述性（如用 `max_hp` 而不是 `m`）
- **保持数据一致**：同一个 CSV 文件中，确保每行的列数一致
- **避免在文本中使用逗号**：如果某个字段内容必须包含逗号，将该字段用双引号 `"` 包裹起来
- **使用英文 ID**：`id` 列建议使用英文（便于代码引用），`name` 列可以使用中文（用于显示）
- **备份重要数据**：CSV 文件本质上是纯文本，建议使用版本控制系统（Git）管理

## 常见问题

**Q: 如何修改已加载的数据？**
A: 数据文件在游戏启动时加载到内存中。在游戏运行时修改的数据（如角色的当前 HP）不会写回 CSV 文件。持久化保存需要使用存档系统（后续教程会涉及）。

**Q: CSV 的编码格式有要求吗？**
A: 建议使用 **UTF-8 with BOM** 或 **UTF-8 without BOM** 编码，以确保中文等非 ASCII 字符正确显示。大多数现代文本编辑器默认使用 UTF-8。

**Q: 可以添加新列而不破坏现有代码吗？**
A: 可以。在 CSV 末尾追加新列是安全的。但删除或重命名现有列可能会破坏使用这些列的代码。

---

数据让游戏内容可以无限扩展。现在是时候将所有知识整合起来了——前往 [完整示例](complete-example.md)，完成一个包含标题画面、角色选择和主循环的迷你游戏。
