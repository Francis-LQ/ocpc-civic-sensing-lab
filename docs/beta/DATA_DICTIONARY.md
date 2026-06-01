# 校园感知 Beta 数据字典

公开数据仅使用随机编号或公开别名。真实身份映射、同意记录、撤回日志和待审音频
属于私有主账本，不进入 GitHub。

| 字段 | 类型 | 是否公开 | 说明 |
| --- | --- | --- | --- |
| `participant_alias` | string | 审核后可公开 | 随机编号或获授权别名，不使用实名 |
| `zone` | string | 可公开 | 模糊分区，如入口区、学习区、活动区 |
| `time_window` | string | 可公开 | 时段，不使用精确到分钟的轨迹 |
| `measurement_method` | string | 可公开 | 家用工具、手机观察或参考设备演示 |
| `temperature_c` | number | 可公开 | 可留空 |
| `humidity_percent` | number | 可公开 | 可留空 |
| `light_lux` | number | 可公开 | 可留空 |
| `relative_db` | number | 可公开 | 仅用于同一设备内相对比较 |
| `soundscape_score_1_to_5` | integer | 可公开 | 主观声景评分 |
| `thermal_comfort_score_1_to_5` | integer | 可公开 | 主观热舒适评分 |
| `reviewed_note` | string | 审核后可公开 | 删除个人信息和精确位置后的短文字 |
| `audio_private_id` | string | 不公开 | 仅在私有主账本中关联待审音频 |
| `withdrawal_status` | string | 不公开 | 仅在私有主账本中记录撤回处理 |

## 解释限制

- 不比较不同手机的绝对 dB。
- 无仪器参与者可提交观察字段和主观评分。
- 跨设备结果只用于探索性展示，不用于健康、安全或政策结论。
