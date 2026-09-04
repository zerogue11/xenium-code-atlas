# 05 运行环境

> 环境本体（venv/WSL 发行版/下载缓存）不入版本管理；此处只登记"规格与位置"。

## 本项目用到的环境

| 用途 | 位置 | 说明 |
|---|---|---|
| 主 Python（脚本/主表/体检） | `C:\xenium_envs\xenium-cn-py311`（venv，python.exe 在 `Scripts/` 下） | 复用官方教程中文优化线的既有环境，scanpy 1.12.1 / spatialdata 0.7.3 / squidpy 1.8.1 |
| mkdocs 站点构建 | `uvx --from mkdocs-material mkdocs`（隔离运行，不落全局） | 构建与本地预览 |
| GitHub CLI | gh 2.93.0，账号 zerogue11（keyring token，repo 权限） | 建仓/推送/Pages |
| OV GPU（引用，非本项目所有） | WSL `Ubuntu-22.04-OV-GPU` / micromamba `ov-gpu-xenium` | 详见 ov工作流测试 `GPU环境策略.md` |

## 纪律

- 新增环境先在此登记规格（用途/位置/关键包版本/创建命令），再使用。
- 分析环境不装文档工具，文档工具不进分析环境。
