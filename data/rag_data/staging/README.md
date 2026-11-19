# Partial preparation for the localized search corpus

This directory contains reviewed text for Lecture 03 (71 pages), its exercises (26 pages), and Lecture 04 exercises (23 pages). It also contains 72 localized graph-term labels and page-level provenance.

The corpus is incomplete. Lecture 01 and Lecture 02 main materials are still required for the 214-page search index; the other documents listed in manifest.json are needed for the complete 438-page full-context corpus. Embeddings and index.sqlite3 have not been generated, and retrieval accuracy has not yet been measured. These files are retained for review and must not be treated as a ready-to-run database release.

Page IDs and page fields follow the pinned Japanese master. Actual uploaded translated-slide numbers are recorded separately in provenance; newly translated source additions may have no corresponding page in the supplied translated deck. Do not present canonical Japanese page numbers as translated PDF page numbers.

Before release: obtain the remaining translated source materials, assemble the complete corpus/tree/graph, propagate accurate citation metadata, create fresh embeddings with the same model used for query search, and run retrieval checks. Keep the existing main branch unchanged until the full data/code update is ready.
