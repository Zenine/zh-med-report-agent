# 通用医疗 Agent 架构

## 目标

本项目从单场景化验单 / 体检报告解读，升级为可配置的通用医疗 Agent 底座。

核心判断：

- 底层是通用 Agent 能力：状态机、工具调用、RAG、评测、安全路由和人工接管。
- 医疗层是通用医疗安全与合规边界：非诊断、非处方、危急值、急症、特殊人群和 handoff。
- 场景层通过配置适配：复杂化验单、智能导诊、用药咨询、随访宣教、患者招募预筛。
- 展示层可叠加医疗数字人：负责表达、追问、播报、引导和展示态 UI，不负责最终医学判断。

## 分层

```text
User Input
  |
  v
Scenario Config Loader
  - scenario
  - persona
  - safety policy
  - tool policy
  - rubric
  |
  v
Universal Medical Agent Core
  - input understanding
  - planning
  - tool / retrieval calls
  - structured analysis
  - citation binding
  |
  v
Medical Safety Router
  - non-diagnosis boundary
  - non-prescription boundary
  - critical value detection
  - emergency / handoff trigger
  |
  v
Scenario Response
  - structured payload
  - follow-up questions
  - citations
  - handoff context
  |
  v
Digital Human Driver Layer
  - spoken explanation
  - guided follow-up
  - visual summary
  - human handoff script
```

## 当前代码问题

当前 M1 代码仍是硬编码单场景：

- `src/medagent/prompts.py` 写死化验单 / 体检报告 prompt。
- `src/medagent/schema.py` 的 `AgentResponse` 写死指标列表和分层建议。
- `src/medagent/agent.py` 的 graph 只有 parse / analyze / handoff / output。
- `src/medagent/run.py` 只支持 `--task` 和 `--case`，不支持 `--scenario`。
- `datasets/` 与 `rubrics/` 没有多场景目录结构。

## M2 改造后目标结构

```text
configs/
  scenarios/
    lab_report.yaml
    triage.yaml
    medication_consult.yaml
    followup_education.yaml
    recruitment_prescreen.yaml
  personas/
    default_medical_educator.yaml
  safety/
    base_medical_policy.yaml
datasets/
  scenarios/
    lab_report_tasks.jsonl
rubrics/
  scenarios/
    base_medical_agent.yaml
    lab_report.yaml
src/medagent/
  agent.py
  config.py
  scenario.py
  safety.py
  retrieval.py
  evaluator.py
  digital_human.py
  prompts.py
  schema.py
  run.py
tests/
  test_config.py
  test_scenario_registry.py
  test_safety.py
  test_lab_report_agent.py
  test_digital_human.py
```

## 边界

- 不接真实患者数据。
- 不替代医生诊断或治疗决策。
- 不推荐具体药物或剂量。
- 不把未完成场景包装成已完成能力。
- 数字人层只做 Agent 输出的表达和交互驱动，不直接绕过安全路由。
