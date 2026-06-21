# API 参考

ERA-Engine 的 API 参考文档通过以下方式**自动生成**：

1. 在源码中使用 **XML 文档注释**标记公共接口。
2. 注释内容通过 `scripts/gen_api_docs.py` 提取并生成 Markdown 文档。
3. 生成的文档整合到本网站的 `API` 章节中。

> 本章内容由自动化工具生成，反映当前 `main` 分支的公共 API。

## 命名空间

| 命名空间 | 类型数 | 说明 |
|:---------|:------|:-----|
| [EraEngine](eraengine.md) | 5 | 引擎根命名空间 — Logger、Utils 工具函数 |
| [EraEngine.Core](eraengine-core.md) | 10 | 引擎核心 — Controller、GameManager、Service、Model 与 View |

## 编写规范

要为引擎贡献代码并生成正确的 API 文档，请遵循以下注释规范：

??? tip "查看 XML 注释写法示例"

    ```csharp
    /// <summary>
    /// 创建一个新的实体实例。
    /// </summary>
    /// <param name="entityName">实体名称。</param>
    /// <param name="type">实体类型，参见 <see cref="EntityType"/>。</param>
    /// <returns>创建的 <see cref="Entity"/> 对象。</returns>
    public Entity CreateEntity(string entityName, EntityType type)
    {
        // ...
    }
    ```

关键标记：

| 标记 | 用途 |
|:-----|:-----|
| `<summary>` | 类型或方法的简要说明 |
| `<param name="...">` | 参数的说明 |
| `<returns>` | 返回值的说明 |
| `<see cref="..."/>` | 引用另一个类型 |
| `<example>` | 使用示例 |
| `<remarks>` | 补充说明 |

## 命名空间说明

| 命名空间 | 说明 |
|:---------|:-----|
| `EraEngine` | 引擎根命名空间，包含核心类型和异常定义 |
| `EraEngine.Core` | 引擎核心，包含 Controller、GameManager、Service 和 Model 基类 |
| `EraEngine.Exceptions` | 引擎自定义异常 |
| `EraEngine.ECS` | ECS（实体-组件-系统）框架核心 |
| `EraEngine.Services` | 引擎级服务（视图、存档、输入） |
| `EraEngine.Storage` | 数据持久化与序列化 |
| `EraEngine.UI` | 用户界面组件与布局系统 |
| `EraEngine.Util` | 工具函数与扩展方法 |

> 提示：文档自动生成，与主仓库 `main` 分支同步更新。
