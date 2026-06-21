# 进阶教程

欢迎来到 ERA-Engine 进阶教程！本章节面向有一定开发经验的用户，深入探讨引擎的高级功能和扩展机制。

## 面向读者

进阶教程假设你已经：

- 完成了[入门教程](../tutorial/index.md)的全部步骤
- 阅读了[开发指南](../guide/index.md)中的核心子系统介绍
- 具备一定的 C# 和 GDScript 编程经验
- 理解 ERA-Engine 的 FSM + MVC 架构

如果你尚未满足以上条件，建议先回到基础章节学习。

## 章节概览

| 章节 | 内容 | 关键知识点 |
|:-----|:-----|:----------|
| [自定义 UI 组件](custom-ui-components.md) | 扩展 ViewService 的工厂模式创建自定义 Unit 类型 | ViewService、UnitFactory、UnitContainer 继承 |
| [存档与读档](save-and-load.md) | 基于 ModelService 的序列化与反序列化机制 | ModelService.Save()、Resource、UID |
| [动画与特效](animations-and-effects.md) | 使用 Godot AnimationPlayer 和 Tween 添加视觉表现 | AnimationPlayer、Tween、信号联动 |
| [口上文件格式](kojo-format.md) | Kojo（口上）对话文件的格式规范与编写指南 | CSV 口上表、代码与口上分离 |
| [调试与日志](debugging-and-logging.md) | Logger 系统的使用、日志级别与调试模式 | Logger、LogCategory、DEBUG 模式 |

## 学习路径建议

![进阶学习路径](../Images/learning-path.svg)

建议按照以下顺序学习：

1. **从「自定义 UI 组件」开始** — 理解 ViewService 的扩展机制是后续自定义开发的基础
2. **并行学习「动画与特效」和「口上文件格式」** — 这两者相对独立，可同时进行
3. **再学习「存档与读档」** — 结合前面掌握的 UI 和数据知识
4. **最后学习「调试与日志」** — 这是贯穿所有开发流程的辅助技能
