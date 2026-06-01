# OCPC Toolkit v0.2

`toolkit/` 提供开放公民项目的最小发布规范。

## 快速开始

1. 复制 `templates/project/`。
2. 填写 `ocpc-project.json`、项目说明、贡献记录和风险隐私清单。
3. 仅发布已获授权、完成去标识化处理并经过公开审阅的材料。
4. 使用统一 CLI：

```bash
python scripts/ocpc_toolkit.py scaffold your-project-id --title "项目标题" --output path/to/project
python scripts/ocpc_toolkit.py validate path/to/project
python scripts/ocpc_toolkit.py render path/to/project --output path/to/site
```

JSON Schema 位于 `schema/ocpc-project.schema.json`。校验脚本使用 Python 标准库，
无需安装第三方依赖。原有 `python scripts/validate_ocpc_project.py <project-dir>`
命令继续可用。
