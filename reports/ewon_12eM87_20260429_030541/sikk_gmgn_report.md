# SIKK-GMGN 单币自动化分析报告


token_address: `12eM87tTACWpgnwuapFUHDVDXFaZSxJqxBNj1AHB56sy`  
chain: `sol`  
auto_trade: `false`


## 分析深度控制表
| field | value | remark |
| --- | --- | --- |
| analysis_depth_level | L3 深度结构复盘 | 先判断深度，不默认全量深挖 |
| depth_reason | bundler占比47.71%, fresh=10.84%, sniper=54, smart=43, Top10=18.09%, liquidity=65308.58 | 由结构指标触发 |
| selected_time_windows | W1,W2,W3,W4,W6 | 优先0-30分钟，复盘派发/清仓/回流 |
| deep_analysis_address_scope | 0-30m早期买入,bundled,insider,sniper,fresh,transfer_in,Top Holder,Top Trader,Smart/KOL,rat_trader,核心资金源,回流节点 | 只深挖关键地址 |
| low_weight_address_scope | 中后期小额普通买家,无标签,无复现,无异常来源,非Top Holder/Trader | 低权重记录 |
| skipped_address_reason | 不全量深挖所有散户 | 降低成本并避免历史库污染 |
| infrastructure_edges_kept | LP/Pool/Router/Aggregator/CEX/Program/native_from/token_from | 基础设施不评分但保留关系边 |
| next_review_plan | T+1h,T+6h,T+24h,T+72h,T+7d | E4/R优先复盘 |


## 代币基础信息表
| field | value | remark |
| --- | --- | --- |
| token_symbol | ewon | 未知 |
| token_name | ewon mesk | 未知 |
| token_address | 12eM87tTACWpgnwuapFUHDVDXFaZSxJqxBNj1AHB56sy | 未知 |
| chain | sol | 未知 |
| price_usd | 0.00048781 | 未知 |
| market_cap_calc_usd | 487797.68 | price*circulating_supply |
| liquidity_usd | 65308.58 | 未知 |
| holder_count | 2625 | 未知 |
| creation_time | 2026-04-29 00:16:59 UTC | 未知 |
| open_time | 2026-04-29 00:18:12 UTC | 未知 |
| launchpad | Pump.fun | 未知 |
| main_pool | Gr3k2DGNLnFVZqwhvSBE9xLxe4CN1uGtB3RACCbsJH4 | 未知 |
| creator_address | bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa | 未知 |
| creator_token_status | creator_close | 未知 |
| creator_open_count | 609 | 未知 |
| cto_flag | 1 | 未知 |
| gmgn_url | https://gmgn.ai/sol/token/12eM87tTACWpgnwuapFUHDVDXFaZSxJqxBNj1AHB56sy | 未知 |
| website | https://www.reuters.com/legal/litigation/openai-trial-pitting-elon-musk-against-sam-altman-kicks-off-2026-04-28/ | 未知 |
| twitter_username | DramaAlert/status/2049281729186222405 | 未知 |


## 代币结构指标表
| metric | value | remark |
| --- | --- | --- |
| renounced_mint | True | 安全权限 |
| renounced_freeze_account | True | 安全权限 |
| buy_tax | 0 | 交易税 |
| sell_tax | 0 | 交易税 |
| burn_status | burn | LP燃烧 |
| top_10_holder_rate | 18.090% | 筹码集中度 |
| fresh_wallet_rate | 10.840% | 新钱包比例 |
| top_bundler_trader_percentage | 47.710% | bundler交易占比 |
| top_rat_trader_percentage | 0.020% | rat交易占比 |
| top_entrapment_trader_percentage | 11.230% | entrapment占比 |
| bot_degen_rate | 38.590% | bot比例 |
| smart_wallets | 43 | GMGN标签 |
| renowned_wallets | 8 | KOL |
| sniper_wallets | 54 | 狙击 |
| bundler_wallets | 1000 | bundler |
| fresh_wallets | 409 | fresh |
| rat_trader_wallets | 3 | rat |
| 1h_open | 0.00132481 | kline |
| 1h_close | 0.00049372 | kline |
| 1h_change_pct | -62.73% | kline |
| 1h_high | 0.00147447 | kline |
| 1h_low | 0.00022899 | kline |
| 1h_volume_usd | 1517235.40 | kline |


## sikk_gmgn_master_log.csv 预览
| address | gmgn_tags | address_type | token_source_type | funding_source_type | final_role | evidence_level | signal_direction | action_code | review_windows | sikk_remark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gr3k2DGNLnFVZqwhvSBE9xLxe4CN1uGtB3RACCbsJH4 | top_holder | 基础设施 | 主动买入 | 未知源 | LP池子 | I1 | 排除 | I | T+24h,T+72h | LP/Pool基础设施，不进入普通钱包评分 |
| GQjwMEMvfAPngTPd6o5w2sZzt6xvaZho9gYSgEqc8FAT | top_holder | 基础设施 | 主动买入 | 未知源 | LP池子 | I1 | 排除 | I | T+24h,T+72h | LP/Pool基础设施，不进入普通钱包评分 |
| DxM1hfY8FQ8dNGrucuJzhJcF8KRbjk8WBwrgKvQ9spPv | fomo,kol,top_holder,bundler | 普通钱包 | 主动买入 | 路由/工具节点候选 | 结果钱包/KOL钱包 | E3 | 正向+社交 | A3 | T+6h,T+24h,T+72h | KOL参与，注意后续派发 |
| 2fg5QD1eD7rzNNCsvnhmXFm5hqNgwTTG8p7kQ6f3rx6f | kol,axiom,gmgn,wash_trader,bundler,transfer_in,paper_hands | 普通钱包 | 转入 | 路由/工具节点候选 | 分发派发钱包 | E4/R2 | 结构+风险 | A4+R | T+1h,T+6h,T+24h,T+72h,T+7d | Token转入后高比例卖出，疑似分发后派发 |
| JBhVoSaXknLocuRGMUAbuWqEsegHA8eG1wUUNM2MBYiv | axiom,top_holder,bundler | 普通钱包 | 主动买入 | 路由/工具节点候选 | 结果钱包 | E4 | 正向+结构 | A4 | T+1h,T+6h,T+24h,T+72h,T+7d | bundler+高结果，疑似结构执行中的结果地址 |
| EmfYATLLQWYPDiqHxBFFKNzPFZTEPLupknMWAJZLzgwP | fomo,top_holder,transfer_in | 普通钱包 | 转入 | 路由/工具节点候选 | 分发接收钱包 | E4 | 结构 | A4 | T+1h,T+6h,T+24h,T+72h,T+7d | Token转入/接收，需追token_source_address |
| GijFWw4oNyh9ko3FaZforNsi3jk6wDovARpkKahPD4o5 | axiom,photon,padre,bundler,transfer_in | 普通钱包 | 转入 | 路由/工具节点候选 | 分发派发钱包 | E4/R2 | 结构+风险 | A4+R | T+1h,T+6h,T+24h,T+72h,T+7d | Token转入后高比例卖出，疑似分发后派发 |
| o1cwo8ZWUhGir84GWmeWJo5JZbmeMPnoypuK98q4fMU | fresh_wallet,top_holder,bundler | 普通钱包 | 主动买入 | 路由/工具节点候选 | 新钱包狙击 | E3 | 结构 | A3 | T+6h,T+24h,T+72h | fresh/bundler早期参与，历史稳定性待验证 |
| 7zNeNdCtyteKLop816zN6HoCyhYXtQf9U8jnW7FNVgXX | fomo,top_holder,bundler | 普通钱包 | 主动买入 | 路由/工具节点候选 | 普通交易钱包 | E2 | 中性 | A2 | T+24h,T+72h | Top holder但关键结构证据不足 |
| J4hY1wpM6dZCzAbFndKUBZBEEG5yVRdP96zYnPu9dULb | fomo,top_holder,bundler | 普通钱包 | 主动买入 | 未知源 | 普通交易钱包 | E2 | 中性 | A2 | T+24h,T+72h | Top holder但关键结构证据不足 |
| GExMN6extw7JyLe3jENEZwULyyqbDxxcrfF44VFLvFAT | smart_degen,bundler | 普通钱包 | 主动买入 | 路由/工具节点候选 | 结果钱包 | E4 | 正向 | A4 | T+1h,T+6h,T+24h,T+72h,T+7d | Smart Money高结果，需复盘稳定性 |
| Dfi33bzKPRk7yrRxA8q9MB4TR9FodZ51wK9kkqbsrq4v | gmgn,fresh_wallet,top_holder,bundler | 普通钱包 | 主动买入 | 路由/工具节点候选 | 接盘鲸鱼/派发风险地址 | R2 | 风险 | R | T+6h,T+24h,T+72h | 高买入且大比例卖出/结果不稳定 |


## infrastructure_registry.csv 预览
| address | entity_type | entity_name | infrastructure_level | exclusion_reason | structure_relevance | risk_relevance | keep_edges |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gr3k2DGNLnFVZqwhvSBE9xLxe4CN1uGtB3RACCbsJH4 | LP/Pool | pump_amm | I1 | LP池子不进入普通钱包评分 | 中 | 低 | 是 |
| GnRFFi8CW1gVuUKYyoFjm4cxfAfX1iE2iGgp7DSwJJB5 | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| AxiomRXZAq1Jgjj9pHmNqVP7Lhu67wLXZJZbaK87TTSk | Router/TradingTool | GMGN返回native_from | I3 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| 22zjkDKzquzFCCvnxRSYQU1Bb6gSu52LTEU3ZCBBQYuf | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| B48kNVXs4YK4amkBCH2XokQiv1SeiVQGHDR17xDeKAAn | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| BNuebGMyAsrLytsS13whc3qUqbnM9mVwUJcumD31m5zA | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| GfjD8eab6ebLRnbvjMHo2P11JFKrv2xrkVXVdQtktwTk | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| 8J7NGPfkD4oF2Pu8zXbxNvNfqhjaW668WnkNu7VrUv17 | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| kapRxcwXvkdCLgbc6WuxQtkTYYovs7buJ3hbMp4Xri2 | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |
| 5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9 | FundingSourceCandidate | GMGN返回native_from | I2 | 资金来源/交易工具候选，不进入普通钱包评分 | 中 | 中 | 是 |


## review_update_history.csv 预览
| review_id | address | review_window | old_evidence_level | old_role | review_conclusion | reason |
| --- | --- | --- | --- | --- | --- | --- |
| ewon_Gr3k2D | Gr3k2DGNLnFVZqwhvSBE9xLxe4CN1uGtB3RACCbsJH4 | T+24h,T+72h | I1 | LP池子 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_GQjwME | GQjwMEMvfAPngTPd6o5w2sZzt6xvaZho9gYSgEqc8FAT | T+24h,T+72h | I1 | LP池子 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_DxM1hf | DxM1hfY8FQ8dNGrucuJzhJcF8KRbjk8WBwrgKvQ9spPv | T+6h,T+24h,T+72h | E3 | 结果钱包/KOL钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_2fg5QD | 2fg5QD1eD7rzNNCsvnhmXFm5hqNgwTTG8p7kQ6f3rx6f | T+1h,T+6h,T+24h,T+72h,T+7d | E4/R2 | 分发派发钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_JBhVoS | JBhVoSaXknLocuRGMUAbuWqEsegHA8eG1wUUNM2MBYiv | T+1h,T+6h,T+24h,T+72h,T+7d | E4 | 结果钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_EmfYAT | EmfYATLLQWYPDiqHxBFFKNzPFZTEPLupknMWAJZLzgwP | T+1h,T+6h,T+24h,T+72h,T+7d | E4 | 分发接收钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_GijFWw | GijFWw4oNyh9ko3FaZforNsi3jk6wDovARpkKahPD4o5 | T+1h,T+6h,T+24h,T+72h,T+7d | E4/R2 | 分发派发钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_o1cwo8 | o1cwo8ZWUhGir84GWmeWJo5JZbmeMPnoypuK98q4fMU | T+6h,T+24h,T+72h | E3 | 新钱包狙击 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_7zNeNd | 7zNeNdCtyteKLop816zN6HoCyhYXtQf9U8jnW7FNVgXX | T+24h,T+72h | E2 | 普通交易钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_J4hY1w | J4hY1wpM6dZCzAbFndKUBZBEEG5yVRdP96zYnPu9dULb | T+24h,T+72h | E2 | 普通交易钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_GExMN6 | GExMN6extw7JyLe3jENEZwULyyqbDxxcrfF44VFLvFAT | T+1h,T+6h,T+24h,T+72h,T+7d | E4 | 结果钱包 | pending | 卖出/转出/资金回流/角色升级降级 |
| ewon_Dfi33b | Dfi33bzKPRk7yrRxA8q9MB4TR9FodZ51wK9kkqbsrq4v | T+6h,T+24h,T+72h | R2 | 接盘鲸鱼/派发风险地址 | pending | 卖出/转出/资金回流/角色升级降级 |