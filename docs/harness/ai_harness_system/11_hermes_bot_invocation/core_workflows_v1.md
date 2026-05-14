# V1.0 核心工作流

> 方法轮补全路线图：`../02_research_loop/method_wheel_completion_checklist_v1.md`

## 工作流 1：自然语言目标 → 专业任务

```text
用户输入目标
↓
生成目标护照
↓
识别任务类型
↓
读取控制面
↓
拆分阶段
↓
生成 Hermes 任务包
↓
执行
↓
验证
↓
复盘
↓
写入记忆
```

## 工作流 2：文章 / 书籍 → 方法轮

```text
接收文章
↓
文档护照
↓
核心机制提炼
↓
问题识别
↓
系统映射
↓
缺口检测
↓
任务生成
↓
执行计划
↓
验收标准
↓
复盘沉淀
```

## 工作流 3：系统混乱 → 治理

```text
目录侦察
↓
文件分类
↓
阶段归属判断
↓
重复/废弃/核心文件识别
↓
标准目录设计
↓
迁移计划
↓
风险检查
↓
执行
↓
验证
```

## 工作流 4：Hermes 长任务

```text
建立任务包
↓
限定运行范围
↓
每轮输出状态
↓
每轮验证产物
↓
失败进入恢复
↓
阶段完成后生成报告
↓
继续下一阶段
```

## 工作流 5：CA → 新钱包数据分析入口

```text
用户发送 ca / CA / ca <token_address>
↓
识别为 Source Wallet Bot 入口触发
↓
若带 token_address，解析为目标 token
↓
定位 data/source_wallet_bot/<mode>/<token_address>/
↓
优先读取 wallet_data/
↓
再读取 structure_analysis/
↓
只读展示 / 不交易 / 不签名 / 不广播
↓
回传目录入口或 token 分析页面
```
