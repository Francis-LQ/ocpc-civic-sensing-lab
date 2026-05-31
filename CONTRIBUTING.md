# 贡献指南 / Contributing Guide

感谢你参与 OCPC。这里优先接收可复用模板、校验器改进、文档修正和安全边界建议。

## 提交方式

1. 先创建 issue，说明问题、预期公开成果和数据安全边界。
2. 从 `main` 创建小范围分支。
3. 修改代码时运行：

```bash
python scripts/validate_ocpc_project.py examples/campus-sound-map
python -m unittest discover -s tests -v
```

4. 提交 PR，说明变更、验证结果和许可边界。

## 可接受贡献

- OCPC 项目模板、JSON Schema 与校验器改进。
- 面向教育者、文化工作者和社区维护者的文档。
- 仅包含已获授权、已去标识化内容的示例项目。
- 对隐私、安全、开放许可和复用流程的改进建议。

## 不要提交

- 未成年人实名、联系方式、面部图像或其他个人信息。
- 可识别个人活动轨迹的精确位置数据。
- 未经授权的原始数据、论文、图片、音视频或学生作品。
- API Key、Token、账号凭据、Office 临时文件或生成缓存。

## 授权说明

提交代码即表示你有权将贡献按 MulanPSL-2.0 提供。提交原创文档或模板即表示你
有权将贡献按 MulanOWL BY-SA v1 提供。第三方材料必须保留原许可和来源，不得
通过 PR 重新授权。

## English summary

Open an issue before contributing. Keep changes focused, run the validator and
unit tests, and state the licensing boundary in your PR. Do not submit personal
data, precise personal locations, unauthorized raw materials, or secrets.
