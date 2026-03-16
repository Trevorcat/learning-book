# Quick Book Mastery - Obsidian Plugin Development

## 项目背景

这是一个 Obsidian 插件项目，将 "Quick Book Mastery" 学习系统从 Claude Skill 迁移到 Obsidian 平台。

## 核心理念

**Quick Book Mastery** 是一个对话式学习引导系统，帮助用户通过四阶段流程快速掌握一本书：
1. 准备与目标设定（5-10分钟）
2. 概览与框架构建（10-15分钟）
3. 深入与理解（15-30分钟）- 费曼法 + 主动回忆
4. 巩固与应用（5-10分钟）- 间隔重复 + 行动计划

支持两种模式：
- **快速模式**：30-60分钟掌握框架
- **伴读模式**：细粒度讲解，系统学习

## 当前状态

- [x] 项目结构已搭建（TypeScript + esbuild）
- [x] 基础配置文件已创建
- [ ] 核心插件代码待开发
- [ ] AI 对话面板待实现
- [ ] 学习模板系统待实现
- [ ] 进度跟踪待实现

## 技术栈

- TypeScript
- Obsidian API
- esbuild (构建)

## 参考文档

- 完整项目背景：`docs/context/PROJECT_OVERVIEW.md`
- 需求文档：`docs/context/REQUIREMENTS.md`
- 原 Skill 文档：`../../SKILL.md` (父目录)

## 开发任务

### 当前阶段
根据需求文档实现 MVP 功能：
1. 书籍管理（创建、列表、进度）
2. 学习模式选择
3. 四阶段学习模板
4. AI 对话面板（Claude API）

### 集成点
- Excalidraw 插件（可选）：框架图绘制
- Spaced Repetition 插件（可选）：间隔重复

## 当前请求

请帮我实现 [具体功能/模块]。
