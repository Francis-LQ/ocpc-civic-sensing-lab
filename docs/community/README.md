# CSL Community Launch Kit / 共感城市实验室社区发起者工具包

这个工具包帮助老师、馆员、家长、学生社团和社区志愿者发起一个低门槛、可审阅、可复用的 CSL 7 天共创挑战。

## 你可以做什么

- 选择一个身边公共议题，例如遮阴、声音、微气候、公共休憩、校园动线或文化空间体验。
- 组织一个 7 天小挑战，邀请参与者完成低门槛观察或共创任务。
- 产出活动说明、协议、Rubric、去标识化聚合摘要和复盘。
- 在安全边界确认后，将成果整理为 OCPC 项目草案包。

## 不做什么

- 不把社区挑战写成课程售卖。
- 不把观察结果写成健康、安全或政策结论。
- 不默认公开个人页、音频、图片或学生作品。
- 不把报名表、联系方式、授权记录、精确位置、原始音频或撤回日志提交到 GitHub。

## 快速开始

1. 阅读 `PUBLIC_BOUNDARY.md`，确认公开与私有边界。
2. 复制 `PROMOTION_TEMPLATE.md`，改写成适合你的社群邀请文案。
3. 填写 `ACTION_CANVAS.md`，明确公共议题、参与对象、7 天任务和安全门禁。
4. 使用 GitHub 的 Community Activity issue 模板提交提案。
5. 提案通过后，按 `SEVEN_DAY_CHALLENGE_PLAYBOOK.md` 执行活动。
6. 活动结束后，提交经审核的公开成果和复盘；如需要项目包，再进入 `toolkit/templates/project/` 流程。

## 文件索引

| 文件 | 用途 |
| --- | --- |
| `PROMOTION_TEMPLATE.md` | 一句话介绍、活动邀请、合作方说明和社群转发文案 |
| `ACTION_CANVAS.md` | 7 天小挑战的一页行动画布 |
| `SEVEN_DAY_CHALLENGE_PLAYBOOK.md` | Day 0 到 Day 7 的执行流程 |
| `ROLE_CARDS.md` | 发起人、数据管理员、安全审阅人、记录员和参与者职责 |
| `PUBLIC_BOUNDARY.md` | 公开成果、私有资料、未成年人、音频、位置和撤回边界 |
| `EXAMPLE_ACTIVITY.md` | 无真实数据的“校园遮阴与声景 7 天挑战”示例 |

## 进入 OCPC 项目包的门槛

- 已有公开 issue 记录活动目标和安全边界。
- 公开成果只包含去标识化、经审阅、可授权发布的内容。
- 私有主账本、授权记录、身份映射和撤回日志不进入 GitHub。
- 维护者或指定安全审阅人确认可以创建项目草案包。

## 推荐命令

```bash
python scripts/ocpc_toolkit.py scaffold your-activity-id --title "活动标题" --output projects/your-activity-id
python scripts/ocpc_toolkit.py validate projects/your-activity-id
```

创建项目包前，请先完成社区活动 issue 的安全边界确认。
