# Claude Trends — Delta Report 2026-10-13

*Baseline: 2026-09-18 (claude-trends-2026-09-18-delta.md). Analyzed 12 videos uploaded between 2026-09-18 and 2026-10-13, plus Anthropic primary sources (newsroom, API release notes, Claude Code changelog v2.1.277–v2.1.296).*

## Executive Summary

- **The 5.5 model family shipped in three weeks.** Opus 5.5 (09-22, $4/$20, at Fable 5.1 level on most tasks per Anthropic), Sonnet 5.5 (09-28, $2/$10), Haiku 5.5 (10-07, $0.10/$0.50 up to 100K prompt tokens, 1M context, first Haiku with adjustable effort). Sonnet 4.5 retires 2026-11-30.
- **Claude Code Mods (v2.1.287, 10-01).** Plugins whose TypeScript/JavaScript handlers run inside Claude Code as middleware on internal events. They can rewrite or answer tool calls, prompts and renders, and can draw panes, bands and toasts. This is the most-covered topic among creators in the window.
- **Security caveat on mods, verified.** On a machine with no managed settings and no Team/Enterprise sign-in, a user-installed mod handling `tool.check` **can approve a call that a deny rule refused** (code.claude.com/docs/en/permissions). Mods are not sandboxed.
- **Defaults moved.** Auto mode is the default permission mode on every plan and provider (CL 2.1.284/2.1.285). Opus is the default model on Pro and Team Standard (CL 2.1.280). Medium is the default and recommended effort for Opus 5.5. Anthropic ships `/doctor prompt-audit` to strip instructions written for older models (CL 2.1.283).
- **Plan economics.** Max 5x, Max 20x and Team now include monthly API credits ($100 / $200 / up to $500 pooled; RN 10-07). Sonnet 5.5 cache reads halved to $0.10 (RN 10-07).

## NEW Features / Releases

### Models

| Item | Detail | Source | Strength |
|---|---|---|---|
| Opus 5.5 (`claude-opus-5-5`, 09-22) | 1M context. Adaptive thinking is always on and cannot be disabled. $4/$20, cache read $0.20, cache write $5. Effort runs Low to Max with Medium as default. Fast mode preview up to 2.5x speed at $8/$40. `tool_choice` any/tool returns 400. | anthropic.com/claude-opus-5-5; RN 09-22 | official |
| Opus 5.5 safeguards | Most cyber tasks reroute to Opus 4.8. Biology requires the Life Sciences Verification Program. Preserved thinking applies to API accounts created on or after 2026-08-31. | Opus page | official |
| Sonnet 5.5 (`claude-sonnet-5-5`, 09-28) | $2/$10. Cache reads $0.10 from 10-07. More than 30% faster than Sonnet 5. Thinking blocks are account-bound. Five breaking changes from Sonnet 5, including `between_tools` thinking. | Sonnet page; RN 09-28, 10-07 | official |
| Haiku 5.5 (`claude-haiku-5-5`, 10-07) | 1M context, 128K output. $0.10/$0.50 up to 100K prompt tokens, $0.50/$2.50 above. Adjustable effort, new tokenizer. `budget_tokens`, sampling params and prefill return 400. Positioned for subagents, compaction and summarization. | Haiku page; RN 10-07 | official |
| Sonnet 4.5 deprecated | Announced 09-30; retires 2026-11-30. | RN 09-30 | official |

### Claude Code CLI

- **Auto mode is the default** on every plan and provider (CL 2.1.284), in `claude -p` and the Python SDK (2.1.285), and with a server-side classifier on API and Enterprise (2.1.278). → changelog → official
- **Opus is the default model** on Pro and Team Standard. `/effort` is now per-model, so a saved effort does not carry over to Opus 5.5 (CL 2.1.280). → official
- **Ultracode** is its own toggle (`/effort ultracode on|off`). It no longer forces xhigh effort (CL 2.1.284). → official
- **Per-agent controls:**
  - the Agent tool takes `effort` (CL 2.1.292)
  - subagent frontmatter takes `autoCompactWindow` (CL 2.1.296)
  - `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL` sets the model for workflow agents (CL 2.1.296)
  - `/autocompact` is saved per model (CL 2.1.288) → official
- **`/doctor prompt-audit`** audits CLAUDE.md, skills, agents and commands for patterns written for older models (CL 2.1.283). → official
- **AGENTS.md** is read when a project has no CLAUDE.md (CL 2.1.277), implemented as a built-in mod. → official
- **Plugin tooling:**
  - `claude plugin configure` and `plugin install --marketplace` / `--config` (CL 2.1.285, 2.1.292)
  - `plugin validate` lists each mod's gating hooks (CL 2.1.290) → official
- **Other:**
  - `/code-review --max-findings` (2.1.288)
  - `claude attach` / `claude logs` (2.1.288)
  - Read `allow_large` (2.1.296)
  - hooks `onFailure: "block"` (2.1.295)
  - WebSearch budget refills at 100/hour (2.1.290)
  - subagent results wrapped under a header against injection (2.1.277)
  - project settings can no longer widen sandboxes or enable Chrome (2.1.285–2.1.290) → official

### Mods, Plugins, Skills

- **Mods** (CL 2.1.287; Desktop Code tab from 2.1.286):
  - A mod is a plugin whose `hooks.json` gains a `modules` key pointing at a TS/JS file.
  - Handlers receive `$` (the API back into Claude Code), the event and `next`. They can observe or rewrite an event, or answer it without calling `next`.
  - They draw only in the CLI and the Desktop Code tab. In VS Code, `-p` and cloud sessions, hooks run but nothing draws.
  - Saving the file hot-reloads the mod.
  - Mods are shared through plugin marketplaces.
  - Sources: yUuFvL1lK4k; code.claude.com/docs/en/plugins/mods/overview → official
- **API additions in the window:** `$.ui.notify`, `prompt.autocomplete`, `$.model.complete` with prompt caching, `isDeferred` on `$.tool.register`, and `agent.spawn` covering workflow agents (CL 2.1.288–2.1.295). → official
- **Built-in mods:** `cc-plugin-diff` (`/diff`), `agents-md`, `sec-default`, `telemetry`, `plugin-authoring`, and `you-should-know` (off by default). → MODS docs → official
- **Skills namespacing:** skills in the `anthropic-skills` and `claude-ai` namespaces no longer load from local folders (CL 2.1.282). → official

### MCP

- MCP protocol 2026-07-28 is negotiated by default (CL 2.1.292, 2.1.295). URL-mode elicitation (2.1.281, 2.1.287). Re-auth prompt for added OAuth scope (2.1.288). → official
- Tool-description cap raised to 4,096 characters up front and 16,384 for tool-search loads (CL 2.1.295, 2.1.296). `alwaysLoad: false` defers a whole server behind tool search (2.1.287). `/mcp reconnect all` (2.1.284). → official
- API: tools can be added mid-conversation via system messages without invalidating the cache (`inline-tools-2026-09-15`, RN 09-22). → official

### Routines / Scheduling

- Scheduled and Run-now routines publish private artifacts without asking (CL 2.1.292, 2.1.295). → official
- `/loop` wakeups survive updates and low memory (CL 2.1.290). → official

### Desktop App / claude.ai

- **One Claude:** Chat and Cowork are one Claude. Docs, Slides and Design are available from any conversation on all paid plans, with co-editing and @Claude in doc comments (ICGS7LlRfpI). → strong
- **Claude Motion, Dashboards and a Google Workspace add-in** were reported by creators (LlwhNla5eQg). → moderate (no primary source reviewed)

### API / Managed Agents

- **Managed Agents:**
  - Dynamic workflows in beta (RN 10-09).
  - `limited` networking now governs `web_fetch` and `web_search`, and `web_fetch` is restricted to URLs already seen in the session (RN 10-07).
- **SDKs and Admin API:**
  - Browser-use and computer-use classes in the Python and TS SDKs, beta (RN 10-07).
  - Admin API out of beta (RN 09-30).
- **Models API:** new `capabilities.server_tools`, `capabilities.thinking.types.disabled` and `line` fields (RN 10-01 to 10-06).
- **Cache diagnostics** are out of beta (RN 09-23).
- **Refusal billing** resumes for pre-output refusals in the `bio`, `frontier_llm` and `reasoning_extraction` categories (RN 09-24).

## NEW Workflow Patterns

- **Default to medium effort and escalate for multi-file changes.** One rename task that missed a serializer field succeeded at high effort (jKRl_CSVxyI; vsGwx28z4jk). A single-trial cost ladder for one task: low ~$3.9, medium $12.4, high $16.3, xhigh $25.9, max $50.4, ultracode $18.7. The creator preferred xhigh over max (QCkHIyEPIYo, n=1 per level, weak).
- **Strip configuration for the newer models.**
  - An Anthropic engineer says CLAUDE.md "might go away in the limit" and that logs of failure modes over-constrain the newer models (IZAlq-V19U8).
  - A five-run test of a stripped setup came out 32% faster and 66% cheaper (73KFY9xX8x4). The test used Sonnet 5 and had a broken hook as a confounder.
  - Anthropic shipped `/doctor prompt-audit` for this.
- **Route subagents to cheaper models** through frontmatter or `CLAUDE_CODE_SUBAGENT_MODEL` (jKRl_CSVxyI). Haiku 5.5 is now positioned for this.
- **Opus 5.5 prompt hygiene,** from a creator's reading of Anthropic's guide (vsGwx28z4jk, moderate):
  - say which earlier answers are settled
  - keep a task checklist, because progress updates can end a turn early
  - state a time budget
  - supply a design system
  - provide crop or zoom tools for dense images
- **Surface rejected alternatives.** Most failures come from the model considering the right fix and rejecting it, so ask for notes on decisions and assumptions. A proposed mod would add a `register_assumption` tool (IZAlq-V19U8).
- **Mods practitioners build first:**
  - a cache-expiry countdown with one-click compact or handoff
  - a collision guard for files another session touched recently
  - having Claude read your last ~30 sessions and propose five mods

  Sources: Rn4nmFRPe0s; 9hetShMMp2s.
- **Forked-agent supervisors.** A forked agent keeps the prompt cache, so a supervisor that runs every turn is cheap and leaves no context behind (IZAlq-V19U8).

## NEW Tools / MCPs / Integrations

| Tool | Claude-native? | Note | Source |
|---|---|---|---|
| Built-in `cc-plugin-*` mods | Native | Ship with Claude Code | MODS docs |
| `gh api` in cloud sessions | Native | CL 2.1.288 | changelog |
| Higgsfield MCP | Adjacent | Motion graphics from inside Claude | LlwhNla5eQg (weak) |
| Grok routing to Opus 5.5 | Adjacent | Third-party bot routing work to Claude; unverified | LlwhNla5eQg (weak) |

## Notable Applications

- **Enterprise:**
  - Barclays scaling Claude (NEWS 10-01)
  - Accenture embedded evaluation (09-18)
  - $100M Claude Frontier Academy to train 10,000 engineers (10-02)
- **Science:**
  - novel enzyme system with CRISPR-like repeats (NEWS 09-23)
  - Ebola outbreak response in DRC (09-22)
- **Cyber:** Anthropic Cyber Mission (10-08) and an expanded Cyber Verification Program (10-06). Titles only; contents not reviewed.
- **Creator demos:**
  - a 3D virtual-conference world built from 105 GB of recordings with `/goal` (QCkHIyEPIYo)
  - front-end bake-offs of Opus 5.5 vs GPT-6.1 (-dGYCum7Wo0, weak)

## Pricing / Cost shifts

| Item | Before | After | Source |
|---|---|---|---|
| Opus input / output | $5 / $25 (Opus 5) | $4 / $20 (Opus 5.5) | Opus page |
| Opus cache read / write | $0.50 / $6.25 | $0.20 / $5 | Opus page |
| Sonnet 5.5 cache read | $0.20 | $0.10 (10-07) | RN 10-07 |
| Haiku input / output | $1 / $5 (Haiku 4.5) | $0.10 / $0.50 to 100K tokens; $0.50 / $2.50 above | Haiku page |
| Max / Team API credits | none | $100 Max 5x, $200 Max 20x, up to $500 pooled Team; no rollover; none on Pro | RN 10-07 |

- Anthropic claims typical tasks cost 40% less on Opus 5.5 than on Opus 5. The only confirmation is a single run on Anthropic's channel (jKRl_CSVxyI).
- Refusal billing resumes for three categories (RN 09-24).
- Unverified: a free usage reset expiring 10-23 (vsGwx28z4jk), and a one-hour subscription cache TTL (Rn4nmFRPe0s; 9hetShMMp2s).

## Consensus shifts (vs 2026-09-18)

- **Strengthened: less configuration is better on newer models.** An Anthropic engineer, Anthropic's own tool (`/doctor prompt-audit`) and two creators converge. This extends the 07-31 finding that Anthropic deleted most of Claude Code's own system prompt.
- **Strengthened: medium effort is the default.** The question is now when to escalate, not whether to start high.
- **Changed: auto mode is the default everywhere.** It was introduced as default in August; it is now default on every plan, provider and headless path.
- **Changed: extension moved inward.** Hooks, skills, plugins and MCP are now joined by mods running inside the harness. Creators call it the biggest upgrade since skills (moderate; hype risk).
- **Strengthened: orchestration moves into the product.** Projects are the single-player orchestrator, Claude Tag the multiplayer one, and cloud agents are getting "local hands" (IZAlq-V19U8).

## Contradictions vs baseline

1. **Mods can override deny rules: true, with conditions.**
   - Holds on machines with no managed settings and no Team/Enterprise sign-in. On those, deny rules hold by default. Source: code.claude.com/docs/en/permissions.
   - Mods are not sandboxed (MODS docs).
   - Mods are "on by default" only as a capability. A mod runs only if a plugin containing one is installed, or it is built in.
   - Mitigations: `/plugin` shows the active mod count; `disableAllHooks`; `--safe-mode`. Built-in mods are not stopped by these.
   - Video claim: PZhQfG4LhHI.
2. **Ultracode mechanism.** QCkHIyEPIYo describes ultracode as extra effort plus dynamic workflows. The changelog says it no longer forces xhigh effort and stays on at any effort level (CL 2.1.284). The changelog wins.
3. **`/doctor` and token cost.** 73KFY9xX8x4 credits `/doctor` with a 17K-token context-cost audit. The documented feature is `/doctor prompt-audit`, which checks instructions for older-model patterns. Per-skill context cost is `/skill-doctor` (baseline). The video's figure is unverified.
4. **`/claude-api prompt-audit`** (jKRl_CSVxyI) is not in the changelog; `/doctor prompt-audit` is. Unresolved.
5. **Docs, Slides and Design rollout.** The baseline said Pro and Max first. Anthropic's channel now says all paid plans (ICGS7LlRfpI). This is an update, not a conflict.
6. **Unsupported claims in -dGYCum7Wo0:** "rewrote an industry-standard codebase in 30 minutes at 81% lower cost than Fable" and "#1 on the Artificial Analysis index". Neither is supported by primary sources. The claim of being 30% faster is supported.

## Sources

| Video ID / URL | Title | Channel / publisher | Date | Strength (official / strong / moderate / weak) |
|---|---|---|---|---|
| github.com/anthropics/claude-code CHANGELOG.md | v2.1.277–v2.1.296 | Anthropic | 09-18 to 10-09 | official |
| platform.claude.com/docs/en/release-notes/overview | API release notes, 30 entries in window | Anthropic | 09-18 to 10-09 | official |
| anthropic.com/news | 12 posts in window | Anthropic | 09-18 to 10-08 | official (titles only) |
| anthropic.com/claude-opus-5-5 | Introducing Claude Opus 5.5 | Anthropic | 09-22 | official (vendor benchmarks) |
| anthropic.com/claude-sonnet-5-5 | Introducing Claude Sonnet 5.5 | Anthropic | 09-28 | official (vendor benchmarks) |
| anthropic.com/claude-haiku-5-5 | Introducing Claude Haiku 5.5 | Anthropic | 10-07 | official (vendor benchmarks) |
| code.claude.com/docs/en/plugins/mods/overview | Mods overview | Anthropic docs | fetched 10-13 | official |
| code.claude.com/docs/en/permissions | Configure permissions | Anthropic docs | fetched 10-13 | official |
| jKRl_CSVxyI | Using Claude Opus 5.5 as your daily driver | Claude | 09-23 | strong (vendor; single run) |
| ICGS7LlRfpI | What's new in Claude: September recap | Claude | 10-07 | strong (vendor) |
| yUuFvL1lK4k | Mods in Claude Code | Claude | 10-05 | strong (vendor) |
| IZAlq-V19U8 | Claude Code's Bitter Lesson — Thariq Shihipar | Latent Space | 09-29 | strong on design; weak on third-party incident claims |
| Rn4nmFRPe0s | Claude Mods Is The Biggest Upgrade Since Skills | Chase AI | 10-02 | moderate |
| 9hetShMMp2s | Claude Code Mods Are Game Changers | Nate Herk | 10-02 | moderate |
| QCkHIyEPIYo | Opus 5.5 at Every Effort Level | Nate Herk | 09-24 | moderate (n=1 per level) |
| vsGwx28z4jk | 12 New Rules for Prompting Opus 5.5 | RoboNuggets | 09-24 | moderate (secondhand) |
| PZhQfG4LhHI | Mods Are On by Default; deny-rule override | jason barnes | 10-13 | moderate; verified with caveats |
| 73KFY9xX8x4 | Run /doctor, Then Clean Up Claude Code | Talal Builds AI | 10-13 | weak to moderate (n=5, confounded) |
| LlwhNla5eQg | Claude Motion, Dashboards + More | Brock Mesarich | 10-09 | moderate to weak |
| -dGYCum7Wo0 | Opus 5.5 vs GPT-6.1 vs Haiku 5.5 | Mike's Ai Forge | 10-13 | weak (promotional) |

## Methodology

- **YouTube searches:** 8 searches via the YouTube MCP, published after 2026-09-18.
  - Five seed queries ordered by date (`Claude Code workflow`, `Claude Opus agents`, `Claude Code skills plugins hooks`, `Claude Code MCP`, `Claude Code routines subagents`). These bunched almost entirely onto 10-12/10-13.
  - Three added queries ordered by view count to cover the full window: `Claude Code mods`, `Claude Opus 5.5`, `Claude Haiku 5.5 Anthropic new release`.
- **Primary sources (new Step 2b, first run):**
  - anthropic.com/news and the three model-launch pages, via WebFetch.
  - platform.claude.com release notes, via WebFetch. Two fetches returned the same 30 in-window entries.
  - The Claude Code CHANGELOG, via raw GitHub. Versions were dated from `npm view @anthropic-ai/claude-code time` and the cut was made at v2.1.277 (released 2026-09-18).
- **Filters:**
  - Skipped game-modding false positives on "mods", music videos, shorts, and non-English videos.
  - Kept four official Claude-channel videos under 5 minutes; they are vendor sources, not clickbait.
  - Did not check channel subscriber counts; channels were selected by recognition.
- **Transcripts:** 12 of 15 downloaded via `youtube_transcript_api`. The failures were 1f13Bl1sYkw (Introducing Opus 5.5; no transcript), s5nkj-L2vAw (Introducing Sonnet 5.5; transcripts disabled) and eNh18BWwaz4 (no transcript). The launch-page fetches cover the two launch videos.
- **Analysis:** one general-purpose subagent diffed all sources against the 09-18 baseline. Primary sources outrank video claims.
- **Playlist:** not created (optional step; it would have used 650 YouTube quota units).
