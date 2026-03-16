# Quick Book Mastery - Obsidian Plugin

## 🚀 快速开始

### 方式1：在当前目录重开 Claude Code

```bash
cd ~/.claude/skills/learning-book/quick-book-mastery/obsidian-plugin
claude
```

然后在 Claude Code 中加载 prompt：

```
@docs/prompts/PROMPT.md
```

### 方式2：使用特定功能的 prompt

```
@docs/prompts/MVP.md          # MVP 开发
@docs/prompts/ARCHITECTURE.md  # 架构设计
@docs/prompts/FEATURE.md       # 添加新功能
```

## 📁 项目结构

```
obsidian-plugin/
├── docs/
│   ├── context/
│   │   ├── PROJECT_OVERVIEW.md  # 项目背景
│   │   └── REQUIREMENTS.md      # 需求文档
│   └── prompts/
│       ├── PROMPT.md            # 通用开发 prompt
│       ├── MVP.md               # MVP 开发 prompt
│       ├── ARCHITECTURE.md      # 架构设计 prompt
│       └── FEATURE.md           # 功能开发 prompt
├── src/                         # 源代码目录（待创建）
├── main.ts                      # 插件入口（待创建）
├── manifest.json                # 插件清单
├── package.json                 # 依赖配置
├── tsconfig.json                # TypeScript 配置
└── esbuild.config.mjs           # 构建配置
```

## 📖 参考文档

### 项目文档
- `docs/context/PROJECT_OVERVIEW.md` - 项目背景、核心概念
- `docs/context/REQUIREMENTS.md` - 功能需求、技术需求

### 原 Skill 文档
- `../SKILL.md` - 完整的学习方法论
- `../INSTALL.md` - OCR 等工具安装指南

### 外部资源
- [Obsidian API 文档](https://docs.obsidian.md/)
- [Obsidian 插件示例](https://github.com/obsidianmd/obsidian-sample-plugin)

## 🛠️ 开发命令

```bash
# 安装依赖
npm install

# 开发模式（自动重建）
npm run dev

# 构建生产版本
npm run build
```

## 📝 开发工作流

1. **首次开发**：加载 `docs/prompts/MVP.md`，实现基础功能
2. **架构设计**：加载 `docs/prompts/ARCHITECTURE.md`，设计代码结构
3. **添加功能**：加载 `docs/prompts/FEATURE.md`，填写具体需求
4. **通用开发**：加载 `docs/prompts/PROMPT.md`，描述当前任务

## 🎯 当前状态

- [x] 项目结构搭建
- [x] 基础配置完成
- [x] 文档准备完成
- [ ] 核心代码开发（下一步）

## 💡 提示

- 所有 prompt 文件都在 `docs/prompts/` 目录
- 使用 `@` 符号在 Claude Code 中加载 prompt
- 上下文信息在 `docs/context/` 目录
