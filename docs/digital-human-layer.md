# 医疗数字人驱动层

## 定位

医疗数字人不是另一个医学判断模型，而是通用医疗 Agent 的展示和交互驱动层。

它负责：

- 把 Agent 的结构化输出转成适合口播的解释。
- 在信息不足时组织追问话术。
- 在高风险时生成清晰、克制、可执行的 handoff 话术。
- 为演示 UI 或语音 / 视频数字人提供稳定脚本。

它不负责：

- 绕过底层 Agent 的安全路由。
- 直接做诊断。
- 推荐具体药物或剂量。
- 独立生成与 Agent 输出冲突的医学结论。

## 输入

数字人层输入来自底层 Agent：

```json
{
  "scenario_id": "lab_report",
  "risk_level": "high",
  "summary": "...",
  "follow_up_questions": [],
  "citations": [],
  "handoff": {
    "reason": "...",
    "urgency": "high",
    "key_findings": []
  },
  "disclaimer": "..."
}
```

## 输出

```json
{
  "opening": "我先帮你把报告里最需要关注的地方说明一下。",
  "spoken_summary": "...",
  "followup_script": [],
  "handoff_script": "这个结果风险较高，建议你尽快联系医生或去急诊。",
  "visual_cards": [
    {
      "title": "关键异常",
      "body": "..."
    }
  ],
  "closing": "以上只是技术解释，不构成诊断或治疗建议。"
}
```

## Persona 配置

建议路径：

```text
configs/personas/default_medical_educator.yaml
```

核心字段：

- `role_name`：角色名。
- `tone`：语气。
- `reading_level`：面向患者、医生、运营展示或技术评审。
- `must_say`：必须说出的边界。
- `must_not_say`：禁止表达。
- `handoff_style`：高风险时的转人工风格。

## M3 最小实现

- 新建 `src/medagent/digital_human.py`。
- 支持 `render_turn(agent_response, persona_config)`。
- 先输出文本脚本和展示卡片，不接语音合成或视频驱动。
- 增加 `tests/test_digital_human.py`，验证高风险输出必须包含 handoff 和免责声明。
