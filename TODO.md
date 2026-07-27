# TODO

> 只保留尚未完成、可执行、可验收的事项。完成项移入 `CHANGELOG.md`。

## M2：通用医疗 Agent 底座

- 新建 `configs/scenarios/lab_report.yaml`，把当前化验单 / 体检报告场景从硬编码 prompt 迁移为场景配置。
- 新建 `src/medagent/config.py`，加载 scenario、persona、safety、tools 和 rubric 配置。
- 新建 `src/medagent/scenario.py`，定义 `MedicalScenario` 与场景注册机制。
- 重构 `src/medagent/agent.py`：`run_case(input_text, scenario_id="lab_report")` 支持按场景配置构建 prompt、schema、工具和安全规则。
- 拆分 `src/medagent/prompts.py`：保留通用医疗 Agent 系统边界，把场景 prompt 移到配置或模板。
- 扩展 `src/medagent/schema.py`：增加通用 `MedicalAgentResponse`、场景 payload、`SafetyDecision` 和 `DigitalHumanTurn`。
- 新建 `src/medagent/safety.py`：统一处理非诊断、非处方、危急值、急症、未成年人 / 孕产妇等安全边界和 handoff。
- 新建 `src/medagent/retrieval.py`：提供 RAG citation baseline 的接口占位和本地公开资料检索占位。
- 新建 `src/medagent/evaluator.py`：按 rubric 评估输出，记录 badcase taxonomy 和能力缺口标签。
- 将 `datasets/lab_report_tasks.jsonl` 迁移或镜像到 `datasets/scenarios/lab_report_tasks.jsonl`，为后续多场景任务集做目录隔离。
- 将 `rubrics/lab_report_rubrics.yaml` 迁移或镜像到 `rubrics/scenarios/lab_report.yaml`，并新增 `rubrics/scenarios/base_medical_agent.yaml`。
- 新增测试：`tests/test_config.py`、`tests/test_scenario_registry.py`、`tests/test_safety.py`、`tests/test_lab_report_agent.py`。
- 更新 CLI：`python -m medagent.run --scenario lab_report --case 0`。

## M2 展示与公司技术内容

- 输出 `docs/demo-script.md`，沉淀公司技术展示口径：问题背景、架构图、能力边界、演示流程、风险说明、非诊断免责声明。
- 输出 `reports/m2-lab-report-evaluation.md`，记录任务集、通过情况、badcase、修复项和剩余风险。
- 保留可公开 / 不可公开材料清单，确保不包含真实患者数据、客户隐私或内部敏感材料。

## M3：医疗数字人驱动层

- 新建 `src/medagent/digital_human.py`，把 Agent 输出转成数字人可播报话术、追问话术和 handoff 话术。
- 新建 `configs/personas/default_medical_educator.yaml`，定义数字人角色、人设、语气、禁区和解释风格。
- 新建 `docs/digital-human-layer.md` 的演示流程样例，说明数字人只是 Agent 驱动 / 展示层，不替代底层医学判断。
- 先实现文本 / 语音脚本输出，不先接入真实语音合成、视频驱动或临床工作流。

## 场景扩展候选

- `triage`：智能导诊，重点验证多轮追问、科室建议、急症识别和 handoff。
- `medication_consult`：用药咨询，重点验证拒绝具体处方 / 剂量、相互作用风险提示和医生 / 药师接管。
- `followup_education`：随访宣教，重点验证解释、复查提醒、生活方式建议和边界。
- `recruitment_prescreen`：患者招募预筛，重点验证纳排标准解释、信息缺口追问和人工研究者接管。

这些场景在完成前只作为配置化适配目标，不写成已完成能力。
