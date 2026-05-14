# SIKK Stable Trader OS｜Entity Relationship Map v2.0

Token
  ├── has_many Wallet
  ├── has_many TransactionEvent
  ├── has_many MarketSnapshot
  ├── has_one MarketScene
  ├── has_one ChipState
  ├── has_one DominantSide
  ├── has_many Counterparty
  ├── has_many GateDecision
  ├── has_many RiskEvent
  ├── has_many ExecutionTicket
  ├── has_many PaperPosition
  ├── has_many ReviewCase
  └── has_many RuleChange

Wallet -> belongs_to Token; has_many TransactionEvent; belongs_to AddressGroup
AddressGroup -> has_many Wallet; has_many TransactionEvent; contributes_to ChipState
MarketScene/ChipState/DominantSide -> contributes_to GateDecision
RiskEvent -> may_force GateDecision
ExecutionTicket -> creates PaperPosition
PaperPosition -> creates ReviewCase
ReviewCase -> may_create RuleChange
