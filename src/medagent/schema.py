"""Structured output schemas for medical agent responses."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    NORMAL = "normal"


class Indicator(BaseModel):
    name: str = Field(description="指标名称，如「空腹血糖」「糖化血红蛋白」")
    value: str = Field(description="检测值，含单位")
    reference_range: str = Field(description="参考范围")
    is_abnormal: bool = Field(description="是否异常")
    severity: RiskLevel = Field(description="异常严重程度")
    clinical_note: str = Field(description="临床意义简述")


class FollowUpQuestion(BaseModel):
    question: str = Field(description="需要追问的问题")
    reason: str = Field(description="为什么需要这个信息")
    priority: RiskLevel = Field(description="追问优先级")


class Citation(BaseModel):
    claim: str = Field(description="结论/建议内容")
    source: str = Field(description="引用来源")
    supported: bool = Field(description="引用是否充分支撑该结论")


class HandoffContext(BaseModel):
    reason: str = Field(description="转人工/就医原因")
    urgency: RiskLevel = Field(description="紧急程度")
    key_findings: list[str] = Field(description="需要告知医生的关键发现")
    suggested_department: Optional[str] = Field(default=None, description="建议科室")


class LayeredAdvice(BaseModel):
    explanation: str = Field(description="医学解释：指标含义的通俗说明")
    lifestyle: Optional[str] = Field(default=None, description="生活方式建议")
    recheck: Optional[str] = Field(default=None, description="复查建议")
    seek_care_signal: Optional[str] = Field(default=None, description="就医信号")


class AgentResponse(BaseModel):
    indicators: list[Indicator] = Field(description="识别到的指标列表")
    overall_risk: RiskLevel = Field(description="综合风险等级")
    advice: LayeredAdvice = Field(description="分层建议")
    follow_up_needed: bool = Field(description="是否需要追问更多信息")
    follow_up_questions: list[FollowUpQuestion] = Field(
        default_factory=list, description="追问问题列表"
    )
    citations: list[Citation] = Field(default_factory=list, description="引用列表")
    handoff: Optional[HandoffContext] = Field(
        default=None, description="人工接管上下文（仅高风险时）"
    )
    disclaimer: str = Field(
        default="本分析仅供参考，不构成医疗诊断或治疗建议。如有疑虑请及时就医。",
        description="免责声明",
    )
