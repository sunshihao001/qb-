# SIKK 大系统冻结与备份声明

## 冻结原因

当前大型交易系统同时包含：

- HER_DOC
- P01-P10 阶段体系
- Control Plane
- phase controllers
- runner binding
- domain planes
- method loops / 方法轮
- wallet intelligence / wallet structure modules
- paper/runtime/review 体系

如果继续在同一个运行主线里完善这些大型系统，同时又想快速恢复钱包结构分析项目，会产生：

- 认知冲突：到底是先运行 token，还是先完善体系；
- 目录冲突：个人轻量运行产物和大型控制面产物混写；
- 字段冲突：P01-P10 contract 字段和轻量 S01-S05 字段互相牵引；
- 执行优先级冲突：真实样本分析被治理/标准/协议任务阻塞。

## 当前决策

大型体系先完整备份到 GitHub，不继续作为当前主线扩展。

短期主线改为：

1. 保留一个主系统：`/root/sikk-gmgn/`
2. 保留旧钱包分析项目；
3. 钱包分析作为主系统核心模块；
4. P01-P10 运行时压缩为 S01-S05；
5. 冻结大型 HER 总控设计；
6. 先跑单 token；
7. 再跑批量 paper。

## 当前允许继续做的事

- 修复单 token 分析读数问题；
- 补最小字段缺口；
- 跑真实 token；
- 做 paper-only；
- 做复盘归因；
- 输出轻量报告。

## 当前暂停的事

- 新增大型 Plane；
- 新增复杂 Controller；
- 扩大 HER Control Plane；
- 继续拆 P01-P10 合同；
- 新增大型 schema/handoff/contract 体系；
- 把个人版需求做成机构级系统。

## 备份后用途

此备份可用于：

- 回溯历史设计；
- 后续拆分仓库；
- 提取成熟模块；
- 查找阶段/字段/控制面定义；
- 对照个人版轻量系统做取舍。

不用于：

- 继续阻塞单 token 分析；
- 继续扩大当前运行主线；
- 自动覆盖个人版轻量逻辑。
