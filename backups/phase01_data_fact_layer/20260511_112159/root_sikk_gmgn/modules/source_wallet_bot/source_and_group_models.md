# Source and Same-Source Group Models

## 1. Model boundary
Source & Wallet Intelligence Bot may produce evidence-backed candidate groups. It must not produce final dominant-side control decisions.

## 2. Candidate same-source evidence dimensions
- same funding source address
- funding time similarity
- buy time similarity
- buy amount similarity
- GMGN tag overlap
- synchronized sell behavior
- shared backflow receiver
- matching transaction path signature
- cross-token reappearance

## 3. Candidate group output fields
- `candidate_group_key`
- `same_source_evidence_items`
- `group_basis_fields`
- `group_basis_text_zh`
- `evidence_level`
- `risk_level`
- `requires_followup_fields`

## 4. Evidence levels
- E0: no evidence
- E1: weak single-field hint
- E2: multiple weak hints
- E3: strong behavior + tag evidence
- E4: strong on-chain path evidence
- E5: strong path + synchronized behavior + backflow

## 5. Risk levels
- R0: low / no notable risk evidence
- R1: weak risk hint
- R2: moderate risk
- R3: strong risk
- R4: severe risk evidence

## 6. Allowed wording
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

## 7. Not allowed
- final same_source_group_id as Bot2 decision
- final dominant-side control inference
- PAPER_READY / BLOCKED
- final_trade_gate
