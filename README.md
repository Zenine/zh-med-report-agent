# Medical Agent Reliability Lab

面向中文医疗场景的高可靠通用医疗 Agent 业务架构实验项目。

项目目标不是做一个单点的化验单助手，而是从通用 Agent 抽象出“通用医疗 Agent”底座，再通过场景配置层适配复杂化验单 / 体检报告解读、智能导诊、用药咨询、随访宣教、患者招募预筛等不同医疗场景。上层可叠加医疗数字人驱动层，用于技术展示、交互体验、人工接管和合规边界说明。

当前 M1 已以“复杂化验单 / 体检报告联合解读”作为第一个验证场景，完成最小可运行 loop。后续 M2/M3 将围绕配置化场景适配、RAG citation、安全策略、评测闭环和数字人展示层展开。

通过 Agentic RAG、引用交叉验证、安全路由、人工接管和 Badcase 驱动评测，验证医疗 Agent 在复杂问答中的可靠性边界。

> **本项目不是诊断系统。** 所有输出仅供研究和技术验证，不构成医疗建议。

## 当前验证场景：复杂化验单 / 体检报告联合解读

用户输入多份化验单或体检报告摘要，系统：

1. 识别异常指标及其临床意义
2. 发现信息不足时主动追问（年龄、病史、用药等）
3. 检索公开医学资料并绑定引用来源
4. 输出分层建议：医学解释 → 生活方式 → 复查建议 → 就医信号
5. 高风险场景触发人工接管 / 就医建议
6. **不给出确诊结论，不推荐具体药物剂量**

## 路线

- **M1：单场景最小 loop**：输入理解、指标抽取、风险判断、结构化输出、危急值 handoff。
- **M2：通用医疗 Agent 底座**：抽出场景配置、任务 / rubric 配置、工具与知识源配置、安全策略、RAG citation、评测报告和 badcase 闭环。
- **M3：医疗数字人驱动层**：在底层 Agent 之上增加文本 / 语音交互编排、角色人设、追问策略、结果解释、handoff 触发和展示态 UI。

详细设计见：

- `docs/architecture.md`
- `docs/scenario-config-spec.md`
- `docs/digital-human-layer.md`
- `TODO.md`

## 架构

```
用户输入
         │
         ▼
┌─────────────────┐
│  场景配置加载    │  scenario / persona / safety / tools / rubric
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   输入理解       │  按场景解析输入、抽取关键信息
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  场景 Agent      │  分析 / 追问 / 工具调用 / RAG citation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   安全路由       │  非诊断、非处方、危急值、handoff
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 人工接管   结构化输出
    │         │
    └────┬────┘
         ▼
┌─────────────────┐
│ 医疗数字人驱动层 │  口播稿 / 追问话术 / 展示态 UI
└─────────────────┘
```

**M1 范围**：输入理解 → 指标抽取 → 风险判断 → 结构化输出。最小可运行 loop。

## 快速开始

```bash
# 安装依赖
pip install -e .

# 运行单个 case
python -m medagent.run --task datasets/lab_report_tasks.jsonl --case 0
```

## 项目结构

```
src/medagent/       # 核心代码
configs/            # 场景、persona、安全策略配置（M2）
datasets/           # 任务集 (JSONL)
rubrics/            # 评分标准
docs/               # 设计文档
reports/            # 评测报告
safety_policies/    # 安全策略
examples/           # 示例输入输出
```

## 关键词

High-reliability Medical Agent · Agentic RAG · Anti-Hallucination · Citation Verification · Safety Boundary · Human Handoff · Badcase-driven Development · Rubric-first Evaluation

## 已知边界

- 当前运行时代码仍只覆盖"复杂化验单/体检报告联合解读"单一场景
- 智能导诊、用药咨询、随访宣教、患者招募预筛暂为配置化适配目标，不包装成已完成能力
- 医疗数字人层先作为 Agent 驱动和展示层，不作为临床服务入口
- 不做 SFT/LoRA、vLLM 深度优化、完整 EHR sandbox
- 数据全部为合成/脱敏/公开医学资料，不含真实患者数据
- 评测以 LLM-as-Judge + 人工复核为主，非临床验证

## License

MIT
