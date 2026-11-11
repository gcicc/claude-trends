# Claude Trends — Delta Report 2026-05-27

*Baseline: 2026-05-15 (`reports/claude-code-2026-features-youtube-research.md`). Analyzed 10 YouTube videos uploaded between 2026-05-18 and 2026-05-27. Window: 12 days.*

## Executive Summary

- **Routines shipped from Anthropic** — `/schedule` + GitHub webhook + Slack triggers turn Claude Code into a proactive teammate. This is the headline addition of the window; the baseline mentioned routines only in passing.
- **Managed Agents pricing is now public** — $0.08/hr compute + $1–3/action variable, plus a "5-pillar" architecture (Brain / Hands / Session / Memory / Dream). Baseline knew the feature existed; the *economics* and *architecture* are new.
- **MCP ecosystem visibly expanding** — Blender (official), Paper, BlueDot, ComfyUI, and Lemlist's 38-skill bundle all landed in this window. The "MCP is USB-C for AI" framing has hardened into consensus.
- **Hookify** — a community/Anthropic plugin that adds *conversation-aware* hooks (pattern-match on user intent, deny/allow with wildcards) — extends the static `settings.json` hooks model from baseline.
- **Workflow consensus is shifting** away from "fully autonomous agents" toward orchestration + plan-mode verification + memory stores. Multiple creators independently emphasized human-in-loop checkpoints.

---

## NEW Features / Releases

### Routines (Anthropic, official)
**Source:** eSP7PLTXNy8 (Anthropic channel, 22 min, 89K views)

- `/schedule` command creates time-based routines ("next Thursday 2pm"); event-triggered via GitHub webhooks (push, PR, issue open) and Slack messages.
- Context **mounts automatically** at trigger time — routine reads the current repo state, not a stale snapshot.
- **Steering** during execution: user can interrupt, redirect, or supply mid-run input.
- Positioned as "Claude reads your repo and opens a PR before you've opened your laptop." First-party feature, not a community plugin.
- Baseline mentioned routines as part of the `/schedule` skill but had no end-to-end walkthrough; this is the canonical reference now.

### Managed Agents — pricing and architecture (Anthropic, partner-tier)
**Source:** 5j6Vq52fgNU (Kacper Rutkiewicz, 33 min)

- **Pricing now public:** $0.08/hour compute + $1–3/action (variable by tool). A 10-min mixed-I/O run ≈ $4. *Source is a partner reseller, not Anthropic docs — treat as directional.*
- **"5 Pillars" framing:** Brain (model), Hands (sandboxed execution), Session (event log), Memory (persistent markdown stores), Dream (async reflection that consolidates memory between sessions).
- **Files API** powers credential vault and persistent env vars; sessions log every tool call for audit.
- **Memory stores** are markdown files that survive session boundaries — agents read/write project context across days. The "Dream" cycle re-summarizes memory while idle.
- New consultancy thesis: $5k install + $1.5k/mo retainer offer aimed at SMB clients. Treat as market positioning, not Anthropic pricing.

### Hookify (community/Anthropic plugin)
**Source:** tSIFk3YDsQo (Code With Sally, 1h11m)

- Hooks now support **pattern matching + conditional actions** in natural language. `/hookify` writes hook rules from a prompt.
- Example rules: if user mentions "testing," auto-allow Playwright CLI; deny any tool call whose path includes `secrets/`.
- **Precedence:** `settings.json` (project) > Hookify rules > `CLAUDE.md` instructions. This precedence ordering was not in baseline.
- The plugin coexists with the static deny-list hooks from baseline; it's an additive layer, not a replacement.
- `/update-config` skill (built-in) lets Claude *write its own* hook rules — meta-configuration loop.

### Knowledge Work Plugins (Anthropic, official marketplace bundle)
**Sources:** 0kDryeRcW1Q (short, description-only), reinforced by tNbGO68Opug

- 18 plugins for non-engineering departments: Sales (prospect research, pipeline), Finance (reconciliation, month-end close), Legal (contract review, NDA triage), Engineering (standups, incident response), Marketing (campaigns, brand voice), Data (SQL, dashboards), Bio Research (genomics, preclinical).
- Install path: `claude plugin marketplace add anthropic/knowledge-work-plugins` → `claude plugin install sales@knowledge-work-plugins`.
- Partner integrations bundled: Slack, Zoom, Figma, Zapier, Notion + 20 more.
- Plugins are file-based (markdown + JSON) — no code to author.
- Baseline noted the plugin marketplace existed; this is the first concrete first-party plugin bundle for non-developer users.

### Smaller items confirmed in this window
- **Claude Cowork** vs Claude Code distinction sharpened (cVmkq_aENr8): same engine, same agent, same files — split is desktop chat UX (Cowork) vs terminal+customization (Code). Baseline conflated them.
- **`/init`, `/recap`, `/btw`** still work as baseline described — multiple videos used them without comment, signaling stability.

---

## NEW Workflow Patterns

### Progressive disclosure for large codebases
**Source:** lGalJmyI78w (AI LABS, 14 min, 15K views)

- Keep root `CLAUDE.md` **≤ ~300 lines**; create per-subdirectory `CLAUDE.md` files for monorepos so context loads progressively as Claude descends into a folder.
- Skills should expose only frontmatter (name, description, trigger) at session start; full skill body loads on-demand. Reduces base context bloat.
- The harness (hooks + skills + plugins + sub-agents + LSP) **matters more than the model**. Same Opus 4.7 with bad harness underperforms Sonnet 4.6 with great harness.
- Anthropic's own [recent blog post](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start) (referenced in video) is the canonical source.
- New advice that contradicts baseline implicitly: **drop RAG-based code search**; use file-system tools (`ls`, `grep`, bash) like a human developer. RAG pollutes context with non-existent modules.

### Plan-mode verification loop for agents
**Sources:** Yb2j6C-TD2Q, 5j6Vq52fgNU

- Pattern: agent reads context → enters plan mode → asks clarifying questions (lead cap, cadence, enrichment strategy) → locks decisions → executes in stages.
- Lemlist's outbound campaign skill: agent never sends an email — it stages a *paused* campaign in the Lemlist UI for human approval.
- Quote (Othmane): *"This is nowhere near the famous AI SDR dream… this is smart orchestration."* The "orchestration ≠ autonomy" framing is the dominant rhetorical shift of the window.

### Memory store + reflection (DIY pattern)
**Source:** 5j6Vq52fgNU + 0eQ9qRFquBA (short)

- Pattern: at session end, agent summarizes what happened → extracts learnings → appends to markdown memory store. Next session reads memory before any tool call.
- "Sleep cycle" pattern: idle agents run a reflection job that consolidates the week's memories into a tighter summary. (Short video; verify before adopting.)

### Playwright CLI > Playwright MCP for testing
**Source:** tSIFk3YDsQo

- Playwright CLI is **cheaper on tokens** than the MCP equivalent (headed mode optional, headless default).
- Recommendation: use the CLI for testing-skill automation; reserve the MCP for general web-access tasks where discoverability matters.
- New trade-off framing not present in baseline.

---

## NEW Tools / MCPs / Integrations

| Tool / MCP | Source | What it does | Native vs adjacent |
|---|---|---|---|
| **Blender MCP** (official) | YwIGmEs0NdU | 3D modeling automation, animation retargeting, geometry nodes | Official Blender add-on |
| **Paper MCP** | OfoGGQ8ab7Y | Imports generated UI as *editable layers* in Paper canvas | Adjacent (paper.design) |
| **Leek Design API** + Sleek skill | OfoGGQ8ab7Y | 4-variant mobile UI generation from prompt | Adjacent |
| **BlueDot MCP** | zpfFmtENh2Q | Apple Watch tap → meeting recording → search/summarize | Adjacent (third-party) |
| **Lemlist Skills (38)** | Yb2j6C-TD2Q | Sales outreach orchestration; orchestrator skill open-source | Adjacent |
| **ComfyUI** | m7Fh3po0wE0 | Local VS Code setup + JSON workflow generation for image gen | Adjacent (open source) |
| **Composio plugin** | ULEgpAbugxg (short, low signal) | Claims 500+ tool integrations (GitHub, Slack, Gmail, Notion) | Adjacent — verify before using |
| **Claude-Mem plugin** | ULEgpAbugxg | Claims persistent memory across sessions | Adjacent — verify before using |
| **Context7 MCP** | tNbGO68Opug | Live library docs (already in your global MCP set) | Native ecosystem |

**BlueDot deserves a callout** — it's a proof-of-concept for hyperlocal MCPs (one device → one workflow). Pattern: custom connector in claude.ai → `/slash MCP` command → always-allow permissions → email/calendar cross-reference. Lowest-effort path from "I want X integrated" to a working MCP.

---

## Notable Applications

- **Sales motion in one prompt (Yb2j6C-TD2Q):** ICP + persona definer → People Database lookup → enrichment → angle picker → 3-message sequence → CTA rewrite → Lemlist UI staged for approval. Whole pipeline runs from a single Claude Code skill.
- **Anthropic-Maya routine (eSP7PLTXNy8):** Triggered by GitHub PR open → reads diff → posts review comment → optional auto-fix PR. End-to-end CI-like behavior without a separate CI runner.
- **Blender 1-hour autonomy run (YwIGmEs0NdU):** Four challenges — angel animation, geometry-node sludge, image-blaster automation, autonomous world builder. Skeletal retargeting succeeded on arms/legs (~90%) but failed on hands. Creator concluded vision model is weaker at spatial reasoning than Codex.
- **Meeting memory loop (zpfFmtENh2Q):** Apple Watch records in-person meeting → BlueDot MCP indexes → Routine emails daily summary to Gmail. End-to-end personal-knowledge automation.
- **Design-to-Paper pipeline (OfoGGQ8ab7Y):** Leek generates 4 styled HTML variants → Paper imports as layers (not raster) → designer iterates in Paper, code stays generated.

---

## Pricing / Cost shifts

- **Managed Agents:** $0.08/hr compute + $1–3/action (third-party-reported, 5j6Vq52fgNU).
- **ComfyUI image generation:** $0.05–0.67 per image via GPT-Image-2; batches of 100 land at $30–67 (m7Fh3po0wE0).
- **No changes** reported to Claude Code subscription tiers, Opus 4.7 per-token pricing, or the XI/max effort tier defaults — baseline numbers ($5/M input, $25/M output, ~35% effective inflation from new tokenizer) appear to still hold.
- One short (Hi66ZQLhHOM) cites a developer burning 62M Opus 4.7 tokens against a $2,500/month budget — anecdote, not a pricing change, but a signal that token-budget skills/hooks are an emerging need.

---

## Consensus shifts (vs 2026-05-15)

1. **Harness > model.** Strengthened. AI LABS, Kacper, and Sally all independently emphasize that hooks/skills/plugins/sub-agents around the model determine output quality more than the model itself.
2. **MCP is the universal integration layer.** Strengthened. Codingfab's 4-layer stack (MCP → Skills → Plugins → Agents) is now the prevailing mental model.
3. **Memory is foundational, not optional.** New consensus. Kacper places Memory on equal footing with Brain and Hands; multiple creators independently demo markdown memory stores.
4. **Plan mode + human verification > full automation.** New consensus. Direct rhetorical shift away from "AI SDR" autonomy framing.
5. **Local + cloud hybrid for compute-heavy workflows.** Emerging. Stefan (Blender, local GPU) and AI Aidan (ComfyUI, local VS Code) both prefer local execution with API calls only for the model.

## Contradictions vs baseline

1. **Vision capability is more uneven than baseline implied.**
   - Baseline (lzdmb_Z-yZc): 3× image resolution, parses small text in screenshots.
   - New (YwIGmEs0NdU): spatial reasoning for 3D rigging is weak; hands fail ~10% on retargeting; creator notes Codex outperforms on these tasks.
   - **Retire the implication** that Opus 4.7 vision is broadly state-of-the-art across all visual domains. It's strong on documents/screenshots; weaker on spatial/3D reasoning.

2. **Claude Cowork ≠ Claude Code, despite the desktop app blurring the lines.**
   - Baseline (BV9Bnj3l8pk): described "Claude Code Desktop App" as a unified product.
   - New (cVmkq_aENr8): Cowork (desktop chat UX, built-in connectors, no terminal) is positioned as a *distinct product* from Code (terminal + full customization). Both share the same engine and files.
   - **Adjust mental model:** Cowork is the no-terminal sibling. If you customize via plugins/skills/hooks, you're on Code.

3. **RAG-based code search is being deprecated in favor of file-system tools.**
   - Baseline did not take a position.
   - New (lGalJmyI78w): explicit guidance to drop RAG — the central embedding DB causes hallucinations about modules that no longer exist. Use `ls`/`grep`/`bash` instead.
   - Affects: anyone running custom code-search MCPs over embeddings.

---

## Sources

| Video ID | Title | Channel | Upload date | Strength |
|---|---|---|---|---|
| eSP7PLTXNy8 | Build a proactive agent workflow with Claude Code | Claude (official) | 2026-05-20 | **High** (first-party) |
| lGalJmyI78w | Anthropic Just Revealed The Best Claude Code Setup | AI LABS | 2026-05-21 | High (15K views, links to Anthropic blog) |
| 5j6Vq52fgNU | Sell Claude Managed Agents ($5k Offer) | Kacper Rutkiewicz / AI Made Simple | 2026-05-26 | Medium-High (deep walkthrough, but reseller perspective on pricing) |
| zpfFmtENh2Q | Claude Code Can Now Remember Every Meeting (Bluedot) | Luke Byrne | 2026-05-27 | Medium (vendor-affiliated, but technical walkthrough sound) |
| tNbGO68Opug | Claude Plugins vs MCP vs Skills | Coding Fab | 2026-05-27 | Medium (conceptual, accurate framing) |
| tSIFk3YDsQo | Hooks & Hookify + Playwright (Mastering Claude Pt 4) | Code With Sally | 2026-05-25 | High (1h11m, expert guest Bill Kuehler) |
| YwIGmEs0NdU | Claude Code Run Blender for 1 Hour | Stefan 3D AI | 2026-05-27 | Medium (subjective vision-model take, but well-instrumented test) |
| m7Fh3po0wE0 | Claude to ComfyUI | AI Aidan | 2026-05-27 | Medium |
| Yb2j6C-TD2Q | Multi-channel outreach with Claude Code (Lemlist) | Othmane Khadri | 2026-05-27 | Medium-High (open-source repo, partner Lemlist) |
| OfoGGQ8ab7Y | Claude Code + Paper MCP | Sleek | 2026-05-27 | Medium (vendor demo, but real workflow) |

### Not analyzed (skipped or failed)
- `9KvncVTC6zU` Opus 4.8 leak (French, Nerdy Kings) — transcript fetch blocked by YouTube IP throttle. Leak content unverified; flag for next sweep.
- Sub-1-minute shorts (`0eQ9qRFquBA`, `cVmkq_aENr8`, `0kDryeRcW1Q`, `6CGTPZ4CunA`, `ULEgpAbugxg`, `InbcyF5YJJM`, `Hi66ZQLhHOM`) — used description metadata only.
- Non-English videos (Japanese, Vietnamese, Korean, Chinese, Spanish, Portuguese) — skipped; many were re-uploads of baseline content.

---

## Methodology

- **Searches run 2026-05-27** via YouTube MCP (`mcp__youtube__search_videos`), `publishedAfter=2026-05-15T00:00:00Z`, `order=date`, `maxResults=15`, 5 seed queries: `Claude Code workflow`, `Claude Opus agents`, `Claude Code skills plugins hooks`, `Claude Code MCP`, `Claude Code routines subagents`.
- **Filters:** ≥ 5 min, English-primary or Anthropic-official, channel relevance, skip obvious model-rival re-uploads (Gemini 3.5 Flash, Cursor 2.5 comparisons unless they cited Claude directly).
- **Transcript downloads:** `youtube_transcript_api` 1.x (Python). 10/11 succeeded; 1 failed (IP block on French video).
- **Analysis:** single `general-purpose` subagent given all 10 transcripts + baseline report, asked for novel/confirmed/contradicting claims. Digest used to populate this report; transcript-level citations preserved via video ID.
