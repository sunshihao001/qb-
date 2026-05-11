# Sandbox Policy V2.0

- R0/R1 read-only 可自动 allow。
- R2 普通命令需记录结果。
- R3 写入仅限 /root/sikk-gmgn/hermes_harness/ 授权范围。
- R4 需要人类裁决，本任务默认 deny。
- R5 destructive/secret/trading/broadcast 一律 deny。
- Bash/terminal 单独治理，禁止 `rm -rf`、真实交易、读取密钥、git push。
