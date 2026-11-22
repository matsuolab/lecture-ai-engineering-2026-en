"""Check index creation through retrieval using real SQLite and fixed vectors. No API calls."""

import json
from unittest.mock import Mock

import pytest

from app import retrieval
from scripts.build_rag_index import build_index


@pytest.fixture
def materials(tmp_path):
    source = tmp_path / "lectures.json"
    source.write_text(json.dumps([
        {"id": f"lec{n:02d}-main", "title": f"Lecture {n}", "content": [
            {"section": "Section", "content": [
                {"id": f"lec{n:02d}-main-p001", "title": f"Page {n}",
                 "page": 1, "content": f"Text {n}"}]}]}
        for n in (1, 2, 5)
    ], ensure_ascii=False), encoding="utf-8")
    return source, tmp_path / "index.sqlite3"


def test_built_index_can_be_searched(materials, monkeypatch):
    source, database = materials
    texts = []

    def embed(text, task):
        assert task == "RETRIEVAL_DOCUMENT"
        texts.append(text)
        return [1, 0] if "Text 1" in text else [0, 1]

    result = build_index(source, database, embedder=embed)
    assert result["pages"] == 2  # Lecture 05 materials are excluded from the search scope
    assert all("Section" in text and "Page" in text for text in texts)
    monkeypatch.setattr(retrieval, "RAG_DB", database)
    monkeypatch.setattr(retrieval, "embed_text", lambda *_: [1, 0])
    hits = retrieval.search("Question")
    assert [h["page_id"] for h in hits] == ["lec01-main-p001", "lec02-main-p001"]
    assert hits[0]["content"] == "Text 1"
    assert hits[0]["distance"] == pytest.approx(0)


def test_adjacent_page_expansion_deduplicates_and_stays_within_document():
    pages = [
        {"page_id": "doc1-p001", "document_id": "doc1", "page": 1,
         "content": "one", "citation": "Doc 1 p.1"},
        {"page_id": "doc1-p002", "document_id": "doc1", "page": 2,
         "content": "two", "citation": "Doc 1 p.2"},
        {"page_id": "doc1-p003", "document_id": "doc1", "page": 3,
         "content": "three", "citation": "Doc 1 p.3"},
        {"page_id": "doc1-p004", "document_id": "doc1", "page": 4,
         "content": "four", "citation": "Doc 1 p.4"},
        {"page_id": "doc2-p001", "document_id": "doc2", "page": 1,
         "content": "other document", "citation": "Doc 2 p.1"},
    ]
    hits = [
        {"page_id": "doc1-p002", "document_id": "doc1", "distance": 0.1},
        {"page_id": "doc1-p004", "document_id": "doc1", "distance": 0.2},
    ]

    expanded = retrieval.expand_adjacent_pages(hits, pages)

    assert [page["page_id"] for page in expanded] == [
        "doc1-p002", "doc1-p004", "doc1-p001", "doc1-p003"
    ]
    assert expanded[:2] == hits
    assert expanded[2]["content"] == "one"
    assert expanded[2]["citation"] == "Doc 1 p.1"
    assert expanded[2]["adjacent"] is True
    assert expanded[2]["adjacent_to"] == "doc1-p002"
    assert expanded[3]["adjacent"] is True
    assert expanded[3]["adjacent_to"] == "doc1-p002"
    assert "doc2-p001" not in [page["page_id"] for page in expanded]


def test_existing_index_survives_failed_rebuild(materials):
    source, database = materials
    build_index(source, database, embedder=lambda *_: [1, 0])
    before = database.read_bytes()
    embed = Mock(side_effect=RuntimeError("Embedding failed"))
    with pytest.raises(FileExistsError):
        build_index(source, database, embedder=embed)
    embed.assert_not_called()
    with pytest.raises(RuntimeError, match="Embedding failed"):
        build_index(source, database, rebuild=True, embedder=embed)
    assert database.read_bytes() == before
    assert not list(database.parent.glob(".rag-build-*"))
