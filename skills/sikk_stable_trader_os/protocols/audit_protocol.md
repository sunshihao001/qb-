# Audit Protocol

每次阶段运行必须写入 audit：

- input refs
- output refs
- contract validation result
- schema validation result
- source refs
- missing/gap register
- hard-negative check result
- safety boundary check

审计必须能回答：为什么通过、为什么降级、为什么阻断、下游读什么。
