# 开发指南

本章节深入解析 ERA-Engine (Godot) 的核心架构与实现细节，面向需要理解引擎内部机制、进行二次开发或扩展功能的开发者。

## 章节导航

| 章节 | 说明 |
|------|------|
| [架构总览](./architecture-overview.md) | MVC 三层架构图、服务职责表、数据流全景 |
| [启动流程](./startup-lifecycle.md) | `GameManager._Ready()` 逐步执行流程、Autoload 注册、错误处理 |
| [数据系统](./data-system.md) | 文件扫描 → 正则分类 → 继承验证 → 拓扑排序 → CSV 工厂 → 持久存储 |
| [流程控制](./flow-system.md) | FlowService 信号机制、状态函数生命周期、`main_state.gd` 动态加载 |
| [视图系统](./view-system.md) | ViewService 工厂模式、Unit/Suite/Box 复制模板、信号处理器 |
| [模型层](./model-layer.md) | Model 容器、DataModel 资源字典、ViewModel 组件（ButtonUnit / MainContent / UnitContainer） |
| [常量与工具](./constants-and-utilities.md) | Constants 命名空间、Utils 工具函数、Logger 日志系统 |

## 前置知识

阅读本指南前，建议先了解：

- **Godot 引擎基础** — 节点系统、场景、信号机制
- **C# 与 GDScript 互操作** — ERA-Engine 的核心逻辑使用 C#，数据定义和流程脚本使用 GDScript
- **MVC 模式** — 引擎整体采用 Model-View-Controller 架构组织代码

## 引擎概览

ERA-Engine (Godot) 是一个基于 Godot 引擎的文本驱动游戏框架。其核心设计遵循 MVC 模式，使用 C# 实现引擎底层逻辑（控制器、服务、数据管道），GDScript 定义游戏数据（`Data` 基类及其子类）与流程脚本（`Flow` 基类及其子类）。

### 核心组件关系

- **GameManager**（Autoload 单例）— 全局指挥者，协调所有初始化流程
- **Controller** — 聚合四大服务（ModelService / ViewService / DataService / FlowService），建立信号连接
- **Model** — 持有 DataModel（运行时数据）和 ViewModel（UI 模板）
- **View** — UI 场景实例，通过 ViewService 工厂动态生成界面元素

### 技术栈

- **语言**: C# (Godot .NET) + GDScript
- **引擎版本**: Godot
- **跨语言通信**: Godot 信号 + 方法调用（`Object.Call()`）
