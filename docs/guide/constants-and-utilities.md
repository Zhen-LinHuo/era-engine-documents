# 常量与工具

ERA-Engine 将系统常量集中定义在 `Constants/` 目录下，通用工具函数封装在 `Utils/` 目录中。这些模块被所有服务层共享，是引擎的基础设施。

## Constants 命名空间

### Constants.cs — 核心常量

```csharp
public static class Constants
{
    // TODO: 通过外部 Config 文件修改参数
    public const string DataFolderName = "Data";
    public const string DataFileName = "data";
    public const string DataBaseName = "Data";
}
```

| 常量 | 值 | 用途 |
|------|-----|------|
| `DataFolderName` | `"Data"` | 数据目录名称，拼接路径用 |
| `DataFileName` | `"data"` | data.gd 的文件名（不含扩展名） |
| `DataBaseName` | `"Data"` | Data 基类的 `class_name`，用于继承验证 |

> **TODO**: 计划改为从外部配置文件读取，当前硬编码。

### FileExtensions.cs — 文件扩展名

```csharp
public static class FileExtensions
{
    public static readonly string GdsScript = "gd";
    public static readonly string CommaSeparatedValues = "csv";
    public static readonly string ExtensibleMarkupLanguage = "xml";
    public static readonly string JavaScriptObjectNotation = "json";
}
```

### FileRegex.cs — 文件路径正则模式

```csharp
public static class FileRegex
{
    public const string DataBasePattern = @"^.*[\/\\](data\.gd)$";
    public const string DataModelPattern = @"^(?!.*[\/\\]data\.gd$).*\.gd$";
    public const string ExtensionPattern = @"\.(\w+)$";
    public const string FilenamePattern = @"([^\/\\]+)\..+$";

    public static string GetDataSourcePattern(string extension) =>
        $@".*\.{extension}$";

    public static string GetFilenamePattern(string extension) =>
        $@"([^\/\\]+)\.{extension}(?:\.{extension})?$";
}
```

| 模式 | 用途 | 示例匹配 |
|------|------|---------|
| `ExtensionPattern` | 捕获文件扩展名 | `character.gd` → `gd` |
| `FilenamePattern` | 捕获文件名（不含路径） | `Data/character.gd` → `character` |
| `DataBasePattern` | 精确匹配 data.gd | `Data/data.gd` ✓ |
| `DataModelPattern` | 匹配 .gd 但排除 data.gd | `Data/character.gd` ✓ |

### FileCategory.cs — 文件分类枚举

```csharp
public enum FileCategory
{
    [Description("Base Data File for data.gd ignore cases")]
    DataBase,
    [Description("Godot Script with .gd")]
    DataModel,
    [Description("")]
    DataSource,
    FlowBase,
    FlowScript,
    FlowSource,
}
```

### ViewModels.cs — UI 组件枚举

```csharp
public enum ViewModels
{
    Unit,
    TextUnit,
    ButtonUnit,
    Box,
    HBox,
    VBox,
    Suite,
    View,
    Controls,
}
```

ViewService 使用此枚举值作为 `FindChild()` 的参数，引用 ViewModel 模板中的预制节点。

### DataFunctionName.cs — 数据方法名称常量

```csharp
public static class DataFunctionName
{
    // 在 data 初始化时，检查这些方法是否仍然存在于 Data 基类
    public const string Csv = "_csv";
    public const string Uid = "_uid";
    public const string SetUuid = "set_uuid";
}
```

这些常量定义了 Data 基类必须实现的方法签名。DataService 和 ModelService 通过 `resource.HasMethod()` 和 `resource.Call()` 使用这些名称进行动态调用。

### FlowFunctionName.cs — 流程方法名称常量

```csharp
public static class FlowFunctionName
{
    // 预留，当前为空实现
}
```

### LogCategory.cs — 日志分类枚举

```csharp
public enum LogCategory
{
    Information,
    Warning,
    Error,
}
```

## Utils 工具类

`Utils` 是一个静态工具类，为引擎提供通用的节点操作、文件系统查询和路径匹配功能。

### GetOrAddNode — 获取或创建子节点

```csharp
// 按类型名查找/创建
public static T GetOrAddNode<T>(Node parent) where T : Node, new()
{
    T child = parent.GetNodeOrNull<T>(typeof(T).Name);
    if (child is not null) return child;

    child = new T { Name = typeof(T).Name };
    parent.AddChild(child);
    child.Owner = parent;
    return child;
}

// 按指定名称查找/创建
public static T GetOrAddNode<T>(Node parent, String name) where T : Node, new()
{
    T child = parent.GetNodeOrNull<T>(name);
    if (child is not null) return child;

    child = new T { Name = name };
    parent.AddChild(child);
    child.Owner = parent;
    return child;
}
```

**使用场景**: 所有 Service 子节点的延迟初始化。如果节点已存在（场景中预配置），直接返回；否则创建新实例。

### AddAndOwnChild — 安全添加子节点

```csharp
public static Node AddAndOwnChild(Node parent, Node child)
{
    parent.AddChild(child);
    child.Owner = parent.Owner ?? parent;
    return child;
}
```

与 `AddChild` 的区别：确保 `child.Owner` 设置正确（尤其在使用 `Duplicate()` 复制后，副本的 Owner 可能为空）。

### GetFilePaths — 递归获取文件路径

```csharp
public static Array<string> GetFilePaths(string path)
{
    Array<string> paths = new Array<string>();
    using DirAccess dirAccess = DirAccess.Open(path);

    dirAccess.ListDirBegin();
    string name = dirAccess.GetNext();
    while (name != "")
    {
        if (dirAccess.CurrentIsDir())
            paths.AddRange(GetFilePaths(dirAccess.GetCurrentDir() + "/" + name));
        else
            paths.Add(dirAccess.GetCurrentDir() + "/" + name);
        name = dirAccess.GetNext();
    }
    dirAccess.ListDirEnd();
    return paths;
}
```

使用 Godot 的 `DirAccess` API 递归遍历目录，返回所有文件的完整路径列表。路径分隔符使用 `/`。

### GroupPathsByRegex — 正则路径分组

有两个重载：

**重载 1 — 按捕获组分组的简单版**:

```csharp
public static Dictionary<string, Array<string>> GroupPathsByRegex(
    Array<string> paths, String pattern)
{
    var dict = new Dictionary<string, Array<string>>();
    foreach (var path in paths)
    {
        var match = Regex.Match(path, pattern);
        var key = match.Success ? match.Groups[1].Value : "<unmatched>";
        // 将 path 加入 dict[key]
    }
    return dict;
}
```

**重载 2 — 多模式匹配版**（使用 `ref` 修改原数组）:

```csharp
public static Dictionary<string, Array<string>> GroupPathsByRegex(
    ref Array<string> paths,
    Dictionary<string, Array<string>> patternMap)
{
    // 遍历每个 pattern → 匹配的 path 从 paths 中移除并加入结果
}
```

### IsInherited — 继承关系验证

```csharp
public static bool IsInherited(GDScript targetScript, string baseScript)
{
    var currentScript = targetScript.GetBaseScript();
    while (currentScript != null)
    {
        if (currentScript.GetGlobalName() == baseScript) return true;
        currentScript = currentScript.GetBaseScript();
    }
    return false;
}
```

检查目标脚本的继承链中是否存在指定 `class_name` 的基类。支持**间接继承**：`SuperCharacter → Character → Data` 中，`IsInherited(SuperCharacter_script, "Data")` 返回 `true`。

### ValidateInheritance — 继承验证（异常版本）

```csharp
public static void ValidateInheritance(GDScript targetScript, GDScript baseScript)
{
    // 遍历继承链，未找到则抛出 ScriptInheritanceException
}
```

与 `IsInherited` 功能相同，但未找到时抛出 `ScriptInheritanceException` 而非返回 `false`。

### CategorizeFilesByExtensions — 按扩展名分类

```csharp
public static Dictionary<string, Array<string>> CategorizeFilesByExtensions(
    Array<string> pathList)
{
    // 用文件名（不含扩展名）作为 key 分组
    // 同一文件名的 .gd 和 .csv 归入同一组
}
```

## Logger 日志系统

```csharp
public partial class Logger
{
    private readonly string _className;
    private string _filter;

    public Logger(string className)
    {
        _className = className;
        _filter = "";  // 过滤器，设为类名可屏蔽该类的日志
    }
}
```

### 日志方法

```csharp
// 信息日志
public void Info(string message, [CallerLineNumber] int line = -1)
    => Log("INFO", LogCategory.Information, message, line);

// 警告日志（黄色输出）
public void Warn(string message, [CallerLineNumber] int line = -1)
    => Log("WARNING", LogCategory.Warning, message, line);

// 错误日志
public void Error(string message, [CallerLineNumber] int line = -1)
    => Log("ERROR", LogCategory.Error, message, line);

// 带异常的错误日志
public void Error(string message, Exception exception, [CallerLineNumber] int line = -1)
    => Log("ERROR", LogCategory.Error, $"{message}\n{exception}", line);
```

### 输出格式

```
[LEVEL] ClassName:line N - message
```

按日志类别输出：
- **Information** → `GD.Print()` 普通输出
- **Warning** → `GD.PrintRich()` 黄色着色输出
- **Error** → `GD.PrintErr()` 错误流输出

### 使用示例

```csharp
// 每个类创建自己的 Logger 实例
private static Logger Logger { get; } = new(nameof(GameManager));

Logger.Info($"Starting to initialize {nameof(ModelService)}.");
Logger.Warn($"{filename} has no csv");
Logger.Error($"Failed to initialize {nameof(DataService)} - {exception}");
```

### 过时 API

旧版 `Info(params string[])`、`Warn(params string[])`、`Error(params string[])` 已标记 `[Obsolete]`，内部仍可用但推荐使用新版单字符串方法。

## Exceptions 异常类

### ScriptInheritanceException

```csharp
public class ScriptInheritanceException : Exception
{
    public ScriptInheritanceException() { }
    public ScriptInheritanceException(string message) : base(message) { }
    public ScriptInheritanceException(string message, Exception innerException)
        : base(message, innerException) { }
}
```

当 GDScript 数据文件未继承指定的基类时抛出。由 `Utils.ValidateInheritance()` 使用。

## 工具链调用关系

- **DataService** 使用：
    - `Utils.GetFilePaths(path)` — 扫描目录
    - `Utils.GroupPathsByRegex(paths, pattern)` — 正则分组
    - `Utils.IsInherited(script, "Data")` — 继承验证
    - `Utils.GroupPathsByRegex(ref paths, map)` — 多模式分组
- **GameManager / Controller / ViewService** 使用：
    - `Utils.GetOrAddNode<T>(parent)` — 延迟创建子节点
    - `Utils.AddAndOwnChild(parent, child)` — 安全添加子节点
- **所有模块** 使用：
    - `Logger.Info/Warn/Error` — 日志记录
