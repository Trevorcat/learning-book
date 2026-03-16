# MVP 开发 Prompt

## 目标

实现 Quick Book Mastery Obsidian 插件的最小可行产品（MVP）。

## 必须实现的功能

### 1. 插件基础架构
- [ ] 主插件类（main.ts）
- [ ] 侧边栏视图（View）
- [ ] 设置面板（Settings Tab）
- [ ] 命令注册

### 2. 书籍管理
- [ ] `createBookProject()` - 创建书籍学习项目
- [ ] `listBooks()` - 列出所有书籍
- [ ] `getBookProgress()` - 获取学习进度
- [ ] 书籍数据结构定义

### 3. 学习模式选择
- [ ] 模式选择 Modal
- [ ] 快速模式 vs 伴读模式说明

### 4. 四阶段模板
- [ ] 阶段1模板：准备与目标设定
- [ ] 阶段2模板：概览与框架构建
- [ ] 阶段3模板：深入与理解
- [ ] 阶段4模板：巩固与应用

### 5. AI 对话面板
- [ ] 侧边栏聊天界面
- [ ] API Key 设置（本地存储）
- [ ] Claude API 调用
- [ ] 对话历史

## 文件结构

```
src/
├── main.ts              # 插件入口
├── views/
│   └── LearningView.ts  # 主侧边栏视图
├── modals/
│   └── ModeSelectModal.ts # 模式选择弹窗
├── templates/
│   └── index.ts         # 学习模板
├── types/
│   └── index.ts         # TypeScript 类型定义
└── utils/
    └── api.ts           # Claude API 调用
```

## 数据结构

```typescript
interface Book {
  id: string;
  title: string;
  author?: string;
  mode: 'fast' | 'companion';
  currentStage: 1 | 2 | 3 | 4;
  progress: number; // 0-100
  createdAt: Date;
  updatedAt: Date;
}

interface LearningProfile {
  goal: string;
  timeBudget: string;
  priorKnowledge: string;
  targetDate?: Date;
}
```

## 当前任务

请实现 [具体模块]，要求：
1. 符合 Obsidian API 规范
2. 类型安全（TypeScript 严格模式）
3. 代码注释完整
4. 遵循项目已有代码风格
