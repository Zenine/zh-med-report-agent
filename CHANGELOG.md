# Changelog

> 已完成事项归档，按日期倒序。当前待办见 `TODO.md`。

---

## 2026-07-27

### 项目路线升级为通用医疗 Agent

- 更新 README：项目定位从单场景化验单助手升级为“通用医疗 Agent 底座 + 配置化场景适配 + 医疗数字人驱动层”。
- 新增 `TODO.md`：拆分 M2 通用医疗 Agent 底座、公司技术展示内容、M3 医疗数字人驱动层和后续场景扩展候选。
- 新增 `docs/architecture.md`、`docs/scenario-config-spec.md`、`docs/digital-human-layer.md`，记录后续需要新建 / 修改的架构模块和边界。

---

## 2026-07-25

### M1 地基完成

- 建仓并推送至 GitHub。
- 完成 README v0、10 条化验单 / 体检报告任务、rubric v0、最小 LangGraph agent loop 和 3 个真实 commit。
- 端到端跑通 case 0 代谢综合征和 case 1 危急值低钾，输出存档到 `examples/`。
