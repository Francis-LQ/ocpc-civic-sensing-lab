# OCPC / 共感城市实验室

[English](#english) | [中文](#中文)

## 中文

OCPC（Open Civic Project Commons / 开放公民项目公地）是一个连接文化遗产、
公民科学与教育科技的开源知识公地。前台品牌为“共感城市实验室”
（Civic Sensing Lab / CSL）。

本仓库包含研究资料、产品规划与 **OCPC Toolkit v0.2**。Toolkit 用于把青年公共
项目整理为可检查、可复用、可持续维护的开放项目包。当前版本不是已经部署的
FastAPI + React 产品。

### Toolkit 快速开始

```bash
python scripts/validate_ocpc_project.py examples/campus-sound-map
python scripts/ocpc_toolkit.py validate examples/campus-sensing-combo
python scripts/ocpc_toolkit.py validate projects/campus-sensing-beta-2026-06
python scripts/ocpc_toolkit.py render examples/campus-sensing-combo --output .tmp-site
python -m unittest discover -s tests -v
```

创建新项目时，复制 `toolkit/templates/project/`，填写清单、公开成果、贡献记录和
风险隐私清单，然后运行校验器。清单格式见
`toolkit/schema/ocpc-project.schema.json`。

### 数据与参与者保护

公开项目包不得包含未成年人实名、联系方式、可识别个人轨迹的精确位置或未经
授权的原始数据。示例项目只使用人工生成的合成数据。涉及真实参与者时，应先
完成授权、数据最小化和安全审阅。

### 许可边界

- 新增软件代码：木兰宽松许可证第 2 版（MulanPSL-2.0），见 `LICENSE`。
- 新增原创文档与模板：木兰开放作品许可协议署名-相同方式共享第 1 版
  （MulanOWL BY-SA v1），见 `DOCS-LICENSE.md`。
- 第三方论文、原始资料、未获授权图片、个人数据和学生作品不因进入本仓库而被
  重新授权，见 `NOTICE.md`。

参与贡献前请阅读 `CONTRIBUTING.md`。维护与发布流程见 `docs/MAINTENANCE.md`。
首轮校园感知 Beta 的公开课程边界见 `docs/beta/`。
真实 Beta 的公开草案包见 `projects/campus-sensing-beta-2026-06/`；该目录不得包含
报名表、授权记录、身份映射、待审音频或撤回日志。
社区成员如希望发起新的 7 天共创挑战，请从 `docs/community/` 开始，并先提交
Community Activity issue。活动通过安全边界确认后，再进入 OCPC 项目包流程。
当前社区项目草案包括 `projects/vibe-coding-boundary-sensing/`，该项目关注
高校编程学习者的编码节奏与身心边界观察，不提供诊断、治疗或心理咨询。
校园感知组合合成示例站点：
<https://francis-lq.github.io/ocpc-civic-sensing-lab/>。

## English

OCPC (Open Civic Project Commons) is an open knowledge commons connecting cultural
heritage, civic science, and education technology. Its public-facing initiative is
Civic Sensing Lab (CSL).

This repository contains research materials, product planning, and **OCPC Toolkit
v0.2**. The toolkit packages youth civic projects as reviewable and reusable open
project bundles. It is not a deployed FastAPI + React product.

### Toolkit quick start

```bash
python scripts/validate_ocpc_project.py examples/campus-sound-map
python scripts/ocpc_toolkit.py validate examples/campus-sensing-combo
python scripts/ocpc_toolkit.py validate projects/campus-sensing-beta-2026-06
python scripts/ocpc_toolkit.py render examples/campus-sensing-combo --output .tmp-site
python -m unittest discover -s tests -v
```

Copy `toolkit/templates/project/` to start a project. Complete the manifest,
public artifacts, contributor record, and risk checklist before validation.

### Safety and licensing

Public packages must not include minors' personal data, contact details, precise
personal locations, or unauthorized raw data. See `NOTICE.md` for licensing
boundaries and `CONTRIBUTING.md` before contributing.

The public boundaries for the first Campus Sensing Beta are documented in
`docs/beta/`.
The draft public package for the real Beta is in
`projects/campus-sensing-beta-2026-06/`; private registrations, consent records,
identity maps, pending audio, and withdrawal logs must stay outside GitHub.
Community members who want to start a new 7-day challenge should begin with
`docs/community/` and open a Community Activity issue before creating a project
package.
The current community draft package includes
`projects/vibe-coding-boundary-sensing/`, which focuses on coding rhythm and
boundary observation rather than diagnosis, treatment, or counseling.
The synthetic Campus Sensing Combo site is available at
<https://francis-lq.github.io/ocpc-civic-sensing-lab/>.
