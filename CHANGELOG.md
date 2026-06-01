# Changelog

本项目遵循语义化版本号记录 OCPC Toolkit 的公开版本。

## [Unreleased]

## [0.2.0] - 2026-06-01

### Added

- 统一零依赖 CLI：`scaffold`、`validate` 和 `render`。
- 校园微气候与声景组合合成示例、协议、Rubric 和匿名个人页结构。
- 静态项目页生成与 GitHub Pages 部署工作流。
- 面向 14 天邀请制 Beta 的课程边界、数据字典和运营检查单。

### Changed

- 公开清单升级到 `schema_version = 0.2.0`，增加主题、协议和发布审阅字段。
- 兼容入口 `validate_ocpc_project.py` 复用新的校验实现。

## [0.1.1] - 2026-06-01

### Fixed

- 校验器拒绝未知 `schema_version`，避免使用不兼容清单。
- 校验器拒绝指向项目目录外的公开成果路径。

## [0.1.0] - 2026-06-01

### Added

- OCPC 项目清单格式和 JSON Schema。
- 零依赖 Python 校验器。
- 可复制项目模板和合成校园声音地图示例。
- 中英双语入口、贡献指南、维护流程和分层许可说明。
- GitHub Actions 校验流程和 issue 模板。
