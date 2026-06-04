# 校园感知 Beta 公开发布检查清单

## 聚合页发布前

- [ ] 公开数据只含随机编号或获授权别名。
- [ ] 模糊分区不暴露精确位置或个人轨迹。
- [ ] 文字反思已删除姓名、联系方式、学校班级、住址和可识别第三方。
- [ ] 不比较不同手机的绝对 dB。
- [ ] 已核对撤回映射，公开资产可在 7 天内定位和删除。
- [ ] `publication_review.status` 仍为 `draft`，直到全部检查完成。

## 可选个人页发布前

- [ ] 参与者已单独授权个人页。
- [ ] 未满 18 岁参与者同时具备监护确认。
- [ ] 页面只含别名、去标识化图表和审阅后的文字。
- [ ] 未成年人页面不含原音频、可识别图片或精确位置。
- [ ] 成年人音频如需公开，每人最多 3 段、每段最多 10 秒，且无可辨识对话。

## Render 前

```bash
python scripts/ocpc_toolkit.py validate projects/campus-sensing-beta-2026-06
python scripts/ocpc_toolkit.py render projects/campus-sensing-beta-2026-06 --output .tmp-site
python -m unittest discover -s tests -v
```

- [ ] `.tmp-site` 人工检查通过。
- [ ] GitHub Actions 通过。
- [ ] release notes 写明真实修复、公开边界和免费 Beta 性质。

## 禁止表述

- 不写“付费验证已完成”。
- 不写“代表某学校/城市整体结论”。
- 不写“不同手机 dB 可横向比较”。
- 不写“未成年人音频已公开”。
- 不写未经授权的机构、学校或个人名称。
