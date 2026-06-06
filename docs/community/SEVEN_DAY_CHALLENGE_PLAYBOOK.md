# CSL 7 天小挑战执行手册

## Day 0：提案

- 填写 `ACTION_CANVAS.md`。
- 复制推广文案草稿。
- 使用 Community Activity issue 模板提交提案。
- 等待维护者确认公开边界、未成年人边界和私有资料处理方式。

未确认前，不开始招募。

## Day 1：启动

- 向参与者说明活动目标、任务、公开边界和撤回路径。
- 只收集完成活动所需的最少信息。
- 如涉及 14–17 岁参与者，先完成监护确认。
- 分配随机编号或公开别名。

## Day 2–4：观察或共创

- 参与者完成低门槛观察、主观评分、文字反思或小组共创。
- 原始记录、联系方式、授权记录和未审素材保存在私有空间。
- 不把原始记录直接提交到 GitHub。

## Day 5：整理

- 将材料整理为匿名摘要、聚合表、协议更新、Rubric 或展示草稿。
- 删除姓名、联系方式、精确位置、学校班级、家庭信息和可识别第三方。
- 不默认公开个人页、音频、图片或学生作品。

## Day 6：审阅

- 对照 `PUBLIC_BOUNDARY.md` 检查公开成果。
- 核对授权状态和撤回映射。
- 涉及音频时，确认无可辨识对话；未成年人原音频不公开。
- 未通过审阅的材料留在私有空间或删除。

## Day 7：复盘

- 输出一页复盘：完成了什么、哪里卡住、哪些材料可复用、哪些风险需要下轮处理。
- 决定是否进入 OCPC 项目草案包。
- 如进入项目包，使用 Toolkit 创建草案，保持 `publication_review.status = draft`，直到公开审阅通过。

## 活动后命令

```bash
python scripts/ocpc_toolkit.py scaffold your-activity-id --title "活动标题" --output projects/your-activity-id
python scripts/ocpc_toolkit.py validate projects/your-activity-id
```

只有在公开成果完成审阅后，才考虑 render 或发布。
