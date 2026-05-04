# SIKK site 静态控制台 Dogfood QA 报告（2026-05-03）

## 范围
- URL：`http://127.0.0.1:8765/index.html`
- 目录：`data/gmgn_candidates_live_run/site/`
- 文件：`index.html`、`app.js`、`style.css`、`dashboard_data.json`
- 安全边界：只读观察；不执行真实 swap；不读取私钥；不签名；不广播。

## 执行步骤
1. 启动本地静态服务：`python3 -m http.server 8765 --bind 127.0.0.1`
2. 浏览器打开 `index.html`
3. 检查 DOM/控制台/资源加载
4. 验证 KPI、代币总表、搜索筛选、优先级排序、单币详情抽屉
5. 视觉检查页面布局与只读边界
6. 关闭静态服务

## 真实样例结果
- 页面标题：`SIKK-SOL Visual Console v2`
- KPI 已加载：候选币总数 `156`、观察中 `112`、已阻断 `20`、纸面准备就绪 `6`、纸面持仓中 `6`
- 代币总表行数：`156`
- 开放纸面仓位卡片：`5`
- `dashboard_data.json` 加载成功，资源大小约 `1,360,550` bytes
- 搜索 `LITH` 后表格剩余 `1` 行
- 点击代币行后 `单币详情` 抽屉打开，展示 LITH 阶段证据、Lifecycle Timeline、纸面入场与持仓监控信息
- 页面边界文案：`只读静态观察控制台；不执行真实 swap，不读取私钥，不自动 broadcast。`

## 发现问题
- Critical：0
- High：0
- Medium：0
- Low：0

## 视觉结论
页面加载成功，深色主题布局完整；侧边栏、KPI、方法论流程、候选漏斗、重点机会、代币总表、纸面验证区、系统健康、最新事件均可见。单币详情抽屉可正常打开。未发现真实交易按钮、钱包连接、签名、broadcast 或 swap 执行入口。

## 证据截图
MEDIA:/root/.hermes/cache/screenshots/browser_screenshot_e31a4606218f421e9d54c5b8921442a6.png

## 验收结论
PASS：site 静态控制台满足只读 dogfood 验收，可继续进入 git diff 清理与最终执行序列收束。
