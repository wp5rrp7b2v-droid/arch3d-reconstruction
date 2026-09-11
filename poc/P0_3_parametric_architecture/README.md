# P0.3｜Parametric Architecture POC

Status: PASS  
Validation Date: 2026-09-11  
Blender: 3.6.23 macOS x64

## Purpose

验证“独立建筑参数 → Blender Python 脚本 → 可重复最小结构模型”的技术链路。

## Evidence

- `params/parametric_arch_v001.json`：Baseline 参数
- `params/parametric_arch_variant_v001.json`：Variant 参数
- `scripts/generate_parametric_arch_v001.py`：统一生成脚本
- `output/baseline/P0_3_PARAMETRIC_ARCH_BASELINE_V001.png`：Baseline 审核图
- `output/variant/P0_3_PARAMETRIC_ARCH_VARIANT_V001.png`：Variant 审核图

## Validation Summary

Baseline:
- 3×2 bays
- 12 columns
- 21 major structural objects
- overall size: 10.8 m × 7.0 m × 5.35 m

Variant:
- 4×3 bays
- 20 columns
- 31 major structural objects
- overall size: 12.6 m × 9.6 m × 6.05 m

Variant 仅修改 JSON 参数，未修改 Python 建模逻辑。

Baseline deterministic core signature:

`269702aa81abed07770550e3b4bd1b6288e526a6fc119630a218bac2b37f716d`

## Local-only Binary Assets

以下 Blender 二进制工程文件保留在本地，不进入普通 Git：

- `output/baseline/P0_3_PARAMETRIC_ARCH_BASELINE_V001.blend`
- `output/variant/P0_3_PARAMETRIC_ARCH_VARIANT_V001.blend`
- Blender `.blend1` 自动备份

正式验收结论详见：

`docs/project_control/`
