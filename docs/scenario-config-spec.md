# 场景配置规范

## 目的

通过配置让同一个通用医疗 Agent 底座适配不同医疗场景，避免把每个场景写成一套硬编码 prompt 和 schema。

## 配置文件

建议路径：

```text
configs/scenarios/<scenario_id>.yaml
```

示例：

```yaml
id: lab_report
name: 复杂化验单 / 体检报告联合解读
version: "0.2.0"

input:
  type: free_text
  required_context:
    - age
    - sex
    - symptoms
    - medical_history
    - medication

capabilities:
  - extract_indicators
  - identify_abnormalities
  - risk_stratification
  - ask_followup_questions
  - cite_sources
  - generate_layered_advice
  - trigger_handoff

prompt:
  system_template: lab_report_system
  user_template: lab_report_user

schema:
  response_model: LabReportResponse

safety:
  policy: base_medical_policy
  critical_rules:
    - potassium_low
    - potassium_high
    - glucose_low
    - glucose_high

tools:
  retrieval:
    enabled: true
    sources:
      - public_guidelines
      - medical_encyclopedia
  calculators:
    enabled: false

rubric:
  file: rubrics/scenarios/lab_report.yaml
```

## 必填字段

- `id`：稳定场景 ID，用于 CLI、任务集、报告和日志。
- `name`：中文展示名。
- `input`：输入类型和必需上下文。
- `capabilities`：该场景允许使用的能力。
- `prompt`：prompt 模板引用。
- `schema`：输出模型。
- `safety`：安全策略和高风险规则。
- `rubric`：评测规则。

## 场景适配原则

- 配置只能开放能力，不能绕过通用医疗安全边界。
- 场景 prompt 可以更具体，但不能允许诊断、处方、具体剂量或对急症“观察即可”。
- 未接入工具或知识源时，必须显式标记为 disabled 或 placeholder。
- 场景输出必须包含 disclaimer、risk level、follow-up / handoff 字段。

## 第一批候选场景

- `lab_report`：复杂化验单 / 体检报告联合解读。
- `triage`：智能导诊。
- `medication_consult`：用药咨询。
- `followup_education`：随访宣教。
- `recruitment_prescreen`：患者招募预筛。

除 `lab_report` 外，其余场景在实现前只作为设计占位。
