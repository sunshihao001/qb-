# Evidence Note Rules and GMGN Watchlist Rules

## Allowed evidence language
- 疑似结构执行钱包
- 疑似同源执行组
- 疑似分发接收钱包
- 疑似派发钱包
- 疑似利润回收钱包
- 疑似核心资金源候选
- 疑似接盘鲸鱼
- 疑似结果钱包
- 证据不足
- 字段缺失
- 需要链上补查

## Forbidden language
- 确定庄家
- 一定是庄家
- 百分百内幕
- 绝对老鼠仓

## GMGN note format
Recommended format:
`[SIKK证据] role=<疑似角色>; evidence=<字段名:值>; missing=<字段缺失>; followup=<需要链上补查>; level=<E0-E5>; risk=<R0-R4>`

## Watchlist action
Allowed actions:
- `watch_candidate`
- `watch_same_source_candidate`
- `watch_distribution_candidate`
- `watch_backflow_candidate`
- `watch_whale_candidate`
- `no_action_field_missing`

## Rule
GMGN notes and watchlist entries are annotations only. They must not become trade gates or Bot2 final decisions.
