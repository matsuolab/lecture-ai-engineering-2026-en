"""Agent wiring tests.

TestModel is a fake model that calls all registered tools and returns a dummy answer
without calling a real LLM. Check that tools are registered, called, and return results
to the model, without using an API key or consuming usage allowances.
"""

import json

from pydantic_ai import DeferredToolRequests
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.test import TestModel

from app.agent import agent

BASE_TOOLS = {"search_materials"}


def _parts(result, kind):
    return [p for m in result.all_messages() for p in m.parts if isinstance(p, kind)]


def test_base_tools_are_registered_and_called(monkeypatch):
    monkeypatch.setattr("app.retrieval.search", lambda *args, **kwargs: [])
    model = TestModel()
    with agent.override(model=model):
        result = agent.run_sync("What is LoRA?")

    offered = {t.name for t in model.last_model_request_parameters.function_tools}
    assert BASE_TOOLS <= offered  # Check inclusion so adding tools in the exercises does not break the test

    called = {p.tool_name for p in _parts(result, ToolCallPart)}
    assert BASE_TOOLS <= called
    # Tools requiring approval (requires_approval=True) wait for approval without running, so they have no return value
    waiting = len(result.output.approvals) if isinstance(result.output, DeferredToolRequests) else 0
    assert len(_parts(result, ToolReturnPart)) + waiting == len(_parts(result, ToolCallPart))
    assert result.output


def test_material_result_reaches_the_model(monkeypatch):
    hit = {"page_id": "lec02-main-p052", "lecture": 2, "page": 52, "content": "The original weights are frozen"}
    monkeypatch.setattr("app.retrieval.search", lambda *args, **kwargs: [hit])
    model = TestModel(call_tools=["search_materials"])
    with agent.override(model=model):
        result = agent.run_sync("What is RAG?")
    returns = _parts(result, ToolReturnPart)
    assert returns and returns[0].tool_name == "search_materials"
    assert json.loads(returns[0].content)["results"] == [hit]
