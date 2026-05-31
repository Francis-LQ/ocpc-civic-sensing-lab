## 变更说明

说明本 PR 解决的问题和公开成果。

## 验证

```bash
python scripts/validate_ocpc_project.py examples/campus-sound-map
python scripts/validate_ocpc_project.py toolkit/templates/project
python -m unittest discover -s tests -v
```

## 发布边界确认

- [ ] 未提交个人数据、精确位置、未授权原始资料或账号凭据。
- [ ] 已检查代码、原创文档与第三方材料的许可边界。
- [ ] 如涉及真实参与者，已完成授权、数据最小化和安全审阅。
