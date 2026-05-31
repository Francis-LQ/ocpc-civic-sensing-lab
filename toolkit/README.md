# OCPC Toolkit v0.1

`toolkit/` 提供开放公民项目的最小发布规范。

## 快速开始

1. 复制 `templates/project/`。
2. 填写 `ocpc-project.json`、项目说明、贡献记录和风险隐私清单。
3. 仅发布已获授权且完成去标识化处理的材料。
4. 运行：

```bash
python scripts/validate_ocpc_project.py path/to/project
```

JSON Schema 位于 `schema/ocpc-project.schema.json`。校验脚本使用 Python 标准库，
无需安装第三方依赖。
