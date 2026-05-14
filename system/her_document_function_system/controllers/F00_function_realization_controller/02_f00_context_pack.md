     1|     1|# F00 Context Pack｜Function Realization Controller
     2|
     3|## Core positioning / 核心定位
     4|
     5|```text
     6|F00 = K00 之后的功能落实控制器
     7|```
     8|
     9|K00 负责把 GPT 研究资料变成系统可接收、可索引、可交接的资料。F00 负责把这些资料继续转化为功能需求、字段模型、判断逻辑、schema / contract、代码模块、测试、replay、runner binding、trace / audit、acceptance 与 handoff。
    10|
    11|F00 的目标是把解释性文档推进为 HER 可执行、可验证、可审计、可交接的系统功能资产。
    12|     2|
    13|     3|## Why F00 exists
    14|     4|
    15|     5|K00 only proves that a document has been preserved, registered, indexed, mapped, and accepted into HER-DFAFS. F00 exists to convert that accepted knowledge material into functional system requirements and implementation assets.
    16|     6|
    17|     7|## F00 must not do
    18|     8|
    19|     9|- Do not summarize documents as the final output.
    20|    10|- Do not treat K00 acceptance as implementation completion.
    21|    11|- Do not write live runtime, wallet signing, auto deploy, or direct production changes.
    22|    12|- Do not declare READY without schema/contract/test/replay/acceptance evidence.
    23|    13|- Do not hide unresolved gaps.
    24|    14|
    25|    15|## F00 must do
    26|    16|
    27|    17|- Read K00 handoff and source references.
    28|    18|- Extract source concepts that imply system capabilities.
    29|    19|- Convert concepts into required functions.
    30|    20|- Build field model requirements.
    31|    21|- Build executable rule logic requirements.
    32|    22|- Decide implementation path for each function.
    33|    23|- Plan assets required for code/schema/contract/test/replay/runner/handoff.
    34|    24|- Emit a machine-readable F00 state and downstream handoff packet.
    35|    25|
    36|    26|## Completion standard
    37|    27|
    38|    28|F00 is complete only when concept-to-function mapping, implementation decisions, asset plan, evidence requirements, and handoff packet are generated and validated against their schemas.
    39|    29|

## F00 must answer / F00 必须回答

- 这个文档要求系统新增什么功能？
- 修改什么功能？
- 增强什么功能？
- 阻断什么错误？
- 需要哪些字段？
- 需要哪些判断规则？
- 需要哪些 schema / contract？
- 需要哪些代码模块？
- 需要哪些测试？
- 需要哪些 replay？
- 需要接入哪个 runner？
- 如何验收？
- 如何交接？
