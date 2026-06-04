# 私有运营与公开发布边界

## 唯一事实来源

- 飞书：报名、文件上传和反馈入口。
- 本地加密目录：唯一私有主账本。每日导出后记录处理状态。
- GitHub：仅存放人工审核后的公开成果。

## 私有主账本最小结构

| 台账 | 用途 |
| --- | --- |
| `participant-index.csv` | 随机编号、年龄段和处理状态 |
| `identity-map.csv` | 身份映射，仅限负责人访问 |
| `consent-log.csv` | 参与、监护和公开授权 |
| `audio-review-log.csv` | 音频时长、审核、删除日期和公开状态 |
| `withdrawal-log.csv` | 撤回请求、公开资产映射和处理完成时间 |

空白表头模板保存在 `docs/beta/ledger-templates/`，只能作为本地加密目录的建表参考。
填写真实数据后的台账不得提交到 GitHub。

## 禁止进入 GitHub

- 身份映射、联系方式、年龄详情、精确位置和个人轨迹。
- 报名表、同意记录、撤回日志和待审音频。
- 未成年人原音频、可辨识对话和未经授权素材。

## 人工门禁

每次生成公开页前，先在私有主账本完成授权和撤回映射检查，再将审核后的公开包
交给 `ocpc_toolkit.py validate` 和 `render`。

`.gitignore` 已排除 `private-ledger/`、`beta-private/` 和项目包中的 `private/`、
`raw/`、`consent/`、`registration/`、`withdrawal/`、`audio-pending/` 等路径。
