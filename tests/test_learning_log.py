import json

import pytest
from pydantic_ai import DeferredToolRequests, DeferredToolResults
from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent


def test_save_log_writes_expected_content(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)

    tools.save_log(
        topic="LoRA",
        summary="LoRA trains small adapter matrices.",
    )

    files = list(tmp_path.glob("*.json"))
    assert len(files) == 1

    record = json.loads(files[0].read_text(encoding="utf-8"))
    assert record["topic"] == "LoRA"
    assert record["summary"] == "LoRA trains small adapter matrices."
    assert record["created_at"]


@pytest.mark.parametrize(
    "topic, summary",
    [
        ("", "A valid summary"),
        ("LoRA", ""),
        ("   ", "A valid summary"),
    ],
)
def test_save_log_rejects_empty_content(
    tmp_path, monkeypatch, topic, summary
):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)

    result = tools.save_log(topic=topic, summary=summary)

    assert "nonempty" in result
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("approved", [True, False])
def test_save_log_requires_approval(tmp_path, monkeypatch, approved):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)

    model = TestModel(call_tools=["save_log"])
    result = agent.run_sync("Save a learning record.", model=model)

    # The tool must not write anything before approval.
    assert isinstance(result.output, DeferredToolRequests)
    assert len(result.output.approvals) == 1
    assert not list(tmp_path.iterdir())

    call = result.output.approvals[0]
    assert call.tool_name == "save_log"

    agent.run_sync(
        model=model,
        message_history=result.all_messages(),
        deferred_tool_results=DeferredToolResults(
            approvals={call.tool_call_id: approved},
        ),
    )

    files = list(tmp_path.glob("*.json"))
    assert len(files) == (1 if approved else 0)