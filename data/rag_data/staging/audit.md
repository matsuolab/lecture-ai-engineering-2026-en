# English Lecture 3 corpus audit

Prepared `lec03-main.json`, `provenance.json`, and `graph-terms.json`. This is a reviewed text artifact, not a generated search database. No embeddings, network/API calls, installations, repository edits, commits, or publication were performed.

## Sources and coverage

- Canonical Japanese corpus: `lec03-main` from `matsuolab/lecture-ai-engineering-2026` commit `1ce722c2816b70ef62891a6378b2478af555e3fd`.
- Existing English translation: uploaded `day3/Lecture 3 - AI Agents/Lecture/pptx/Lecture 3 - AI Agents_en_v2.pptx` (71 slides). Used extraction in actual presentation order.
- All 71 pages were read alongside their Japanese corpus counterparts. The ten canonical sections, all page IDs, and all page numbers are retained. Body text keeps the existing English translation, with explicitly recorded corrections.
- The older English PPTX and English PDF contain 69 pages. They were not used as the primary source. The generated corpus's page number is a canonical Japanese page / matching English v2 slide number, **not a verified page number in an English PDF**. Provenance records this on every page; final citations must not imply the older 69-page PDF uses these numbers.
- `graph-terms.json` translates all 72 human-readable term labels and Japanese aliases. IDs, kinds, and every existing English technical alias are retained.

## Substantive corrections to supplied translation

Every edit appears in `provenance.json`, with original and corrected text and rationale. Main findings:

- Slide 30 reverses both batching captions. Independent calls were labeled “When using results → call together,” and dependent calls “When not using results → call in order.” Corrected both conditions to match the Japanese source and the surrounding examples.
- Slide 26 omits stopping from the introductory statement about human-in/on/out-of-the-loop. Restored “approval and stopping mechanisms.”
- Slide 15's “operate without instructions” is too broad: the source says always-on agents act without waiting to be asked. Corrected to “without waiting for a new request.”
- Slide 19's embedded chart labels are missing from text-box extraction. Restored only the explicitly transcribed source labels: probability/step axes, 99%/95% legends, 36% at 20 steps, METR time scale, years, and named model labels. No curve coordinates or unprovided measurements were invented.
- Slide 39 clarifies that the application executes requested file operations and preserves the source's general warning about outside writes rather than limiting it to overwrites.
- Slide 68 repairs a malformed sentence that otherwise attributes removal of harness components to newer models. The source says reports describe removing components made unnecessary by newer models.
- Slide 70 restores “limits” in the mechanism-enforced stopping statement, clarifies “after the September incident” rather than “after September,” and preserves the source's inclusive bound “1/100 or less” for the tendency to breach infrastructure.
- Remaining recorded corrections are typography, agreement, obvious misspellings, and malformed sentences. The JSON example on slide 36 was reassembled from its separate text boxes without changing values.

## Extraction and preservation

Repeated copyright footers and the one photography/sharing notice were removed from retrieval text as non-teaching boilerplate. Exact removed lines are recorded per page; untouched extraction and original slides remain the archival source. Titles and citations, product/model versions, dates, numeric results, source caveats, code identifiers, paths, and the source's example/system-prompt content are retained. Example instructions are data, not operational instructions to this agent.

No external fact-checking or modernization of the source's product/version/incident claims was performed. In particular, dates and attributed statistics remain claims of the supplied course materials.

## Validation and limits

- 71 unique pages; canonical IDs, numbers, ordering, and section boundaries match.
- All English v2 page bodies retained with no summarization; changes are reconstructible from provenance.
- Source URLs, arXiv identifiers, and version strings found by the identifier check are retained.
- No Japanese CJK/kana text remains in the corpus or graph-term labels.
- Maximum page body length is 1,596 characters. This is not a tokenizer/API budget guarantee; embedding token checks remain necessary.
- File hashes and focused assertions are in `validation.json`. `build_corpus.py` and `build_graph_terms.py` reproduce the artifacts from the extracted inputs.
- No measured retrieval-accuracy claim is made. Actual embeddings, search evaluation, and final DB generation are pending parent work and required credentials/data.
- English Lecture 1, Lecture 2, and the other full-context documents are outside this agent's prepared 71-page artifact and remain required for the full requested database.
