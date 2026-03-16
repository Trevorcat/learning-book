# Quick Book Mastery - Obsidian Plugin 设计文档

**日期**: 2025-03-16
**版本**: 0.1.0

## 1. 项目概述

将 Quick Book Mastery 学习系统从 Claude Skill 迁移为 Obsidian 插件，提供本地化的学习管理和 AI 对话支持。

## 2. 架构设计

### 2.1 模块结构

```
src/
├── main.ts                    # 插件入口类
├── types/
│   └── index.ts              # TypeScript 类型定义
├── models/
│   └── Book.ts               # 书籍数据模型
├── views/
│   └── LearningView.ts       # 主侧边栏视图
├── services/
│   ├── BookService.ts        # 书籍管理服务
│   └── AIService.ts          # AI 对话服务
├── templates/
│   └── stages.ts             # 四阶段学习模板
├── modals/
│   └── ModeSelectModal.ts    # 模式选择弹窗
└── utils/
    └── storage.ts            # 本地存储工具
```

### 2.2 核心类设计

#### QuickBookMasteryPlugin (main.ts)
- 继承 `Plugin` 类
- 生命周期：onload() / onunload()
- 注册：命令、视图、设置

#### LearningView (views/LearningView.ts)
- 继承 `ItemView`
- 侧边栏主界面
- 包含：书籍列表、进度、AI 对话

#### BookService (services/BookService.ts)
- 书籍 CRUD 操作
- 进度管理
- 模板生成

#### AIService (services/AIService.ts)
- Claude API 调用
- 对话历史管理
- 提示词构建

### 2.3 数据模型

```typescript
interface Book {
  id: string;
  title: string;
  author?: string;
  mode: LearningMode;  // 'fast' | 'companion'
  currentStage: Stage; // 1 | 2 | 3 | 4
  progress: number;    // 0-100
  profile?: LearningProfile;
  createdAt: string;
  updatedAt: string;
}

type LearningMode = 'fast' | 'companion';
type Stage = 1 | 2 | 3 | 4;

interface LearningProfile {
  goal: string;
  timeBudget: string;
  priorKnowledge: string;
  notes?: string;
}
```

## 3. 界面设计

### 3.1 侧边栏主界面

```
┌─────────────────────────────────────────────┐
│ 📚 Quick Book Mastery              [设置]   │
├─────────────────────────────────────────────┤
│ 我的书籍                                    │
│ ├─ 📖 Python源码剖析     [████░░] 60%      │
│ │   阶段3/4: 深入与理解                     │
│ ├─ 📘 深入理解计算机系统   [██░░░░] 30%      │
│ │   阶段2/4: 概览与框架                     │
│ └─ ➕ 开始新书...                          │
├─────────────────────────────────────────────┤
│ 🤖 AI 助手                                  │
│ ─────────────────────────────────────       │
│ AI: 我们来理解"引用计数"机制...             │
│                                             │
│ [用户输入...                    ] [发送]    │
└─────────────────────────────────────────────┘
```

### 3.2 模式选择弹窗

- 快速模式卡片（推荐标签）
- 伴读模式卡片
- 模式对比说明

## 4. 功能清单

### MVP (v0.1.0)

- [ ] 项目基础架构
- [ ] 书籍 CRUD
- [ ] 模式选择
- [ ] 四阶段模板生成
- [ ] AI 对话面板（Claude API）

### V2

- [ ] Excalidraw 集成
- [ ] Spaced Repetition 集成
- [ ] 统计面板
- [ ] 语音输入支持

## 5. 技术决策

| 决策 | 选择 | 理由 |
|-----|------|------|
| 语言 | TypeScript | 类型安全，Obsidian 官方支持 |
| UI 框架 | 原生 Obsidian | 无需额外依赖，符合平台风格 |
| AI 服务 | Claude API | 原 Skill 使用，用户熟悉 |
| 存储 | Markdown 文件 | 本地优先，可移植性强 |

## 6. 开发计划

### Phase 1: 基础架构 (1-2 天)
- [ ] 创建目录结构
- [ ] 实现 Plugin 主类
- [ ] 注册基本命令

### Phase 2: 书籍管理 (2-3 天)
- [ ] BookService 实现
- [ ] 书籍列表 UI
- [ ] 创建书籍流程

### Phase 3: 学习流程 (3-4 天)
- [ ] 四阶段模板
- [ ] 进度跟踪
- [ ] 模式切换

### Phase 4: AI 对话 (2-3 天)
- [ ] LearningView 侧边栏
- [ ] AIService 实现
- [ ] 对话历史

总计：约 2 周 MVP

## 7. 参考

- 需求文档：`../context/REQUIREMENTS.md`
- 原 Skill：`../../../SKILL.md`
