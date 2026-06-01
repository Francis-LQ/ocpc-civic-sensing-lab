# OCPC Toolkit 维护与发布说明

## 日常维护

1. 使用 issue 记录 bug、文档改进和项目提案。
2. 对每个变更检查许可边界、参与者隐私和原始资料可追溯性。
3. 修改工具包后运行：

```bash
python scripts/validate_ocpc_project.py examples/campus-sound-map
python scripts/ocpc_toolkit.py validate examples/campus-sensing-combo
python scripts/ocpc_toolkit.py validate toolkit/templates/project
python scripts/ocpc_toolkit.py render examples/campus-sensing-combo --output .tmp-site
python -m unittest discover -s tests -v
```

## 发布检查清单

- [ ] 合成示例和项目模板通过校验。
- [ ] 单元测试通过。
- [ ] README 命令可直接运行。
- [ ] CHANGELOG 已更新。
- [ ] 未把第三方原始资料纳入开放许可。
- [ ] 未公开未成年人个人信息、联系方式、精确位置或未经授权原始数据。
- [ ] GitHub Actions 通过。
- [ ] release notes 已说明新增能力和已知边界。

## 大文件与 Git LFS 审计建议

仓库包含较大的 PDF、DOCX 和 PPTX 历史资料。为保持可追溯性，本版本不移动、
删除或重写这些文件。后续应单独审计远端存储限制、Git LFS 可行性、第三方材料
公开边界和历史迁移方案，再决定是否迁移。
