"""Minimal medical agent loop using LangGraph."""

from __future__ import annotations

import os
from typing import Any, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from medagent.prompts import SYSTEM_PROMPT
from medagent.schema import AgentResponse, RiskLevel


class AgentState(TypedDict):
    report_text: str
    messages: list[Any]
    parsed_response: dict | None
    risk_level: str | None
    needs_handoff: bool


def build_llm(
    model: str | None = None,
    temperature: float = 0.1,
    base_url: str | None = None,
) -> ChatOpenAI:
    model = model or os.environ.get("MEDAGENT_MODEL", "gpt-4o-mini")
    base_url = base_url or os.environ.get("OPENAI_API_BASE")
    kwargs: dict[str, Any] = {"model": model, "temperature": temperature}
    if base_url:
        kwargs["base_url"] = base_url
    return ChatOpenAI(**kwargs)


def parse_input(state: AgentState) -> AgentState:
    report = state["report_text"]
    state["messages"] = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"请分析以下化验单/体检报告：\n\n{report}"),
    ]
    return state


def analyze(state: AgentState) -> AgentState:
    llm = build_llm()
    structured_llm = llm.with_structured_output(AgentResponse)
    response: AgentResponse = structured_llm.invoke(state["messages"])
    state["parsed_response"] = response.model_dump()
    state["risk_level"] = response.overall_risk.value
    state["needs_handoff"] = response.overall_risk in (RiskLevel.CRITICAL, RiskLevel.HIGH)
    return state


def check_handoff(state: AgentState) -> str:
    if state.get("needs_handoff"):
        return "handoff"
    return "output"


def format_handoff(state: AgentState) -> AgentState:
    resp = state["parsed_response"]
    if resp and not resp.get("handoff"):
        resp["handoff"] = {
            "reason": "综合风险等级较高，建议及时就医",
            "urgency": state["risk_level"],
            "key_findings": [
                ind["clinical_note"]
                for ind in resp.get("indicators", [])
                if ind.get("is_abnormal")
            ],
            "suggested_department": None,
        }
    return state


def format_output(state: AgentState) -> AgentState:
    return state


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("parse_input", parse_input)
    graph.add_node("analyze", analyze)
    graph.add_node("format_handoff", format_handoff)
    graph.add_node("format_output", format_output)

    graph.set_entry_point("parse_input")
    graph.add_edge("parse_input", "analyze")
    graph.add_conditional_edges("analyze", check_handoff, {"handoff": "format_handoff", "output": "format_output"})
    graph.add_edge("format_handoff", END)
    graph.add_edge("format_output", END)

    return graph.compile()


def run_case(report_text: str) -> dict:
    """Run the agent on a single lab report case and return structured output."""
    app = build_graph()
    initial_state: AgentState = {
        "report_text": report_text,
        "messages": [],
        "parsed_response": None,
        "risk_level": None,
        "needs_handoff": False,
    }
    result = app.invoke(initial_state)
    return result["parsed_response"]
