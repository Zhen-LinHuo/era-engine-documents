*************************
ERA Engine (Godot) 的设计
*************************

这一章对 ERA Engine (Godot) 的设计进行概述，包其架构和设计纲领。

========
设计模式
========

.. admonition:: 有限状态机 (FSM)
    :collapsible:
    :name: Introduction.DesignIntro.FSM

    有限状态机 ( ``FSM``` ) 是一种包含有限种状态的系统模型，为计算机程序和顺序逻辑回路设计。程序所有的数据、状态和其他信息都被视为 ``状态`` ，在任一时间，系统只会存在有限种状态。

    .. image:: /images/FSM.svg
        :align: center

    ERA Engine (Godot) 内置了这种 ``FSM`` 模式，也可称之为 ``FSM 模式``，作为 ERA 游戏和其他基于文字的游戏的全新编程模式。

    在 ERA Engine 中，任何状态都可以被视为有限状态机中的 ``状态`` ，因而任何状态的变化（e.g. UI 的改变，游戏进度的推进，点击了某个按钮，etc.）都可以被视为状态的 ``转置`` 。因此，实际上整个游戏就可以理解为在不同 ``状态`` 之间进行 ``转置`` 的过程。

.. admonition:: MVC 模式
    :collapsible:
    :name: Introduction.DesignIntro.MVC

    MVC 模式是一种设计模式，用于将应用程序分为三个部分：模型 (Model)，视图 (View) 和控制器 (Controller)。

    .. figure:: /images/MVC.svg
        :align: center

        MVC 模式的结构和逻辑

    一般而言， ``View`` 是用户能看到的界面， ``Model`` 是数据库和数据模型，而 ``Controller`` 则是程序的运作逻辑。在 ``View`` 的状态更新时， ``Controller`` 就会管控运行逻辑，查询 ``Model`` 中的数据，进行计算和处理，最终将更新信息返回给 ``View`` 。使用这样的设计模式有助于令程序结构清晰、运行可靠。

========
设计架构
========

--------
系统架构
--------

总体来看，要在 ERA Engine 中实现一个游戏，你主要需要关注这两个部分：

* ``状态``：你对界面及其内容的布置
* ``数据``：所有的数据文件，包括 ``角色`` ， ``口上`` ， ``物品`` 等。

基于这两部分和 :ref: `Introduction.DesignIntro.FSM` ，你可以自定义你的每一个 ``UI 单元`` 背后的逻辑，最终完成整个游戏的运作逻辑。

.. hint::
    想要快速开始制作你的游戏？查看 :ref: `Tutorial` 章节！