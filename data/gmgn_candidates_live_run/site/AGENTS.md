# SIKK Dashboard Site Rules

本目录只放静态可视化网站文件。

允许文件：

- `index.html`
- `app.js`
- `style.css`
- `dashboard_data.json`
- `AGENTS.md`

规则：

- 页面只读取 `dashboard_data.json`。
- 不调用交易接口。
- 不写入交易数据。
- 不需要后端。
- 不使用数据库。
- 不使用大型前端框架。
- 不创建登录系统。
- 页面只用于观察、筛选、复盘。

页面必须包含：

- KPI 卡片
- Pipeline 漏斗
- 重点机会
- Token 总表
- 搜索和筛选
- 未入场原因
- 纸面仓位
- 最新事件
