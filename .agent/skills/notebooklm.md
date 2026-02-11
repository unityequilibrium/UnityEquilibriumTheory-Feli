1. refresh_auth
Reload auth tokens from disk or run headless re-authentication. Call this after running notebooklm-mcp-auth to pick up new tokens, or to attempt automatic re-authentication if Chrome profile has saved login. Returns status indicating if tokens were refreshed successfully.
2. notebook_list
List all notebooks. Args: max_results: Maximum number of notebooks to return (default: 100)
3. notebook_create
Create a new notebook. Args: title: Optional title for the notebook
4. notebook_get
Get notebook details with sources. Args: notebook_id: Notebook UUID
5. notebook_describe
Get AI-generated notebook summary with suggested topics. Args: notebook_id: Notebook UUID Returns: summary (markdown), suggested_topics list
6. source_describe
Get AI-generated source summary with keyword chips. Args: source_id: Source UUID Returns: summary (markdown with **bold** keywords), keywords list
7. source_get_content
Get raw text content of a source (no AI processing). Returns the original indexed text from PDFs, web pages, pasted text, or YouTube transcripts. Much faster than notebook_query for content export. Args: source_id: Source UUID Returns: content (str), title (str), source_type (str), char_count (int)
8. notebook_add_url
Add URL (website or YouTube) as source. Args: notebook_id: Notebook UUID url: URL to add
9. notebook_add_text
Add pasted text as source. Args: notebook_id: Notebook UUID text: Text content to add title: Optional title
10. notebook_add_drive
Add Google Drive document as source. Args: notebook_id: Notebook UUID document_id: Drive document ID (from URL) title: Display title doc_type: doc|slides|sheets|pdf
11. notebook_query
Ask AI about EXISTING sources already in notebook. NOT for finding new sources. Use research_start instead for: deep research, web search, find new sources, Drive search. Args: notebook_id: Notebook UUID query: Question to ask source_ids: Source IDs to query (default: all) conversation_id: For follow-up questions timeout: Request timeout in seconds (default: from env NOTEBOOKLM_QUERY_TIMEOUT or 120.0)
12. notebook_delete
Delete notebook permanently. IRREVERSIBLE. Requires confirm=True. Args: notebook_id: Notebook UUID confirm: Must be True after user approval
13. notebook_rename
Rename a notebook. Args: notebook_id: Notebook UUID new_title: New title
14. chat_configure
Configure notebook chat settings. Args: notebook_id: Notebook UUID goal: default|learning_guide|custom custom_prompt: Required when goal=custom (max 10000 chars) response_length: default|longer|shorter
15. source_list_drive
List sources with types and Drive freshness status. Use before source_sync_drive to identify stale sources. Args: notebook_id: Notebook UUID
16. source_sync_drive
Sync Drive sources with latest content. Requires confirm=True. Call source_list_drive first to identify stale sources. Args: source_ids: Source UUIDs to sync confirm: Must be True after user approval
17. source_delete
Delete source permanently. IRREVERSIBLE. Requires confirm=True. Args: source_id: Source UUID to delete confirm: Must be True after user approval
18. research_start
Deep research / fast research: Search web or Google Drive to FIND NEW sources. Use this for: "deep research on X", "find sources about Y", "search web for Z", "search Drive". Workflow: research_start -> poll research_status -> research_import. Args: query: What to search for (e.g. "quantum computing advances") source: web|drive (where to search) mode: fast (~30s, ~10 sources) | deep (~5min, ~40 sources, web only) notebook_id: Existing notebook (creates new if not provided) title: Title for new notebook
19. research_status
Poll research progress. Blocks until complete or timeout. Args: notebook_id: Notebook UUID poll_interval: Seconds between polls (default: 30) max_wait: Max seconds to wait (default: 300, 0=single poll) compact: If True (default), truncate report and limit sources shown to save tokens. Use compact=False to get full details. task_id: Optional Task ID to poll for a specific research task.
20. research_import
Import discovered sources into notebook. Call after research_status shows status="completed". Args: notebook_id: Notebook UUID task_id: Research task ID source_indices: Source indices to import (default: all)
21. audio_overview_create
Generate audio overview. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) format: deep_dive|brief|critique|debate length: short|default|long language: BCP-47 code (en, es, fr, de, ja) focus_prompt: Optional focus text confirm: Must be True after user approval
22. video_overview_create
Generate video overview. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) format: explainer|brief visual_style: auto_select|classic|whiteboard|kawaii|anime|watercolor|retro_print|heritage|paper_craft language: BCP-47 code (en, es, fr, de, ja) focus_prompt: Optional focus text confirm: Must be True after user approval
23. studio_status
Check studio content generation status and get URLs. Args: notebook_id: Notebook UUID
24. studio_delete
Delete studio artifact. IRREVERSIBLE. Requires confirm=True. Args: notebook_id: Notebook UUID artifact_id: Artifact UUID (from studio_status) confirm: Must be True after user approval
25. infographic_create
Generate infographic. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) orientation: landscape|portrait|square detail_level: concise|standard|detailed language: BCP-47 code (en, es, fr, de, ja) focus_prompt: Optional focus text confirm: Must be True after user approval
26. slide_deck_create
Generate slide deck. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) format: detailed_deck|presenter_slides length: short|default language: BCP-47 code (en, es, fr, de, ja) focus_prompt: Optional focus text confirm: Must be True after user approval
27. report_create
Generate report. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) report_format: "Briefing Doc"|"Study Guide"|"Blog Post"|"Create Your Own" custom_prompt: Required for "Create Your Own" language: BCP-47 code (en, es, fr, de, ja) confirm: Must be True after user approval
28. flashcards_create
Generate flashcards. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) difficulty: easy|medium|hard confirm: Must be True after user approval
29. quiz_create
Generate quiz. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) question_count: Number of questions (default: 2) difficulty: Difficulty level (default: medium) confirm: Must be True after user approval
30. data_table_create
Generate data table. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID description: Description of the data table to create source_ids: Source IDs (default: all) language: Language code (default: "en") confirm: Must be True after user approval
31. mind_map_create
Generate and save mind map. Requires confirm=True after user approval. Args: notebook_id: Notebook UUID source_ids: Source IDs (default: all) title: Display title confirm: Must be True after user approval
32. save_auth_tokens
Save NotebookLM cookies (FALLBACK method - try notebooklm-mcp-auth first!). IMPORTANT FOR AI ASSISTANTS: - First, run `notebooklm-mcp-auth` via Bash/terminal (automated, preferred) - Only use this tool if the automated CLI fails Args: cookies: Cookie header from Chrome DevTools (only needed if CLI fails) csrf_token: Deprecated - auto-extracted session_id: Deprecated - auto-extracted request_body: Optional - contains CSRF if extracting manually request_url: Optional - contains session ID if extracting manually