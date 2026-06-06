# Changelog

本项目遵循语义化版本号记录 OCPC Toolkit 的公开版本。

## [Unreleased]

### Changed

- 更新创业项目方案的开放许可策略：代码使用 MulanPSL-2.0，明确纳入开放范围的原创文档使用 MulanOWL BY-SA v1，专项资产采用文件级权利核验。
- 明确第三方资料、学生作品、参与者媒体和未经审阅数据默认不因进入仓库而获得重新授权。
- 将商业模式表述调整为对交付、质控、运营和定制服务收费，不改变已公开材料的许可条款。

### Added

- 增加校园感知 Beta 30 天运营手册、招募与 onboarding 文案、公开发布门禁和 Day 30 复盘模板。
- 增加私有主账本空白模板和 `.gitignore` 防误提交规则。
- 增加真实 Beta 公开草案包 `projects/campus-sensing-beta-2026-06/`，用于后续审核后发布聚合成果。
- 增加 CSL 社区发起者工具包、7 天小挑战行动模板和社区活动 issue 模板。
- 增加 `vibe-coding-boundary-sensing` CSL 社区项目草案包，用于高校编程学习者身心边界感知 7 天挑战。

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
