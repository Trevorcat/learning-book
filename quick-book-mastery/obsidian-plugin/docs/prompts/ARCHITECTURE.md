# 架构设计 Prompt

## 问题

需要为 Quick Book Mastery Obsidian 插件设计清晰的架构。

## 背景

这是一个学习辅助插件，核心功能是：
- 管理多本书的学习项目
- 引导用户完成四阶段学习流程
- 提供 AI 对话支持

## 考虑点

### 选项1: 简单直接式
- 所有逻辑集中在 main.ts
- 适用于功能简单的情况
- 难以扩展和维护

### 选项2: 模块化架构
- views/ - UI 视图
- services/ - 业务逻辑
- models/ - 数据模型
- utils/ - 工具函数
- 推荐用于本插件

### 选项3: 特征驱动架构
- features/book/ - 书籍相关
- features/learning/ - 学习流程
- features/ai/ - AI 对话
- 适合大型项目

## 当前倾向

采用选项2（模块化架构），因为：
- 复杂度适中
- Obsidian 插件社区常见模式
- 易于理解和维护

## 请求

请帮我：
1. 确定最终的架构方案
2. 设计核心类和接口
3. 定义模块间依赖关系
4. 创建架构文档

## 参考

- 需求文档：`../context/REQUIREMENTS.md`
- Obsidian API 文档：https://docs.obsidian.md/
