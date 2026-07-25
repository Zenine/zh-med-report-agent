# Medical Agent Reliability Lab

面向中文医疗场景的高可靠 Agent 业务架构实验项目。

通过 Agentic RAG、引用交叉验证、安全路由、人工接管和 Badcase 驱动评测，验证医疗 Agent 在复杂问答中的可靠性边界。

> **本项目不是诊断系统。** 所有输出仅供研究和技术验证，不构成医疗建议。

## 场景：复杂化验单 / 体检报告联合解读

用户输入多份化验单或体检报告摘要，系统：

1. 识别异常指标及其临床意义
2. 发现信息不足时主动追问（年龄、病史、用药等）
3. 检索公开医学资料并绑定引用来源
4. 输出分层建议：医学解释 → 生活方式 → 复查建议 → 就医信号
5. 高风险场景触发人工接管 / 就医建议
6. **不给出确诊结论，不推荐具体药物剂量**

## 架构

```
用户输入 (化验单/体检报告摘要)
         │
         ▼
┌─────────────────┐
│   输入理解       │  解析指标名称、数值、单位、参考范围
│   指标抽取       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   风险判断       │  识别危急值、严重异常、多指标关联
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 高风险    常规
    │         │
    │         ▼
    │  ┌──────────────┐
    │  │  检索计划     │  决定查什么、查几次 (Agentic RAG, M3)
    │  └──────┬───────┘
    │         │
    │         ▼
    │  ┌──────────────┐
    │  │  引用校验     │  结论必须绑定引用，标记 unsupported_claim
    │  └──────┬───────┘
    │         │
    │         ▼
    │  ┌──────────────┐
    │  │  信息充分？   │
    │  └──────┬───────┘
    │    否 ↙   ↘ 是
    │   追问     输出生成
    │  (M2)       │
    │             ▼
    ▼      ┌──────────────┐
 安全路由  │  分层建议     │  解释 / 生活方式 / 复查 / 就医信号
    │      └──────────────┘
    ▼
 就医建议 / 人工接管
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

- 第一版只覆盖"复杂化验单/体检报告联合解读"单一场景
- 不做 SFT/LoRA、vLLM 深度优化、完整 EHR sandbox
- 数据全部为合成/脱敏/公开医学资料，不含真实患者数据
- 评测以 LLM-as-Judge + 人工复核为主，非临床验证

## License

MIT
