from types import SimpleNamespace

from app import ask as ask_module


def test_ask_displays_token_counts_and_elapsed_time(monkeypatch, capsys):
    response = SimpleNamespace(
        text="A low-rank adaptation.",
        usage_metadata=SimpleNamespace(prompt_token_count=8, candidates_token_count=5),
    )
    monkeypatch.setattr(
        ask_module.genai,
        "Client",
        lambda **kwargs: SimpleNamespace(
            models=SimpleNamespace(generate_content=lambda **kwargs: response)
        ),
    )
    ticks = iter([2.0, 3.25])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(ticks))

    assert ask_module.ask("What is LoRA?") == response.text
    assert capsys.readouterr().out == (
        "[metrics] elapsed=1.25s input_tokens=8 output_tokens=5\n"
    )


def test_ask_passes_requested_temperature(monkeypatch):
    response = SimpleNamespace(text="Answer", usage_metadata=None)
    calls = []

    def generate_content(**kwargs):
        calls.append(kwargs)
        return response

    monkeypatch.setattr(
        ask_module.genai,
        "Client",
        lambda **kwargs: SimpleNamespace(
            models=SimpleNamespace(generate_content=generate_content)
        ),
    )
    ticks = iter([0.0, 0.1])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(ticks))

    ask_module.ask("What is LoRA?", temperature=0.7)

    assert calls[0]["config"].temperature == 0.7


def test_chat_reuses_conversation_for_follow_up_questions(monkeypatch, capsys):
    conversation = SimpleNamespace(
        sent_messages=[],
    )
    chat_creations = []

    def send_message(question):
        conversation.sent_messages.append(question)
        return SimpleNamespace(
            text=f"Answer to {question}",
            usage_metadata=SimpleNamespace(
                prompt_token_count=4, candidates_token_count=3
            ),
        )

    conversation.send_message = send_message
    monkeypatch.setattr(
        ask_module.genai,
        "Client",
        lambda **kwargs: SimpleNamespace(
            chats=SimpleNamespace(
                create=lambda **kwargs: chat_creations.append(kwargs) or conversation,
            )
        ),
    )
    questions = iter(["What is LoRA?", "What does low-rank mean?", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))
    ticks = iter([0.0, 0.5, 1.0, 1.75])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(ticks))

    ask_module.chat(temperature=0.3)

    assert conversation.sent_messages == [
        "What is LoRA?",
        "What does low-rank mean?",
    ]
    assert len(chat_creations) == 1
    output = capsys.readouterr().out
    assert output.count("[metrics]") == 2
    assert "Answer to What does low-rank mean?" in output
