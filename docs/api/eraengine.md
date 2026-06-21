# EraEngine

## `DataModel` {#EraEngine-DataModel}

**类型**: class

**继承**: Node


---

## `Logger` {#EraEngine-Logger}

**类型**: class


---

## `Utils` {#EraEngine-Utils}

**类型**: class

---
### 方法

#### `GetOrAddNode<T>`

**声明**

```csharp
public static T GetOrAddNode<T>(Node parent)
```

**返回类型**: `T`

**说明**: 获取并返回父节点下指定类型的子节点；若不存在，则添加并返回一个新节点。
Gets and returns the child node of the specified type under the given parent.
If it does not exist, adds and returns a new child node.


#### `GetFilePaths`

**声明**

```csharp
public static Array<string> GetFilePaths(string path)
```

**返回类型**: `Array<string>`

**说明**: 检索并返回指定路径下所有文件路径。
Retrieves and returns all file paths under the specified path.


#### `GroupPathsByRegex`

**声明**

```csharp
public static Dictionary<string, Array<string>> GroupPathsByRegex(Array<string> paths, String pattern)
```

**返回类型**: `Dictionary<string, Array<string>>`

**说明**: Groups the given paths by the first capture group of the provided regex pattern.

**参数**:
- `paths`: An array of paths to group.
- `pattern`: A regex pattern with at least one capture group.

**返回值**: A dictionary mapping each capture group value to a list of matching paths.


#### `ValidateInheritance`

**声明**

```csharp
public static void ValidateInheritance(GDScript targetScript, GDScript baseScript)
```

**返回类型**: `void`

**说明**: Validates that the specified script either directly or indirectly inherits from the given base script
or any of its ancestor classes in the inheritance chain.

**参数**:
- `targetScript`: The GDScript instance to validate.
- `baseScript`: The base GDScript class that the target script should inherit from (or any of its ancestor classes in the chain).



---

## `ViewModel` {#EraEngine-ViewModel}

**类型**: class

**继承**: Node


---

## `ViewService` {#EraEngine-ViewService}

**类型**: class

**继承**: Node

`ViewService` initializes and manages the views for `GameManager`.


---
